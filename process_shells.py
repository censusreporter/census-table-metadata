'''
Processes `TableShells` xls files from the Census site to produce a new csv
with complete metadata for every column of every table. This is very similar
to the `process_merge` script in this repo, but since it uses XLS files with
more data it can give you heirarchy information for each column.

To run, first download a `TableShells.xls` file from e.g.
http://www2.census.gov/acs2009_1yr/summaryfile/

Then run this script with a single argument for the filename of the `TableShells`
file you downloaded.

>> python process_shells.py ACS2009TableShells.xls

This will write a `metadata` csv alongside the `TableShells` file with information
about each column in each table.
'''
import csv, os, sys, traceback
from os.path import isdir, join, normpath
from xlrd import open_workbook

filename = sys.argv[1]

xlsfile = open_workbook(filename, formatting_info=True)
sheet = xlsfile.sheet_by_index(0)
keys = sheet.row_values(0)

fieldnames = [
    'table_id',
    'sequence_number',
    'line_number',
    'column_id',
    'subject_area',
    'table_title',
    'universe',
    'column_title',
    'indent',
    'parent_column_id'
]

csvfilename = "%s/merge_heirarchy.csv" % os.path.dirname(filename)
csvfile = csv.DictWriter(open(csvfilename, 'w'), fieldnames)
csvfile.writeheader()

one_row = dict()
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    one_row['table_id'] = r_data[0].value
    line_number = r_data[1].value
    column_id = r_data[2].value
    if r_data[3].ctype == 2:
        title = str(r_data[3].value)
    else:
        title = r_data[3].value

    if not line_number and title and title.isupper():
        # The all-caps description of the table
        one_row['table_title'] = title.encode('utf8')

        # New table, so clear out the heirarchy stack
        heirarchy_stack = []
    elif not line_number and title.lower().startswith('universe:'):
        one_row['universe'] = title[11:]
    else:
        one_row['line_number'] = line_number
        one_row['column_id'] = column_id
        one_row['column_title'] = title.encode('utf8')

        cell = sheet.cell(row_index, 3)
        indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level
        one_row['indent'] = indent

        heirarchy_stack[indent] = column_id
        if indent > 0:
            one_row['parent_column_id'] = heirarchy_stack[indent - 1]

        csvfile.writerow(one_row)
