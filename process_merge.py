'''
Processes the merge_5_6.xls (renamed Sequence_Number_and_Table_Number_Lookup.xls
in 2009 3yr ACS and beyond) into a CSV with heirarchical metadata about each column
in the dataset.
'''

import csv
from xlrd import open_workbook, colname
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

heirarchy_stack = []
wrote_one_leaf_out = False

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
        next_row_indent = 0
        next_row_parent_id = None

        # The all-caps description of the table
        one_row['table_title'] = title.encode('utf8')
        # ... this row also includes the subject area text
        one_row['subject_area'] = subject_area

        # New table so clean out heirarchy stack etc.
        heirarchy_stack = []
        wrote_one_leaf_out = False
        if 'parent_column_id' in one_row:
            del one_row['parent_column_id']
    elif not line_number and not cells and title.lower().startswith('universe:'):
        one_row['universe'] = title[11:]
    else:
        one_row['line_number'] = line_number
        one_row['column_id'] = '%s%03d' % (one_row['table_id'], line_number)
        one_row['column_title'] = title.encode('utf8')

        if heirarchy_stack:
            one_row['indent'] = len(heirarchy_stack)
            one_row['parent_column_id'] = heirarchy_stack[-1]

        if title.endswith(':'):
            if wrote_one_leaf_out:
                del heirarchy_stack[-1]
                one_row['parent_column_id'] = heirarchy_stack[-1]
                print "Pop from the stack"
            heirarchy_stack.append(one_row['column_id'])
            print "Append to the stack: %s" % heirarchy_stack
        else:
            print "Wrote a leaf"
            wrote_one_leaf_out = True

        csvfile.writerow(one_row)
