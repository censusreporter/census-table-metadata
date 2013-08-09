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
            column_csv.writerows(rows)
            table = {}
            rows = []

        # The all-caps description of the table
        table['table_title'] = title.encode('utf8')

        table['table_id'] = table_id
        sqn_data = sqn_table_lookup.get(table['table_id'])
        if sqn_data:
            table['sequence_number'] = sqn_data[0]
            table['subject_area'] = sqn_data[1]
    elif not line_number and title.lower().startswith('universe:'):
        # TODO Need to be better about this split here
        table['universe'] = title[11:]
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
