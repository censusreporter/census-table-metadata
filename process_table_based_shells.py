'''
Uses the new format for "table shells" produced for the ACS "tabled-based" 
detailed file data release, and some other information we'll have to figure out
along the way.
'''
import argparse
import codecs
import csv
import os
import re
import requests
from collections import defaultdict
from contextlib import closing
from titlecase import titlecase
from pathlib import Path

table_metadata_fieldnames = [
    'table_id',
    'table_title',
    'simple_table_title',
    'subject_area',
    'universe',
    'denominator_column_id',
    'topics'
]
column_metadata_fieldnames = [
    'table_id',
    'line_number',
    'column_id',
    'column_title',
    'indent',
    'parent_column_id'
]


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

SUBJECT_AREAS = { # these came in the old table shells, but aren't in the new version.
    '01': 'Age-Sex',
    '02': 'Race',
    '03': 'Hispanic Origin',
    '04': 'Ancestry',
    '05': 'Foreign Birth',
    '06': 'Place of Birth - Native',
    '07': 'Residence Last Year - Migration',
    '08': 'Journey to Work',
    '09': 'Children - Relationship',
    '10': 'Grand(Persons) - Age of HH Members',
    '11': 'Households - Families',
    '12': 'Marital Status',
    '13': 'Fertility',
    '14': 'School Enrollment',
    '15': 'Educational Attainment',
    '16': 'Language',
    '17': 'Poverty',
    '18': 'Disability',
    '19': 'Income',
    '20': 'Earnings',
    '21': 'Veteran Status',
    '22': 'Transfer Programs',
    '23': 'Employment Status',
    '24': 'Industry-Occupation-Class of Worker',
    '25': 'Housing',
    '26': 'Group Quarters',
    '27': 'Health Insurance',
    '28': 'Computer and Internet Usage',
    '29': 'Voting-Age Population',
    '98': 'Quality Measures',
    '99': 'Imputations'
 }

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


UNIVERSE_REPLACEMENTS = [
    (r'Nhpi', 'NHPI'),
    (r'Aian', 'AIAN'),
]


def clean_universe(universe):
    """ title case, strip bogus white space, a few observed direct fixes for title casing..."""
    universe = universe.strip()
    universe = titlecase(universe.lower())
    for problem, fix in UNIVERSE_REPLACEMENTS:
        universe = re.sub(problem, fix, universe)
    return universe.strip()


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
    'Voting-Age Population': 'cvap',
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

def build_topics(table_name, subject_area):
    all_areas = set()
    if subject_area:
        all_areas.update(map(lambda x: x.strip(),SUBJECT_AREA_TO_TOPICS[subject_area].split(',')))
    for k,v in TABLE_NAME_TEXT_TO_TOPICS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x: x.strip(),v.split(',')))
    for k,v in TABLE_NAME_TEXT_TO_FACETS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x:x.strip(),v.split(',')))
    return list(map(lambda x: x.strip(), sorted(all_areas)))


def find_denominator_column(table: dict, rows: list):
    """For most tables, the first row is a total row, and that row is the thing to use
       to show estimates as percentages.  But a table must have at least 3 rows for
       percentages to be meaningful -- and percentages are not meaningful for
       median estimates, so sometimes we return None
    """
    if rows and len(rows) > 2 and rows[0]['column_title'].lower().startswith('total') and table and not table['table_title'].lower().startswith('median'):
        return rows[0]['column_id']
    else:
        return None

def write_files(root_dir, tables):
    with open(os.path.join(root_dir, "census_table_metadata.csv"), 'w') as table_file:
        table_writer = csv.DictWriter(table_file, table_metadata_fieldnames, lineterminator='\n')
        table_writer.writeheader()

        with open(os.path.join(root_dir, "census_column_metadata.csv"), 'w') as column_file:
            column_writer = csv.DictWriter(column_file, column_metadata_fieldnames, lineterminator='\n')
            column_writer.writeheader()

            for table_id, table in sorted(tables.items()):
                columns = table.pop('columns')
                table_writer.writerow(table)

                for column in sorted(columns, key=lambda a: a['column_id']):
                    column_writer.writerow(column)

def read_table_shell(url):
    """Product a dict with table_ids for keys and table data structures as values.
    The structures should have all the columns that go in a table 
    eg table_metadata_fieldnames
    plus a 'columns' key which has the data which goes in a column metadata file
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()

    tables = {}
    with closing(resp) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter="|")
        # Table ID|Line|Indent|Unique ID|Label|Title|Universe|Type
        for i,line in enumerate(reader):
            if i > 0: # skip header
                (table_id, line_no, indent, var_id, var_label, table_title, universe, data_type) = line
                if table_id[:2] == 'B9': continue # skipping technical tables now
                column_id = var_id.replace('_','')
                if len(column_id) == 0:
                    column_id = f"{table_id}{line_no.zfill(5)}"
                indent = int(indent)
                try:
                    table = tables[table_id]
                except KeyError:
                    table_title = clean_table_name(table_title)
                    simple_title = simplified_table_name(table_title)
                    subject_area = SUBJECT_AREAS.get(table_id[1:3])
                    topics = build_topics(table_title, subject_area)
                    topics = '{%s}' % ','.join(['"%s"' % topic for topic in topics])
                    table = {
                            'table_id': table_id,
                            'table_title': table_title, 
                            'simple_table_title': simple_title, 
                            'subject_area': subject_area,
                            'universe': universe,
                            'denominator_column_id': None, # after we know all columns, try find_denominator_column
                            'topics': topics, 
                            'columns': []
                    }
                    tables[table_id] = table

                parent_column_id = ''
                if indent > 0:
                    for col in reversed(table['columns']):
                        if col['indent'] < indent:
                            parent_column_id = col['column_id']
                            break

                column = {
                    'table_id': table_id,
                    'line_number': line_no,
                    'column_id': column_id,
                    'column_title': var_label,
                    'indent': indent,
                    'parent_column_id': parent_column_id # parent_column_id # assign these after maybe?

                }
                table['columns'].append(column)

    for table in tables.values():
        denom_col = find_denominator_column(table, table['columns'])
        table['denominator_column_id'] = denom_col

    return tables

def main(root_dir, merge_url):

    tables = read_table_shell(merge_url)

    root_path = Path(root_dir)    
    root_path.mkdir(parents=True, exist_ok=True)
    write_files(root_dir, tables)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument("variables_url", help="The URL to the JSON variables file for the release you're processing")
    parser.add_argument("merge_url", help="The URL to the pipe-delimited basic 'table shell' file")
    parser.add_argument("root_dir", help="Path to directory to write out the resulting table and column metadata CSV files")
    args = parser.parse_args()

    main(args.root_dir, args.merge_url)
