CREATE TABLE acs2007_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2007_1yr.census_table_metadata FROM '/home/ubuntu/ACS2007_1-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2007_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2007_3yr.census_table_metadata FROM '/home/ubuntu/ACS2007_3-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2008_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2008_1yr.census_table_metadata FROM '/home/ubuntu/ACS2008_1-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2008_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2008_3yr.census_table_metadata FROM '/home/ubuntu/ACS2008_3-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2009_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2009_1yr.census_table_metadata FROM '/home/ubuntu/ACS2009_1-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2009_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2009_3yr.census_table_metadata FROM '/home/ubuntu/ACS2009_3-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2010_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2010_1yr.census_table_metadata FROM '/home/ubuntu/ACS2010_1-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2010_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2010_3yr.census_table_metadata FROM '/home/ubuntu/ACS2010_3-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2010_5yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2010_5yr.census_table_metadata FROM '/home/ubuntu/ACS2010_5-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2011_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2011_1yr.census_table_metadata FROM '/home/ubuntu/ACS2011_1-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2011_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2011_3yr.census_table_metadata FROM '/home/ubuntu/ACS2011_3-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

CREATE TABLE acs2011_5yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    subject_area text,
    table_title text,
    universe text,
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number, line_number)
)
WITH (autovacuum_enabled = FALSE, toast.autovacuum_enabled = FALSE);
COPY acs2011_5yr.census_table_metadata FROM '/home/ubuntu/ACS2011_5-Year_merge_hierarchy.csv' WITH csv ENCODING 'utf8' HEADER;

