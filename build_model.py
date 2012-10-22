import csv

def read_csv():
    l = []
    d = None
    current_table = None
    for row in csv.DictReader(open('model.csv'), delimiter=','):
        if not ''.join(row.values()):
            continue
        print bool(row['table_name'])
        if row['table_name']:
            if d:
                l.append(d)
            d = {
                'table_name': row['table_name'],
                'columns': [],
                'foreign_keys': [],
            }
            if row['foreignkeys']:
                d['foreign_keys'] = row['foreignkeys'].split(',')
                
        
        d['columns'].append({
            'name': row['column_name'],
            'type': row['column_type'],
            'length': row['length']
        })
        
    
    return l
        
    
tables = read_csv()
print tables
for table in tables:
    print "%s = Table('%s', metadata," % (table['table_name'], table['table_name'])
    print "    Column('id', Integer, primary_key=True),"
    for fk in table['foreign_keys']:
        print "    Column('%s_id', Integer, ForeignKey(%s.c.id)," % (fk, fk)
    for col in table['columns']:
        length = "(%s)"%col['length'] if col['length'] else ""
        print "    Column('%s', %s" % (col['name'], col['type']) + length
print len(tables)
