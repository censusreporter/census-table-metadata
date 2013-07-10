'''
Processes `TableShells` xls files from the Census site to produce a new csv
with complete metadata for every column of every table. This is very similar
to the `process_merge` script in this repo, but since it uses XLS files with
more data it can give you heirarchy information for each column.

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

# Parse the Sequence_Number_And_Table_Number_Lookup.xls/merge_5_6.xls file
# so we can get the subject area and sequence number data to match up with
# the shells.
sqn_table_lookup = {}
xlsfile = open_workbook(sys.argv[2])
sheet = xlsfile.sheet_by_index(0)
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    table_id = r_data[1].value
    sqn = r_data[2].value
    subject_area = r_data[8].value.strip()

    if subject_area:
        sqn_table_lookup[table_id] = (sqn, subject_area)

filename = sys.argv[1]

xlsfile = open_workbook(filename, formatting_info=True)
sheet = xlsfile.sheet_by_index(0)

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

        sqn_data = sqn_table_lookup.get(table_id)
        if sqn_data:
            one_row['sequence_number'] = sqn_data[0]
            one_row['subject_area'] = sqn_data[1]

        # New table, so clear out the heirarchy stack
        heirarchy_stack = [None]*10
    elif not line_number and title.lower().startswith('universe:'):
        one_row['universe'] = title[11:].strip()
    elif line_number and title:
        one_row['line_number'] = line_number
        one_row['column_id'] = column_id
        one_row['column_title'] = title.encode('utf8')

        cell = sheet.cell(r, 3)
        indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level
        one_row['indent'] = indent

        heirarchy_stack[indent] = column_id
        if indent > 0:
            one_row['parent_column_id'] = heirarchy_stack[indent - 1]

        csvfile.writerow(one_row)
