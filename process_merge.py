'''
Processes the merge_5_6.xls (renamed Sequence_Number_and_Table_Number_Lookup.xls
in 2009 3yr ACS and beyond) into a CSV with metadata about each column in the dataset.

There's not enough information about heirarchy in the merge_5_6.xls files, so those
columns are left blank in the output of this script.
'''

import csv
from xlrd import open_workbook
import sys
import os

filename = sys.argv[1]

xlsfile = open_workbook(filename)
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
    one_row['table_id'] = r_data[1].value
    one_row['sequence_number'] = int(r_data[2].value)
    line_number = r_data[3].value
    position = r_data[4].value
    cells = r_data[5].value
    if r_data[7].ctype == 2:
        title = str(r_data[7].value)
    else:
        title = r_data[7].value
    subject_area = r_data[8].value

    if not line_number and cells:
        # The all-caps description of the table
        one_row['table_title'] = title.encode('utf8')
        # ... this row also includes the subject area text
        one_row['subject_area'] = subject_area
    elif not line_number and not cells and title.lower().startswith('universe:'):
        one_row['universe'] = title[11:]
    else:
        one_row['line_number'] = line_number
        one_row['column_id'] = '%s%03d' % (one_row['table_id'], line_number)
        one_row['column_title'] = title.encode('utf8')

        csvfile.writerow(one_row)
