'''
Processes the `Table_Names_and_Subject_Areas` files generated earlier by
`process_sequences`. It creates a new csv that adds custom taxonomy fields,
the mapping for which is controlled by two dicts: `SUBJECT_AREA_TO_TOPICS`
and `TABLE_NAME_TEXT_TO_TOPICS`.

Use the -f arg to pass the filepath to a `Table_Names_and_Subject_Areas` file.

>> python taxonify.py -f generated_csv/file.csv

After running, you may want to look through the rows and edit as necessary.
You can also use the -t arg to filter for tables within a topical area.

>> python taxonify.py -f generated_csv/file.csv -t poverty

This will generate a separate csv with only the tables that match the topic
you're interested in. The Census `subject_area` field is a good starting point
for getting a handle on the data available on specific subjects, but tables
often touch on multiple themes, so this can be a useful exploratory tool.
'''
import csv, optparse, os, sys, traceback
from os.path import isdir, join, normpath

OUTPUT_DIR = 'taxonified'

FIELDS_FOR_CSV = [
    'table_id',
    'topics',
    'facets',
    'table_name',
    'table_size',
    'source',
    'subject_area'
]

SUBJECT_AREA_TO_TOPICS = {
    'Age-Sex': 'age, gender',
    'Hispanic Origin': 'race',
    'Race': 'race',

    'Earnings': 'income',
    'Employment Status': 'employment',
    'Health Insurance': 'health insurance',
    'Income': 'income',
    'Industry-Occupation-Class of Worker': 'employment',
    'Journey to Work': 'employment, transportation',
    'Poverty': 'poverty',
    'Transfer Programs': 'public assistance',

    'Ancestry': 'ancestry',
    'Children - Relationship': 'children',
    'Disability': 'disability',
    'Educational Attainment': 'education',
    'Fertility': 'fertility',
    'Foreign Birth': 'place of birth',
    'Grand(Persons) - Age of HH Members': 'children, grandparents',
    'Households - Families': 'households, families',
    'Language': 'language',
    'Marital Status': 'marital status',
    'Place of Birth - Native': 'place of birth',
    'Residence Last Year - Migration': 'migration',
    'School Enrollment': 'education',
    'Veteran Status': 'veterans',

    'Housing': 'housing',
}

THEMES_TO_TOPICS = {
    'Demographic characteristics': 'age, gender, race',

    'Economic characteristics': 'employment, income, health insurance, poverty, public assistance, transportation',

    'Social characteristics': 'ancestry, children, disability, education, families, fertility, grandparents, households, language, marital status, migration, place of birth, veterans',

    'Housing characteristics': 'housing',
}

TABLE_NAME_TEXT_TO_TOPICS = {
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
    'living arrange': 'housing',
    'household': 'households',
    'earnings': 'income',
    'income': 'income',
    'geographical mobility': 'migration',
    'poverty': 'poverty',
    'food stamps': 'public assistance',
    'public assistance': 'public assistance',
    '65 years and over': 'seniors',
    'transportation': 'transportation',
    'va health care': 'veterans',
    'veteran': 'veterans',
}

TABLE_NAME_TEXT_TO_FACETS = {
    'by age': 'age',
    'age by': 'age',
    'citizenship': 'citizenship',
    'naturalization': 'citizenship',
    'by famil': 'family type',
    'by sex': 'gender',
    'sex by': 'gender',
    'by household': 'household type',
    'household type by': 'household type',
    'language': 'language',
    'marriage': 'marital status',
    'marital': 'marital status',
    'nativity': 'place of birth',
    'place of birth': 'place of birth',
    'by relationship': 'relationship type',
    '(white': 'race',
    '(black': 'race',
    '(american': 'race',
    '(asian': 'race',
    '(native': 'race',
    '(some other race': 'race',
    '(two or more races': 'race',
    'hispanic': 'race',
}

def process_csv_file(filename):
    output_rows = []
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            table_name = row['table_name']
            subject_area = row['subject_area']
            row['topics'] = []
            row['facets'] = []
            stored_row = None

            if subject_area in SUBJECT_AREA_TO_TOPICS:
                # only keep the rows in the subject areas we want
                stored_row = row
                stored_row['topics'].extend(
                    [topic.strip() for topic in SUBJECT_AREA_TO_TOPICS[subject_area].split(',')]
                )
                
            if stored_row:
                for key in TABLE_NAME_TEXT_TO_TOPICS:
                    if key in row['table_name'].lower():
                        stored_row['topics'].extend(
                            [topic.strip() for topic in TABLE_NAME_TEXT_TO_TOPICS[key].split(',')]
                        )
                        
                for key in TABLE_NAME_TEXT_TO_FACETS:
                    if key in row['table_name'].lower():
                        stored_row['facets'].extend(
                            [facet.strip() for facet in TABLE_NAME_TEXT_TO_FACETS[key].split(',')]
                        )

                # if it's a topic, it shouldn't be a facet
                for topic in stored_row['topics']:
                    if topic in stored_row['facets']:
                        stored_row['facets'].remove(topic)
                
                stored_row['topics'] = ', '.join(sorted(set(stored_row['topics'])))
                stored_row['facets'] = ', '.join(sorted(set(stored_row['facets'])))
                
                if not options.topic or (options.topic in stored_row['topics']):
                    output_rows.append(stored_row)

    write_csv(filename, output_rows)


def write_csv(filename, dict_list):
    csvfilename = os.path.basename(filename)
    csvfilename = csvfilename.replace(
        'Table_Names_and_Subject_Areas',
        'Tables_and_Taxonomy'
    )
    if options.topic:
        csvfilename = csvfilename.replace(
            '.csv',
            '_%s.csv' % options.topic.replace(' ','_')
        )
    csvpath = normpath(join(OUTPUT_DIR, csvfilename))

    print "Writing: " + csvpath + " ...\n"

    with open(csvpath,'wb') as csvfile:
        csvwriter = csv.DictWriter(
            csvfile,
            FIELDS_FOR_CSV,
            extrasaction='ignore',
            quoting=csv.QUOTE_ALL
        )
        csvwriter.writeheader()
        for item in dict_list:
            csvwriter.writerow(item)

def process_options(arglist=None):
    global options, args
    parser = optparse.OptionParser()
    parser.add_option(
        '-f', '--filename',
        dest='filename',
        help='filename of file to process',
    )
    parser.add_option(
        '-t', '--topic',
        dest='topic',
        help='specific topic to filter for',
    )
    options, args = parser.parse_args(arglist)
    return options, args


def main(args=None):
    """
    >> python taxonify.py -f generated_csv/file.csv
    """
    if args is None:
        args = sys.argv[1:]
    options, args = process_options(args)

    # make sure we have the expected directories
    for path in [OUTPUT_DIR,]:
        if not isdir(path):
            os.mkdir(path)

    process_csv_file(options.filename)


if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        sys.stderr.write('\n')
        traceback.print_exc(file=sys.stderr)
        sys.stderr.write('\n')
        sys.exit(1)