'''
Processes the merge_5_6.xls from 2007 and 2008 vintage ACS releases into a CSV
with metadata about each column in the dataset.

There's not enough information about hierarchy in the merge_5_6.xls files, so the
second argument is the base directory containing the shell files for each table
as found in on the Census website [0].

Run as follows:
    python process_merge.py acs2007_1yr_merge_5_6.xls acs2007_shells

[0] http://www2.census.gov/acs/downloads/shells/2007/Detailed_Tables/
'''

import unicodecsv
from xlrd import open_workbook
import sys
import os
import re
from titlecase import titlecase
import json

def read_shells(path):
    lookup = {}

    if os.path.isdir(path):
        for shell_file in os.listdir(path):
            single_shell = read_shell(os.path.join(path, shell_file))
            # print json.dumps(single_shell, indent=2)
            lookup.update(single_shell)
    elif os.path.isfile(path):
        lookup = read_shell(path)

    return lookup

def read_shell(path):
    lookup = {}
    try:
        xlsfile = open_workbook(path, formatting_info=True)
    except NotImplementedError:
        # https://stackoverflow.com/a/13914953/73004
        print("ERROR: You're trying to open an .xlsx. Open '{}' in Excel and save it as an .xls file and try again.".format(path))
        sys.exit(22)
    sheet = xlsfile.sheet_by_index(0)

    # Find the columns we're interested in
    header = sheet.row(0)
    title_column = None
    table_id_column = None
    line_number_column = None
    col_number = 0
    for col in header:
        clean_column_name = re.sub(r'\s+', '', col.value)
        if clean_column_name == 'Stub':
            title_column = col_number
        elif clean_column_name in ('Table ID', 'TableID'):
            table_id_column = col_number
        elif clean_column_name in ('Line', 'Order'):
            # 2010 5yr uses "Order" instead of line number. >:(
            line_number_column = col_number
        col_number += 1

    for r in range(1, sheet.nrows):
        r_data = sheet.row(r)

        table_id = r_data[table_id_column].value.strip()

        if not table_id:
            continue

        if table_id not in lookup:
            lookup[table_id] = {}
            hierarchy_stack = [None]*10

        line_number = r_data[line_number_column].value

        if table_id and line_number and r_data[line_number_column].ctype in (1, 2):
            line_number_str = str(line_number)

            if not line_number_str.strip():
                continue

            if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
                # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
                column_id = "%s%05.1f" % (table_id, float(line_number))
            else:
                column_id = "%s%03d" % (table_id, int(line_number))

            cell = sheet.cell(r, title_column)
            indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level
            if not indent and cell.value.startswith('  '):
                # In the 2008 shells they show the indent level with two spaces instead of XLS indents
                (spaces, table_name) = re.search('^([  ]*)(.*)$', cell.value).groups()
                indent = len(spaces) // 2

            hierarchy_stack[indent] = column_id
            parent_column_id = None
            if indent > 0:
                parent_column_id = hierarchy_stack[indent - 1]

                # Sometimes the parent is actually 2 levels up for some reason
                if not parent_column_id:
                    parent_column_id = hierarchy_stack[indent - 2]

            # print "{}, {} has indent {} parent column {}".format(table_id, column_id, indent, parent_column_id)
            lookup[table_id][column_id] = {
                "indent": indent,
                "parent_column_id": parent_column_id
            }

    return lookup

filename = sys.argv[1]
shell_lookup = read_shells(sys.argv[2])

xlsfile = open_workbook(filename)
sheet = xlsfile.sheet_by_index(0)


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
    table_name = re.sub(r'\s+', ' ', table_name) # some have multiple white spaces
    table_name = titlecase(table_name.lower())
    for problem,fix in TABLE_NAME_REPLACEMENTS:
        table_name = re.sub(problem,fix,table_name)
    return table_name.strip()

COLLOQUIAL_REPLACEMENTS = [
    (re.compile(r'in the Past 12 Months'), ''),
    (re.compile(r'\(In \d{4} Inflation-adjusted Dollars\)',re.IGNORECASE), ''),
    (re.compile(r'for the Population \d+ Years and Over',re.IGNORECASE), ''),
    (re.compile(r'Civilian Employed Population 16 Years and Over',re.IGNORECASE), 'Civilian Population'),
    (re.compile(r'((grand)?children) Under 18 Years',re.IGNORECASE), r'\1'),
    (re.compile(r'Women \d+ to \d+ Years Who Had a Birth'), 'Women Who Had a Birth'),
    (re.compile(r'Field of Bachelor\'s Degree for First Major the Population 25 Years and Over',re.IGNORECASE), 'Field of Bachelor\'s Degree for First Major'),
    (re.compile(r'Married Population 15 Years and Over',re.IGNORECASE), 'Married Population'),
    (re.compile(r'Population 16 Years and Over',re.IGNORECASE), 'Population'), # seems to always have to do with employment, where I think we can take the age for granted
    (re.compile(r'Place of Work for Workers 16 Years and Over',re.IGNORECASE), 'Place of Work'),
    (re.compile(r'For Workplace Geography',re.IGNORECASE), ''),
    (re.compile(r'\(In Minutes\)',re.IGNORECASE), ''),
]

