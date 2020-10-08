'''
Uses the CSV output from the Census API to generate census_table_metadata.csv
and census_column_metadata.csv.
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
    return map(lambda x: x.strip(), sorted(all_areas))


def find_denominator_column(table, rows):
    """For most tables, the first row is a total row, and that row is the thing to use
       to show estimates as percentages.  But a table must have at least 3 rows for
       percentages to be meaningful -- and percentages are not meaningful for
       median estimates, so sometimes we return None
    """
    if rows and len(rows) > 2 and rows[0]['column_title'].lower().startswith('total') and table and not table['table_title'].lower().startswith('median'):
        return rows[0]['column_id']
    else:
        return None

def get_vars(var_url):
    """Parse the official ACS metadata JSON for the given schema (ACS release) and return a dict
       with table IDs for keys and a list of metadata objects for each column in that table as values.
       Because this works through a list one variable at a time, it isn't able to handle pseudo-columns:
       that is, labels which have no data associated with them, but which must be managed to present
       a proper hierarchy of columns. That comes in a separate step, finish_fixing_table"""
    try:
        resp = requests.get(var_url)
        resp.raise_for_status()
        var_json = resp.json()

        var_dict = {}
        for k,v in var_json['variables'].items():
            if '_' in k and k.endswith('E'):
                v['column_id'] = k.replace('_','')[:-1]

                # reconstruct the label without leading 'Estimate'
                split_label = v['label'].split('!!')[1:]
                v['label'] = '!!'.join(split_label)

                # parent_label is used to work out parent_column_id in finish_fixing_table
                v['parent_label'] = '!!'.join(split_label[:-1])
                v['indent'] = len(split_label) - 1
                v['leaf_label'] = split_label[-1]
                v['label_parts'] = split_label
                try:
                    var_dict[v['group']].append(v)
                except KeyError:
                    var_dict[v['group']] = [ v ]
    except KeyError:
        raise Exception("Invalid schema [{}]".format(schema))
    sorted_var_dict = {}
    for k,v in var_dict.items():
        v = [(var['column_id'], var) for var in v]
        v.sort()
        sorted_var_dict[k] = [var[1] for var in v]
    return sorted_var_dict

def extract_line_number(group, column_id):
    "Construct a line number based on the column ID, using the group as a 'mask'"
    line_number_str = column_id.replace(group,'')
    line_number_str = line_number_str.lstrip('0')
    if line_number_str[0] == '.':
        line_number_str = '0{}'.format(line_number_str)
    if '.' in line_number_str: # pseudo
        return line_number_str
    return "{}.0".format(line_number_str)

def finish_fixing_table(var_list):
    """Given the complete list of real variables for a given table, from the get_vars process
        assign the parent_column_id and line_number,
        handling pseudo-header columns as well. (groupers that don't have variables)
    """
    by_label = dict((v['label'], v) for v in var_list)
    for var in var_list:
        var['line_number'] = extract_line_number(var['group'],var['column_id'])
        if var['parent_label']:
            try:
                parent = by_label[var['parent_label']]
            except KeyError: # create the parent that doesn't exist
                col_number = int(var['column_id'][-3:]) - 1
                column_id = "{}{:03}.5".format(var['group'],col_number) # create a pseudo-column ID

                label_parts = var['parent_label'].split('!!')
                parent_label = '!!'.join(label_parts[:-1])
                leaf_label = label_parts[-1]
                try:
                    parent_column_id = by_label[parent_label]['column_id']
                except KeyError:
                    parent_column_id = ''
                parent = { # preserving a number of properties we may not use for a while
                    'label': var['parent_label'],
                    'concept': var['concept'],
                    'group': var['group'],
                    'column_id': column_id,
                    'indent': var['indent'] - 1,
                    'leaf_label': leaf_label,
                    'parent_label': parent_label,
                    'label_parts': label_parts,
                    'parent_column_id': parent_column_id
                }
                parent['line_number'] = extract_line_number(parent['group'],parent['column_id'])
                by_label[parent['label']] = parent
            var['parent_column_id'] = parent['column_id']
        else:
            # must be first row?
            var['parent_column_id'] = ''

    # make sure everything is sorted correctly before returning
    new_list = [(x['column_id'], x) for x in by_label.values()]
    new_list.sort()
    return [x[1] for x in new_list]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("variables_url", help="The URL to the JSON variables file for the release you're processing")
    parser.add_argument("merge_url", help="The URL to the CSV list of sequence IDs for the ACS release you're processing")
    parser.add_argument("root_dir", help="Path to directory to write out the reulsting table and column metadata CSV files")
    args = parser.parse_args()

    # Gather the indent information from the variables URL
    raw_vars = get_vars(args.variables_url)

    # build the lookup table to augment data missing from CSV list of sequence IDs
    lookup = defaultdict(dict)

    for table_id, col_list in raw_vars.items():
        fixed_cols = finish_fixing_table(col_list)
        for col in fixed_cols:
            column_id = col['column_id']
            lookup[table_id][column_id] = {
                "column_id": column_id,
                "indent": col['indent'],
                "parent_column_id": col.get('parent_column_id','')
            }

    tables = {}
    table = {}
    rows = []
    previous_line_number = 0

    # Gather the column information from the merge CSV
    resp = requests.get(args.merge_url, stream=True)
    resp.raise_for_status()
    with closing(resp) as r:

        reader = csv.DictReader(codecs.iterdecode(r.iter_lines(), 'iso-8859-1'))
        for line in reader:

            table_id = line['Table ID']
            line_number = line['Line Number']
            cells = line['Total Cells in Table']
            title = line['Table Title'].strip()
            subject_area = line['Subject Area']

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
                table_lookup = lookup.get(table_id)

            elif not line_number and not cells and title.lower().startswith('universe:'):
                table['universe'] = titlecase(title.split(':')[-1]).strip()

            elif line_number:
                row = {}
                row['table_id'] = table['table_id']
                line_number = float(line_number)

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

                column_info = table_lookup.get(row['column_id'])
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

    with open(os.path.join(args.root_dir, "census_table_metadata.csv"), 'w') as table_file:
        table_writer = csv.DictWriter(table_file, table_metadata_fieldnames, lineterminator='\n')
        table_writer.writeheader()

        with open(os.path.join(args.root_dir, "census_column_metadata.csv"), 'w') as column_file:
            column_writer = csv.DictWriter(column_file, column_metadata_fieldnames, lineterminator='\n')
            column_writer.writeheader()

            for table_id, table in sorted(tables.items()):
                columns = table.pop('columns')
                table_writer.writerow(table)

                for column in sorted(columns, key=lambda a: a['column_id']):
                    column_writer.writerow(column)
