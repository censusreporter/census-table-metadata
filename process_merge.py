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

import json
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
            if not indent and cell.value.startswith('  '):
                # In the 2008 shells they show the indent level with two spaces instead of XLS indents
                (spaces, table_name) = re.search('^([  ]*)(.*)$', cell.value).groups()
                indent = len(spaces) / 2

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

release = filename[:11]

table_file = open("%s/census_table_metadata.txt" % root_dir, 'w')
column_file = open("%s/census_column_metadata.txt" % root_dir, 'w')

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

def find_denominator_column(table, cols):
    if cols and len(cols) > 1 and cols[0]['column_title'].lower().startswith('total') and table and not table['table_title'].lower().startswith('median'):
        return cols[0]['column_id']
    else:
        return None

table_ids_already_written = set()
table = {}
columns = []
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    table_id = r_data[1].value.strip()
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
        # Write out the previous table's data
        if table and table_id != table['table_id']:
            table['denominator_column_id'] = find_denominator_column(table, columns)
            table['topics'] = build_topics(table)
            if table['table_id'] in table_ids_already_written:
                print 'Skipping %s' % table['table_id']
            else:
                table['release'] = release

                table_file.write(json.dumps({'index': {'_index': 'census', '_type': 'table', '_id': release + table['table_id']}}) + "\n")
                table_file.write(json.dumps(table) + "\n")
                for column in columns:
                    column_file.write(json.dumps({'index': {'_index': 'census', '_type': 'column', '_id': release + column['column_id']}}) + "\n")
                    column_file.write(json.dumps(column) + "\n")
            table_ids_already_written.add(table['table_id'])
            table = {}
            columns = []

        # The all-caps description of the table
        table['table_title'] = clean_table_name(title).encode('utf8')
        table['simple_table_title'] = simplified_table_name(table['table_title'])
        # ... this row also includes the subject area text
        table['subject_area'] = subject_area.strip()

        table['table_id'] = table_id

        external_shell_lookup = read_shell(table['table_id'])
    elif not line_number and not cells and title.lower().startswith('universe:'):
        table['universe'] = titlecase(title.split(':')[-1]).strip()
    elif line_number:
        column = {}
        column['line_number'] = line_number
        column['table_id'] = table['table_id']
        column['release'] = release

        line_number_str = str(line_number)
        if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
            # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
            column['column_id'] = "%s%05.1f" % (table['table_id'], line_number)
        else:
            column['column_id'] = '%s%03d' % (table['table_id'], line_number)
        column['column_title'] = title.encode('utf8')

        column_info = external_shell_lookup.get(column['column_id'])
        if column_info:
            column['indent'] = column_info['indent']
            column['parent_column_id'] = column_info['parent_column_id']

        columns.append(column)

# Write out the last table's data
if table:
    table['denominator_column_id'] = find_denominator_column(table, columns)
    table['topics'] = '{%s}' % ','.join(['"%s"' % topic for topic in build_topics(table)])
    if table['table_id'] in table_ids_already_written:
        print 'Skipping %s' % table['table_id']
    else:
        table['release'] = release

        table_file.write(json.dumps({'index': {'_index': 'census', '_type': 'table', '_id': release + table['table_id']}}) + "\n")
        table_file.write(json.dumps(table) + "\n")
        for column in columns:
            column_file.write(json.dumps({'index': {'_index': 'census', '_type': 'column', '_id': release + column['column_id']}}) + "\n")
            column_file.write(json.dumps(column) + "\n")
    table_ids_already_written.add(table['table_id'])
    table = {}
    columns = []

table_file.close()
column_file.close()
