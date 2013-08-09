'''
Processes `TableShells` xls files from the Census site to produce a new csv
with complete metadata for every column of every table. This is very similar
to the `process_merge` script in this repo, but since it uses XLS files with
more data it can give you hierarchy information for each column.

To run, first download `TableShells.xls` and `merge_5_6.xls` files from e.g.
http://www2.census.gov/acs2009_1yr/summaryfile/

Then run this script with the filename of the `TableShells` and `merge_5_6.xls`
file you downloaded.

>> python process_shells.py ACS2009TableShells.xls merge_5_6.xls

This will write a `metadata` csv alongside the `TableShells` file with information
about each column in each table.

NOTE: Since the `TableShells` file does not contain sequence number or subject area
information, you currently need to point the script at the corresponding
`merge_5_6.xls` file as a second argument.

'''
import csv
import sys
import os
from xlrd import open_workbook
import re
from titlecase import titlecase

# Parse the Sequence_Number_And_Table_Number_Lookup.xls/merge_5_6.xls file
# so we can get the subject area and sequence number data to match up with
# the shells.
sqn_table_lookup = {}
xlsfile = open_workbook(sys.argv[2])
sheet = xlsfile.sheet_by_index(0)
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    table_id = r_data[1].value
    sqn = int(r_data[2].value)
    subject_area = r_data[8].value.strip()

    if subject_area:
        sqn_table_lookup[table_id] = (sqn, subject_area)

filename = sys.argv[1]

xlsfile = open_workbook(filename, formatting_info=True)
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

topic_fieldnames = [
    'topic_id',
    'topic'
]
topics_csv = csv.DictWriter(open("%s/census_topics.csv" % root_dir, 'w'), topic_fieldnames)
topics_csv.writeheader()

table_topic_fieldnames = [
    'table_id',
    'sequence_number',
    'topic_id'
]
table_topics_csv = csv.DictWriter(open("%s/census_table_topics.csv" % root_dir, 'w'), table_topic_fieldnames)
table_topics_csv.writeheader()

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
    'household': 'families',
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
    'by relationship': 'relationship type',
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

next_topic_id = 0
def add_autoinc_id(container, new_entry):
    global next_topic_id
    if new_entry not in container:
        topics[new_entry] = next_topic_id
        next_topic_id += 1

    return dict(topic_id=container[new_entry], topic=new_entry)

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
    return map(lambda x: add_autoinc_id(topics, x.strip()), all_areas)

topics = {}
this_tables_topics = set()
table = {}
rows = []
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    table_id = r_data[0].value.strip()
    line_number = r_data[1].value
    column_id = r_data[2].value
    if r_data[3].ctype == 2:
        title = str(r_data[3].value)
    else:
        title = r_data[3].value
    title = title.strip()

    if not line_number and title and title.isupper():
        # New table, so clear out the hierarchy stack
        hierarchy_stack = [None]*10

        # Write out the previous table's data
        if table:
            table_csv.writerow(table)
            table_topics_csv.writerows([dict(table_id=table['table_id'], sequence_number=table['sequence_number'], topic_id=topic['topic_id']) for topic in build_topics(table)])
            column_csv.writerows(rows)
            table = {}
            this_tables_topics = set()
            rows = []

        # The all-caps description of the table
        table['table_title'] = clean_table_name(title).encode('utf8')
        table['simple_table_title'] = simplified_table_name(table['table_title'])

        table['table_id'] = table_id
        sqn_data = sqn_table_lookup.get(table['table_id'])
        if sqn_data:
            table['sequence_number'] = sqn_data[0]
            table['subject_area'] = sqn_data[1]
    elif not line_number and title.lower().startswith('universe:'):
        table['universe'] = titlecase(title.split(':')[-1]).strip()
    elif line_number and (r_data[1].ctype == 2) and title:
        row = {}
        row['line_number'] = line_number
        row['table_id'] = table['table_id']
        row['sequence_number'] = table['sequence_number']

        line_number_str = str(line_number)
        if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
            # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
            row['column_id'] = "%s%05.1f" % (table_id, line_number)
        else:
            row['column_id'] = "%s%03d" % (table_id, line_number)
        row['column_title'] = title.encode('utf8')

        cell = sheet.cell(r, 3)
        indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level
        row['indent'] = indent

        hierarchy_stack[indent] = row['column_id']
        if indent > 0:
            parent_column_id = hierarchy_stack[indent - 1]

            # Sometimes the parent is actually 2 levels up for some reason
            if not parent_column_id:
                parent_column_id = hierarchy_stack[indent - 2]

            row['parent_column_id'] = parent_column_id

        rows.append(row)

# Write out the last table's data
if table:
    table_csv.writerow(table)
    table_topics_csv.writerows([dict(table_id=table['table_id'], sequence_number=table['sequence_number'], topic_id=topic['topic_id']) for topic in build_topics(table)])
    column_csv.writerows(rows)
    table = {}
    this_tables_topics = set()
    rows = []

# Write out the topic data
topics_csv.writerows([dict(topic_id=topic_id, topic=topic) for (topic, topic_id) in topics.iteritems()])