def simplified_table_name(table_name):
    """Make some editorial choices about how to simplify table names for more casual use"""
    for regexp, substitution in COLLOQUIAL_REPLACEMENTS:
        table_name = re.sub(regexp, substitution, table_name)
    table_name = re.sub(r'\s+', ' ', table_name)
    return table_name.strip()

SUBJECT_AREA_TO_TOPICS = {
    'Age-Sex': 'age, sex',
    'Hispanic Origin': 'race',
    'Race': 'race',

    'Earnings': 'income',
    'Employment Status': 'employment',
    'Health Insurance': 'health insurance',
    'Income': 'income',
    'Industry-Occupation-Class of Worker': 'employment',
    'Journey to Work': 'commute',
    'Poverty': 'poverty',
    'Transfer Programs': 'public assistance',

    'Ancestry': 'ancestry',
    'Children - Relationship': 'children',
    'Disability': 'disability',
    'Educational Attainment': 'education',
    'Fertility': 'fertility',
    'Foreign Birth': 'place of birth',
    'Grand(Persons) - Age of HH Members': 'children, grandparents',
    'Households - Families': 'families',
    'Language': 'language',
    'Marital Status': 'marital status',
    'Place of Birth - Native': 'place of birth',
    'Residence Last Year - Migration': 'migration',
    'School Enrollment': 'education',
    'Veteran Status': 'veterans',
    'Voting-Age Population': 'citizen',
    'Computer and Internet Usage': 'computer, internet',

    'Housing': 'housing',
    'Unweighted Count': 'technical',
    'Group Quarters': 'group quarters',
    'Quality Measures': 'technical',
    'Imputations': 'technical',
}

TABLE_NAME_TEXT_TO_TOPICS = {
    'ancestry': 'ancestry',
    'race': 'race',
    'total population': 'age, sex',
    'children': 'children',
    'disability': 'disability',
    'bachelor\'s degree': 'education',
    'education': 'education',
    'school': 'education',
    'employ': 'employment',
    'occupation': 'employment',
    'work': 'employment',
    'families': 'families',
    'family': 'families',
    'grandparent': 'grandparents',
    'health insurance': 'health insurance',
    'living arrang': 'families',
    'household': 'families',
    'earnings': 'income',
    'income': 'income',
    'geographical mobility': 'migration',
    'poverty': 'poverty',
    'food stamps': 'public assistance',
    'public assistance': 'public assistance',
    '65 years and over': 'seniors',
    'va health care': 'veterans',
    'veteran': 'veterans',
    'means of transportation': 'commute',
    'travel time': 'commute',
    'vehicles': 'commute',
    'workplace geography': 'commute',
    'time leaving home': 'commute',
    'imputation': 'technical',
    'unweighted': 'technical',
    'coverage rate': 'technical',
    'nonresponse rate': 'technical',
    'movers': 'migration',
    'place of work': 'commute',
    'workers': 'employment',
    'group quarters': 'group quarters',
    'had a birth': 'fertility',
    'income deficit': 'poverty',
    'difficulty': 'disability',
    'disabilities': 'disability',
    'tricare': 'health insurance',
    'medicare': 'health insurance',
    'medicaid': 'health insurance',
    'va health care': 'health insurance',
    'gross rent': 'costs and value',
    'contract rent': 'costs and value',
    'rent asked': 'costs and value',
    'price asked': 'costs and value',
    'value': 'costs and value',
    'utilities': 'costs and value',
    'costs': 'costs and value',
    'real estate taxes': 'costs and value',
    'rooms': 'physical characteristics', # including bedrooms
    'facilities': 'physical characteristics',
    'heating': 'physical characteristics',
    'units in structure': 'physical characteristics',
    'year structure built': 'physical characteristics',
    'tenure': 'tenure',
    'moved into unit': 'tenure',
    'occupan': 'occupancy', # add vacancy to topic?
    'vacan': 'occupancy',
    'mortgage': 'mortgage',
    'under 18 years': 'children',
    'family type': 'families',
    'nonfamily': 'roommates',
}

TABLE_NAME_TEXT_TO_FACETS = {
    'by age': 'age',
    'age by': 'age',
    'citizenship': 'citizenship',
    'naturalization': 'citizenship, place of birth',
    'by famil': 'family type',
    'by sex': 'sex',
    'sex by': 'sex',
    # 'by household': 'household type',
    # 'household type by': 'household type',
    'language': 'language',
    'marriage': 'marital status',
    'marital': 'marital status',
    'nativity': 'place of birth',
    'place of birth': 'place of birth',
    '(white': 'race',
    '(black': 'race',
    'american indian': 'race',
    'asian alone': 'race',
    'alaska native': 'race',
    'native hawaiian': 'race',
    'some other race': 'race',
    'two or more races': 'race',
    'hispanic': 'race',
}

