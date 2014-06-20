#-*-encoding=utf-8-*-
"""
Author: Benjamin Arbogast
"""


import json
import re

import requests

import hwdb.model as M


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
            table_text = '\n'.join(current_table)
            # Hack to skip tables which have spanning rows
            # (for which parsing is not yet implemented)
            if not 'rowspan' in table_text:
                tables.append(table_text)
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
        table_rows.pop(0)
        table_rows.pop(0)
    else:
        headers = None

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
        fixed_row['name'], fixed_row['URL'] = parse_maybe_url(model_number)

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

        fixed_row['Frequency'] = pop_one_of(row, ['Frequency', 'Clock Speed'])
        if fixed_row['Frequency'].endswith('&nbsp;GHz'):
            fixed_row['Frequency'] = str(int(float(fixed_row['Frequency'].strip('&nbsp;GHz')) * 1000))

        price = pop_one_of(row, ['Release Price (USD)', ], assert_when_missing=False)
        if price is not None:
            fixed_row['Release price'] = price

        fixed_row['Clock multiplier'] = pop_one_of(row, ['Multiplier', 'Clock Multiplier', '[[clock multiplier|Mult]]'])
        fixed_row['Clock multiplier'] = fixed_row['Clock multiplier'].strip('×'.decode('utf-8'))

        fixed_row['Part number'] = multi_split(pop_one_of(row, ['Part Number(s)']), ['\n', '<br>'])
        fixed_row['Voltage range'] = pop_one_of(row, ['Voltage', 'Voltage Range'])
        fixed_row['Front side bus'] = pop_one_of(row, ['[[Front Side Bus]]', 'FSB Speed']).strip(' MT/s')
        fixed_row['Release date'] = pop_one_of(row, ['Release Date', ])
        fixed_row['L2 cache'] = pop_one_of(row, ['L2 Cache', '[[CPU caches#Multi-level caches|L2-Cache]]'])
        fixed_row['Socket'] = pop_one_of(row, ['Socket', '[[CPU socket|Socket]]'])
        fixed_row['Thermal design power'] = pop_one_of(row, ['[[Thermal Design Power|TDP]]', '[[Thermal design power|TDP]]', 'TDP']).strip(' W')

        fixed_data.append(fixed_row)

        #left_over_cols.update(row.keys())

    return fixed_data


def replace_html_chars(table_row_dicts):
    """ Replaces &nbsp; with a blank and decodes utf-8 """
    for row in table_row_dicts:
        for k in row:
            if isinstance(row[k], basestring):
                row[k] = row[k].replace('&nbsp;', ' ')

                # doesnt seem to work when getting the text via HTTP (and not from the file)
                #row[k] = row[k].decode('utf-8')
            elif isinstance(row[k], list):
                #row[k] = [x.replace('&nbsp;', ' ') for x in row[k]]
                pass
            elif row[k] is None:
                pass
            else:
                raise Exception()


def insert_record(attributes):
    name = attributes.pop('name')
    attributes.pop('Voltage range') # TODO
    attributes.pop('Socket') # TODO
    attributes.pop('Part number') # TODO
    attributes.pop('sspecs') # TODO
    if attributes['url'] is None:
        attributes.pop('url')
    part = M.Part.init(name, 'Pentium 4', attributes=attributes)
    M.db_session.add(part)


def get_all_rows(wikitext):
    all_dicts = []
    tables = split_table_strings(wikitext)
    for table in tables:
        row_dicts = parse_table_rows(table)
        fixed_row_dicts = fix_table_row_dict(row_dicts)
        replace_html_chars(fixed_row_dicts)
        all_dicts.extend(fixed_row_dicts)

    return all_dicts


if __name__ == '__main__':
    wikitext = open('wikiarticle.txt').read()
    print(get_all_rows(wikitext))
