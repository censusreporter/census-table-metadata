census-table-metadata
=====================

Tools for generating metadata about tables and fields in a Census release
based on sequence lookup and table shell files.

### Usage ###

You can use the CSV files inside the `precomputed` directory or build them
yourself with the `make` command:

Set up a virtualenv with the requirements and then run `make`. You'll end up
with the ACS table metadata downloaded and parsed into CSV appropriate for
loading in to a PostgreSQL schema:

```
mkvirtualenv --no-site-packages census-table
pip install -r requirements.txt
make
```

Look in the `precomputed` directory for the resulting CSV. It's useful in this
form, but is designed to be inserted into a PostgreSQL database with the schema
defined in `census_metadata.sql`.

A PostgreSQL loading script can be found in `census_metadata_load.sql`.

### process_merge.py ###

Processes the merge_5_6.xls from 2007 and 2008 vintage ACS releases into a CSV
with metadata about each column in the dataset.

There's not enough information about hierarchy in the merge_5_6.xls files, so the
second argument is the base directory containing the shell files for each table
as found in [on the Census website](http://www2.census.gov/acs/downloads/shells/2007/Detailed_Tables/).

Run as follows:
    python process_merge.py acs2007_1yr_merge_5_6.xls acs2007_shells

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
