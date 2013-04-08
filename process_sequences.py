'''
Processes `Sequence_Number_and_Table_Number_Lookup` files from the Census
FTP site, in either csv or xls format. Creates a new csv with table names,
table IDs, table size (number of columns) and subject areas.

To run, fetch Sequence_Number_and_Table_Number_Lookup.xls for the release
you want, e.g. ftp://ftp2.census.gov/acs2011_1yr/summaryfile/. (Or you
could fetch the .txt version of the file and save as a .csv.)

Then run this script with two arguments:

- The -s flag gets a code for the data release. This can be whatever you like.
It's there to help you remember where the data came from, and potentially
support csv files that combine information from multiple releases.
- The -f flag gets the filepath to the `Sequence_Number` file you downloaded.

>> python process_sequences.py -s ACS2011_1-Year -f sequence_files/file.xls

This will write a `Table_Names_and_Subject_Areas` csv into `OUTPUT_DIR`,
with columns for each field in `FIELDS_FOR_CSV`.
'''
import csv, optparse, os, sys, traceback
from os.path import isdir, join, normpath
from xlrd import open_workbook, colname

from __init__ import OUTPUT_DIR

FIELDS_FOR_CSV = [
    'source',
    'table_id',
    'table_name',
    'table_size',
    'subject_area'
]

def process_csv_file(filename):
    output_rows = []
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # handle inconsistent column names in sequence files
            try:
                table_name = row['Long Table Title']
            except:
                table_name = row['Table Title']

            try:
                table_size = row['cells'].split(' ')[0]
            except:
                table_size = row['Total Cells in Table'].split(' ')[0]

            try:
                subject_area = row['subject_area']
            except:
                subject_area = row['Subject Area']

            if subject_area:
                stored_row = {
                    'source': options.source,
                    'table_id': row['Table ID'],
                    'table_name': table_name,
                    'table_size': table_size,
                    'subject_area': subject_area,
                }
                output_rows.append(stored_row)

    write_csv(filename, output_rows)

def process_xls_file(filename):
    output_rows = []
    xlsfile = open_workbook(filename)
    sheet = xlsfile.sheet_by_index(0)
    keys = sheet.row_values(0)

    for row_index in range(1, sheet.nrows):
        values = [cell.value for cell in sheet.row(row_index)]
        row = dict(zip(keys, values))
        
        # handle inconsistent column names
        try:
            table_name = row['Long Table Title']
        except:
            table_name = row['Table Title']

        try:
            table_size = row['cells'].split(' ')[0]
        except:
            table_size = row['Total Cells in Table'].split(' ')[0]
            
        try:
            subject_area = row['subject_area']
        except:
            subject_area = row['Subject Area']
            
        if subject_area:
            stored_row = {
                'source': options.source,
                'table_id': row['Table ID'],
                'table_name': table_name,
                'table_size': table_size,
                'subject_area': subject_area,
            }
            output_rows.append(stored_row)

    xlsfile.unload_sheet(0)
    write_csv(filename, output_rows)

def write_csv(filename, dict_list):
    csvfilename = os.path.basename(filename)
    csvfilename = csvfilename.replace(
        'Sequence_Number_and_Table_Number_Lookup',
        'Table_Names_and_Subject_Areas'
    ).replace('.xls','.csv')
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
        '-s', '--source',
        dest='source',
        help='source of data, e.g. ACS2011_5-Year',
    )
    parser.add_option(
        '-f', '--filename',
        dest='filename',
        help='filename of sequence file to process',
    )
    options, args = parser.parse_args(arglist)

    if not options.source:
        parser.error('please provide an -s argument naming the data source, e.g. ACS2011_5-Year')

    options.source = options.source.replace(' ','_')
        
    return options, args


def main(args=None):
    """
    >> python process_sequences.py -s ACS2011_5-Year -f sequence_files/file.xls
    """
    if args is None:
        args = sys.argv[1:]
    options, args = process_options(args)

    # make sure we have the expected directories
    for path in [OUTPUT_DIR,]:
        if not isdir(path):
            os.mkdir(path)

    filetype = options.filename.split('.')[-1]
    if filetype == 'xls':
        process_xls_file(options.filename)
    else:
        process_csv_file(options.filename)

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        sys.stderr.write('\n')
        traceback.print_exc(file=sys.stderr)
        sys.stderr.write('\n')
        sys.exit(1)