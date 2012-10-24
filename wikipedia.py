#-*-encoding=utf-8-*-

import json
import re

import requests



# https://github.com/earwig/mwparserfromhell
# https://bitbucket.org/JanKanis/wiki2csv


def fetch_from_wikipedia():
    # http://en.wikipedia.org/w/api.php
    # http://en.wikipedia.org/w/api.php?format=xml&action=query&titles=List_of_Intel_Pentium_4_microprocessors&prop=revisions&rvprop=content

    # http://en.wikipedia.org/wiki/List_of_Intel_Pentium_4_microprocessors
    # http://en.wikipedia.org/wiki/Pin_grid_array
    payload = {'format': 'json', 'action': 'query', 'titles': 'List_of_Intel_Pentium_4_microprocessors', 'prop': 'revisions', 'rvprop': 'content'}
    r = requests.get("http://en.wikipedia.org/w/api.php", params=payload)

    j = json.loads(r.text)
    wikitext = j['query']['pages']['4589953']['revisions'][0]['*']
    return wikitext


# Helpers
def parse_maybe_url(text):
    """ Tries to parse a wikipedia url and returns a tuple of (text, url) """
    m = re.search('(?P<prefix>.*)\[(?P<url>.+)(?P<url_label> .*)\](?P<postfix>.*)', text)
    if not m:
        return text, None
    d = m.groupdict()
    return d['prefix'] + d['url_label'].lstrip() + d['postfix'], d['url']

def pop_one_of(d, keys, assert_when_missing=True):
    """
    Pop the value of the first key of the given keys which is found in the
    dict and return it. If assert_when_missing is True, an Exception is raised,
    else None is returned.
    """
    for k in keys:
        if k in d:
            return d.pop(k)
    else:
        if assert_when_missing:
            raise KeyError('None of %s is in %s'%(keys, d))
        else:
            return None

def multi_split(s, seperators):
    """ Splits the string with every given seperator """
    l = s.split(seperators.pop())
    for sep in seperators:
        new_l = []
        for el in l:
            new_l.extend(el.split(sep))
        l = new_l
    return l


# Parsers
def split_table_strings(wikitext):
    """ Extracts the tables from a wikipedia article. Returns a list with
    strings starting with the table header and ending with the last table row """
    tables = []
    table_is_active = False
    current_table = []

    for line in wikitext.split('\n'):
        if line.strip().startswith('|}'):
            tables.append('\n'.join(current_table))
            table_is_active = False
            current_table = []

        if table_is_active:
            current_table.append(line)

        if line.strip().startswith('{|'):
            table_is_active = True

    return tables


def parse_table_rows(table_string):
    """ Parses each table row to a dict. The header of the table will be key of
    the dict. Tables rows spanning multiple physical rows are recognized. """
    headers = None
    data = []
    current_row = None

    # remove empty lines
    table_rows = [row for row in table_string.split('\n') if row.strip()]

    # parse + remove header
    if table_rows[0].startswith('!'):
        headers = [cell.strip() for cell in table_rows[0].strip('!').split('||')]
    else:
        headers = None
    table_rows.pop(0)
    table_rows = [row for row in table_string.split('\n') if row.strip()]

    # join rows again and split them by |- to get table rows spanning multiple
    # physical rows
    for row in '\n'.join(table_rows).split('|-'):
        row_dict = {}
        row = row.strip('|')
        for i, cell in enumerate(row.split('||')):
            row_dict[headers[i]] = cell.strip()
        data.append(row_dict)

    return data

def fix_table_row_dict(table_row_dicts):
    """ Returns the row dicts with unified keys. Cells containing multiple
    values are returned as list/dicts """
    fixed_data = []
    left_over_cols = set()
    for row in table_row_dicts:
        fixed_row = {}
        model_number = pop_one_of(row, ('Model Number', 'Model Number  Clock Speed'))
        fixed_row['name'], fixed_row['url'] = parse_maybe_url(model_number)

        seperators = []
        sspec_number = pop_one_of(row, ('sSpec&nbsp;Number', 'sSpec number', 'sSpec Number'))
        if '\n' in sspec_number:
            seperators.append('\n')
        if '<br>' in sspec_number:
            seperators.append('<br>')
        if len(seperators) > 1:
            raise Exception('Line has newline and breaks, dont know what to do: %r'%sspec_number)
        if seperators:
            specs = sspec_number.split(seperators[0])
        else:
            specs = [sspec_number]

        fixed_row['sspecs'] = []
        for s in specs:
            spec_name, spec_url = parse_maybe_url(s)
            fixed_row['sspecs'].append(dict(name=spec_name, url=spec_url))

        fixed_row['part_numbers'] = multi_split(pop_one_of(row, ['Part Number(s)']), ['\n', '<br>'])
        fixed_row['frequency'] = pop_one_of(row, ['Frequency', 'Clock Speed'])
        fixed_row['voltage'] = pop_one_of(row, ['Voltage', 'Voltage Range'])
        fixed_row['fsb'] = pop_one_of(row, ['[[Front Side Bus]]', 'FSB Speed'])
        fixed_row['release'] = pop_one_of(row, ['Release Date', ])
        fixed_row['l2cache'] = pop_one_of(row, ['L2 Cache', '[[CPU caches#Multi-level caches|L2-Cache]]'])
        fixed_row['multiplier'] = pop_one_of(row, ['Multiplier', 'Clock Multiplier', '[[clock multiplier|Mult]]'])
        fixed_row['socket'] = pop_one_of(row, ['Socket', '[[CPU socket|Socket]]'])
        fixed_row['tdp'] = pop_one_of(row, ['[[Thermal Design Power|TDP]]', '[[Thermal design power|TDP]]', 'TDP'])
        fixed_row['price'] = pop_one_of(row, ['Release Price (USD)', ], assert_when_missing=False)

        fixed_data.append(fixed_row)

        #left_over_cols.update(row.keys())

    return fixed_data


def replace_html_chars(table_row_dicts):
    """ Replaces &nbsp; with a blank and decodes utf-8 """
    for row in table_row_dicts:
        for k in row:
            if isinstance(row[k], basestring):
                row[k] = row[k].replace('&nbsp;', ' ').decode('utf-8')
            elif isinstance(row[k], list):
                #row[k] = [x.replace('&nbsp;', ' ') for x in row[k]]
                pass
            elif row[k] is None:
                pass
            else:
                raise Exception()


def main():
    #wikitext = fetch_from_wikipedia()
    wikitext = open('wikiarticle.txt').read()
    tables = split_table_strings(wikitext)
    for table in tables:
        row_dict = parse_table_rows(table)
        fixed_row_dict = fix_table_row_dict(row_dict)
        replace_html_chars(fixed_row_dict)

    print fixed_row_dict
    import pprint;pprint.pprint(fixed_row_dict)

    return fixed_row_dict


if __name__ == '__main__':


    main()