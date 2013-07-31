census-table-metadata
=====================

Tools for generating metadata about tables and fields in a Census release
based on sequence lookup and table shell files.

### process_merge.py ###

The shell files for the 2007 and 2008 ACS releases are spread out between several
XLS files.

Processes sequence lookup files from the Census FTP site, in either csv or xls
format. To run, fetch `Sequence_Number_and_Table_Number_Lookup.xls` for the
release you want, e.g. [ftp://ftp2.census.gov/acs2011_1yr/summaryfile/](ftp://ftp2.census.gov/acs2011_1yr/summaryfile/).
(Or you could fetch the .txt version of the file and save as a .csv.)

Then run this script with two arguments:

- The -s flag gets a code for the data release. This can be whatever you like.
It's there to help you remember where the data came from, and potentially
support csv files that combine information from multiple releases.
- The -f flag gets the filepath to the `Sequence_Number` file you downloaded.

`>> python process_sequences.py -s ACS2011_1-Year -f sequence_files/file.xls`

This will create a `Table_Names_and_Subject_Areas` csv , with table names,
table IDs, table size (number of columns) and subject areas.


### process_shells.py ###

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


### taxonify.py ###

Processes the `Table_Names_and_Subject_Areas` files generated earlier by
`process_sequences`. It creates a new csv that adds custom taxonomy fields,
the mapping for which is controlled by two dicts: `SUBJECT_AREA_TO_TOPICS`
and `TABLE_NAME_TEXT_TO_TOPICS`.

Use the -f arg to pass the filepath to a `Table_Names_and_Subject_Areas` file.

`>> python taxonify.py -f generated_csv/file.csv`

After running, you may want to look through the rows and edit as necessary.
You can also use the -t arg to filter for tables within a topical area.

`>> python taxonify.py -f generated_csv/file.csv -t poverty`
`>> python taxonify.py -f generated_csv/file.csv -t "health insurance"`

This will generate a separate csv with only the tables that match the topic
you're interested in. The Census `subject_area` field is a good starting point
for getting a handle on the data available on specific subjects, but tables
often touch on multiple themes, so this can be a useful exploratory tool.