def build_topics(table):
    table_name = table['table_title']
    subject_area = table['subject_area']
    all_areas = set()
    if subject_area:
        all_areas.update(map(lambda x: x.strip(),SUBJECT_AREA_TO_TOPICS[subject_area].split(',')))
    for k,v in TABLE_NAME_TEXT_TO_TOPICS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x: x.strip(),v.split(',')))
    for k,v in TABLE_NAME_TEXT_TO_FACETS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x:x.strip(),v.split(',')))
    return map(lambda x: x.strip(), all_areas)

def find_denominator_column(table, rows):
    if rows and rows[0]['column_title'].lower().startswith('total') and table and not table['table_title'].lower().startswith('median'):
        return rows[0]['column_id']
    else:
        return None

tables = {}
table = {}
rows = []
previous_line_number = 0
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    table_id = r_data[1].value.strip()
    line_number = r_data[3].value
    cells = r_data[5].value
    if r_data[7].ctype == 2:
        title = str(r_data[7].value)
    else:
        title = r_data[7].value
    title = title.strip()
    subject_area = r_data[8].value

    # print "table_id:{}, line_number:{}, cells:{}, title:{}, subject_area:{},".format(table_id, line_number, cells, title, subject_area)

    # In 2009 metadata, they seem to have used "." to signify null.
    # In 2012 metadata, they seem to have used " " to signify null.
    if type(line_number) is not float:
        line_number = None

    if not line_number and cells:
        # Save the previous table's data
        if table and table_id != table['table_id']:
            table['denominator_column_id'] = find_denominator_column(table, rows)
            table['topics'] = '{%s}' % ','.join(['"%s"' % topic for topic in build_topics(table)])
            if table['table_id'] in tables:
                print('Skipping %s because it was already written.' % table['table_id'])
            else:
                table['columns'] = rows
                tables[table['table_id']] = table
            table = {}
            rows = []
            previous_line_number = 0

        # The all-caps description of the table
        table['table_title'] = clean_table_name(title)
        table['simple_table_title'] = simplified_table_name(table['table_title'])
        # ... this row also includes the subject area text
        table['subject_area'] = subject_area.strip()

        table['table_id'] = table_id

        external_shell_lookup = shell_lookup.get(table_id, {})
        if not external_shell_lookup:
            tables[table['table_id']] = None
            print("Could not find shells for table '{}', won't write that table out as its likely deleted from the release.".format(table['table_id']))
    elif not line_number and not cells and title.lower().startswith('universe:'):
        table['universe'] = titlecase(title.split(':')[-1]).strip()
    elif line_number:
        row = {}
        row['table_id'] = table['table_id']

        line_number_str = str(line_number)
        if title.endswith('--') and (line_number - previous_line_number > 1.0):
            # In the 2009 releases, the line numbers that are headers (x.5 and x.7) don't have decimals
            # so lets manufacture them here if this line is out of order.
            line_number = line_number / 10.0
        row['line_number'] = line_number
        previous_line_number = line_number

        if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
            # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
            row['column_id'] = "%s%05.1f" % (row['table_id'], line_number)
        else:
            row['column_id'] = '%s%03d' % (row['table_id'], line_number)
        row['column_title'] = title

        column_info = external_shell_lookup.get(row['column_id'])
        # print "Row {} has info {}".format(row['column_id'], column_info)
        if column_info:
            row['indent'] = column_info['indent']
            row['parent_column_id'] = column_info['parent_column_id']

        rows.append(row)

# Save the last table's data
if table:
    table['denominator_column_id'] = find_denominator_column(table, rows)
    table['topics'] = '{%s}' % ','.join(['"%s"' % topic for topic in build_topics(table)])
    if table['table_id'] in tables:
        print('Skipping %s because it was already written.' % table['table_id'])
    table['columns'] = rows
    tables[table['table_id']] = table
    table = {}
    rows = []
    previous_line_number = 0

# Write out the tables and columns to CSV
root_dir = os.path.dirname(filename)
if not root_dir:
    root_dir = "./"

with open("%s/census_table_metadata.csv" % root_dir, 'wb') as table_file:
    table_metadata_fieldnames = [
        'table_id',
        'table_title',
        'simple_table_title',
        'subject_area',
        'universe',
        'denominator_column_id',
        'topics'
    ]
    table_csv = unicodecsv.DictWriter(table_file, table_metadata_fieldnames)
    table_csv.writeheader()

    with open("%s/census_column_metadata.csv" % root_dir, 'wb') as column_file:
        column_metadata_fieldnames = [
            'table_id',
            'line_number',
            'column_id',
            'column_title',
            'indent',
            'parent_column_id'
        ]
        column_csv = unicodecsv.DictWriter(column_file, column_metadata_fieldnames)
        column_csv.writeheader()

        for table_id, table in sorted(tables.items()):
            if not table:
                # don't write out a table that was marked to be skipped on purpose
                continue

            columns = table.pop('columns')
            table_csv.writerow(table)
            for column in sorted(columns, key=lambda a: a['column_id']):
                column_csv.writerow(column)
