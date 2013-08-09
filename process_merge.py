'''
Processes the merge_5_6.xls (renamed Sequence_Number_and_Table_Number_Lookup.xls
in 2009 3yr ACS and beyond) into a CSV with metadata about each column in the dataset.

There's not enough information about hierarchy in the merge_5_6.xls files, so those
columns are left blank in the output of this script.
'''

import csv
from xlrd import open_workbook
import sys
import os
import re
from titlecase import titlecase

filename = sys.argv[1]


def read_shell(table_id):

    if table_id.endswith('PR'):
        table_id = table_id[:-2]
    if table_id.startswith('C'):
        table_id = 'B%s' % table_id[1:]

    lookup = {}
    hierarchy_stack = [None]*10
    try:
        xlsfile = open_workbook('%s/%s.xls' % (sys.argv[2], table_id), formatting_info=True)
    except IOError, e:
        if e.errno == 2:
            print "Missing table %s/%s.xls" % (sys.argv[2], table_id)
            return lookup
    sheet = xlsfile.sheet_by_index(0)
    for r in range(1, sheet.nrows):
        r_data = sheet.row(r)

        table_id = r_data[0].value.strip()
        line_number = r_data[1].value

        if table_id and line_number and r_data[1].ctype == 2:
            line_number_str = str(line_number)
            if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
                # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
                column_id = "%s%05.1f" % (table_id, line_number)
            else:
                column_id = "%s%03d" % (table_id, line_number)

            cell = sheet.cell(r, 2)
            indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level

            hierarchy_stack[indent] = column_id
            parent_column_id = None
            if indent > 0:
                parent_column_id = hierarchy_stack[indent - 1]

                # Sometimes the parent is actually 2 levels up for some reason
                if not parent_column_id:
                    parent_column_id = hierarchy_stack[indent - 2]

            lookup[column_id] = {
                "indent": indent,
                "parent_column_id": parent_column_id
            }

    return lookup

xlsfile = open_workbook(filename)
sheet = xlsfile.sheet_by_index(0)

root_dir = os.path.dirname(filename)
if not root_dir:
    root_dir = "./"

table_metadata_fieldnames = [
    'table_id',
    'sequence_number',
    'table_title',
    'simple_table_title',
    'subject_area',
    'universe'
]
table_csv = csv.DictWriter(open("%s/census_table_metadata.csv" % root_dir, 'w'), table_metadata_fieldnames)
table_csv.writeheader()

column_metadata_fieldnames = [
    'table_id',
    'sequence_number',
    'line_number',
    'column_id',
    'column_title',
    'indent',
    'parent_column_id'
]
column_csv = csv.DictWriter(open("%s/census_column_metadata.csv" % root_dir, 'w'), column_metadata_fieldnames)
column_csv.writeheader()

TABLE_NAME_REPLACEMENTS = [ # mostly problems with slashes and -- characters
    (r'minor Civil Division Level for 12 Selected States \(Ct, Me, Ma, Mi, Mn, Nh, Nj, Ny, Pa, Ri, Vt, Wi\)',
        'Minor Civil Division Level for 12 Selected States (CT, ME, MA, MI, MN, NH, NJ, NY, PA, RI, VT, WI)'),
    (r'/snap','/SNAP'),
    (r'\(Ssi\)','(SSI)'),
    (r'Va Health Care',r'VA Health Care'),
    (r'Medicaid/means-tested',r'Medicaid/Means-tested'),
    (r'/military',r'/Military'),
    (r'--metropolitan',r'--Metropolitan'),
    (r'--micropolitan',r'--Micropolitan'),
    (r'--place Level',r'--Place Level'),

    (r'--state',r'--State'),
    (r'\(Aian\)',r'(AIAN)'),
]

def clean_table_name(table_name):
    """ title case, strip bogus white space, a few observed direct fixes for title casing..."""
    table_name = re.sub('\s+',' ',table_name) # some have multiple white spaces
    table_name = titlecase(table_name.lower())
    for problem,fix in TABLE_NAME_REPLACEMENTS:
        table_name = re.sub(problem,fix,table_name)
    return table_name.strip()

COLLOQUIAL_REPLACEMENTS = [
    (re.compile(r'in the Past 12 Months'),''),
    (re.compile(r'\(In \d{4} Inflation-adjusted Dollars\)',re.IGNORECASE),''),
    (re.compile('for the Population \d+ Years and Over',re.IGNORECASE), ''),
    (re.compile('Civilian Employed Population 16 Years and Over',re.IGNORECASE),'Civilian Population'),
    (re.compile(r'((grand)?children) Under 18 Years',re.IGNORECASE),r'\1'),
    (re.compile(r'Women \d+ to \d+ Years Who Had a Birth'),'Women Who Had a Birth'),
    (re.compile(r'Field of Bachelor\'s Degree for First Major the Population 25 Years and Over',re.IGNORECASE),'Field of Bachelor\'s Degree for First Major'),
    (re.compile(r'Married Population 15 Years and Over',re.IGNORECASE),'Married Population'),
    (re.compile(r'Population 16 Years and Over',re.IGNORECASE),'Population'), # seems to always have to do with employment, where I think we can take the age for granted
    (re.compile(r'Place of Work for Workers 16 Years and Over',re.IGNORECASE),'Place of Work'),
    (re.compile(r'For Workplace Geography',re.IGNORECASE),''),
    (re.compile(r'\(In Minutes\)',re.IGNORECASE),''),
]

def simplified_table_name(table_name):
    """Make some editorial choices about how to simplify table names for more casual use"""
    for regexp,substitution in COLLOQUIAL_REPLACEMENTS:
        table_name = re.sub(regexp,substitution,table_name)
    table_name = re.sub('\s+',' ',table_name)
    return table_name.strip()

table = {}
rows = []
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    table['table_id'] = r_data[1].value.strip()
    table['sequence_number'] = int(r_data[2].value)
    line_number = r_data[3].value
    position = r_data[4].value
    cells = r_data[5].value
    if r_data[7].ctype == 2:
        title = str(r_data[7].value)
    else:
        title = r_data[7].value
    title = title.strip()
    subject_area = r_data[8].value

    if not line_number and cells:
        # The all-caps description of the table
        table['table_title'] = clean_table_name(title).encode('utf8')
        table['simple_table_title'] = simplified_table_name(table['table_title'])
        # ... this row also includes the subject area text
        table['subject_area'] = subject_area.strip()

        external_shell_lookup = read_shell(table['table_id'])
    elif not line_number and not cells and title.lower().startswith('universe:'):
        table['universe'] = titlecase(title.split(':')[-1]).strip()
    elif line_number:
        row = {}
        row['line_number'] = line_number
        row['table_id'] = table['table_id']
        row['sequence_number'] = table['sequence_number']

        line_number_str = str(line_number)
        if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
            # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
            row['column_id'] = "%s%05.1f" % (row['table_id'], line_number)
        else:
            row['column_id'] = '%s%03d' % (row['table_id'], line_number)
        row['column_title'] = title.encode('utf8')

        column_info = external_shell_lookup.get(row['column_id'])
        if column_info:
            row['indent'] = column_info['indent']
            row['parent_column_id'] = column_info['parent_column_id']

        rows.append(row)
