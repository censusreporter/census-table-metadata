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


def read_shell(table_id):

    if table_id.endswith('PR'):
        table_id = table_id[:-2]
    if table_id.startswith('C'):
        table_id = 'B%s' % table_id[1:]

    lookup = {}
    heirarchy_stack = [None]*10
    try:
        xlsfile = open_workbook('%s/%s.xls' % (sys.argv[2], table_id), formatting_info=True)
    except IOError, e:
        if e.errno == 2:
            print "Missing table %s/%s.xls" % (sys.argv[2], table_id)
            return lookup
    sheet = xlsfile.sheet_by_index(0)
    for r in range(1, sheet.nrows):
        r_data = sheet.row(r)

        table_id = r_data[0].value.strip()
        line_number = r_data[1].value

        if table_id and line_number and r_data[1].ctype == 2:
            line_number_str = str(line_number)
            if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
                # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
                column_id = "%s%05.1f" % (table_id, line_number)
            else:
                column_id = "%s%03d" % (table_id, line_number)

            cell = sheet.cell(r, 2)
            indent = xlsfile.xf_list[cell.xf_index].alignment.indent_level

            heirarchy_stack[indent] = column_id
            parent_column_id = None
            if indent > 0:
                parent_column_id = heirarchy_stack[indent - 1]

                # Sometimes the parent is actually 2 levels up for some reason
                if not parent_column_id:
                    parent_column_id = heirarchy_stack[indent - 2]

            lookup[column_id] = {
                "indent": indent,
                "parent_column_id": parent_column_id
            }

    return lookup

xlsfile = open_workbook(filename)
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

external_shell_lookup = {}

one_row = dict()
for r in range(1, sheet.nrows):
    r_data = sheet.row(r)

    # The column names seem to change between releases but their order doesn't
    one_row['table_id'] = r_data[1].value.strip()
    one_row['sequence_number'] = int(r_data[2].value)
    line_number = r_data[3].value
    position = r_data[4].value
    cells = r_data[5].value
    if r_data[7].ctype == 2:
        title = str(r_data[7].value)
    else:
        title = r_data[7].value
    title = title.strip()
    subject_area = r_data[8].value

    if not line_number and cells:
        # The all-caps description of the table
        one_row['table_title'] = title.encode('utf8')
        # ... this row also includes the subject area text
        one_row['subject_area'] = subject_area.strip()

        external_shell_lookup = read_shell(one_row['table_id'])
    elif not line_number and not cells and title.lower().startswith('universe:'):
        one_row['universe'] = title[11:].strip()
    elif line_number:
        one_row['line_number'] = line_number

        line_number_str = str(line_number)
        if line_number_str.endswith('.7') or line_number_str.endswith('.5'):
            # This is a subhead (not an actual data column), so we'll have to synthesize a column_id
            one_row['column_id'] = "%s%05.1f" % (one_row['table_id'], line_number)
        else:
            one_row['column_id'] = '%s%03d' % (one_row['table_id'], line_number)
        one_row['column_title'] = title.encode('utf8')

        column_info = external_shell_lookup.get(one_row['column_id'])
        if column_info:
            one_row['indent'] = column_info['indent']
            one_row['parent_column_id'] = column_info['parent_column_id']

        csvfile.writerow(one_row)
