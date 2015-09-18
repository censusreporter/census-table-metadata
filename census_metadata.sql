CREATE TABLE acs2007_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2007_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2007_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2007_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2007_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2007_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2007_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2007_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2008_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2008_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2008_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2008_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2008_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2008_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2008_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2008_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2009_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2009_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2009_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2009_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2009_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2009_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2009_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2009_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2010_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2010_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2010_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2010_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2010_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2010_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2010_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2010_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2010_5yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_5yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2010_5yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2010_5yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2010_5yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2011_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2011_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2011_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2011_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2011_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2011_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2011_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2011_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2011_5yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_5yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2011_5yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2011_5yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2011_5yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2012_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2012_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2012_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2012_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2012_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2012_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2012_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2012_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2012_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2012_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2012_5yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2012_5yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2012_5yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2012_5yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2012_5yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2013_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2013_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2013_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2013_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2013_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2013_3yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2013_3yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2013_3yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2013_3yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2013_3yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2013_5yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2013_5yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2013_5yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2013_5yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2013_5yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE acs2014_1yr.census_table_metadata (
    table_id varchar(10),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    topics text[],
    PRIMARY KEY (table_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2014_1yr.census_column_metadata (
    table_id varchar(10),
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON acs2014_1yr.census_table_metadata USING GIN(topics);
CREATE INDEX ON acs2014_1yr.census_table_metadata (lower(table_title) text_pattern_ops);
CREATE INDEX ON acs2014_1yr.census_column_metadata (lower(column_title) text_pattern_ops);

CREATE TABLE public.census_tabulation_metadata (
    tabulation_code varchar(6),
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    topics text[],
    weight smallint,
    tables_in_one_yr text[],
    tables_in_three_yr text[],
    tables_in_five_yr text[],
    PRIMARY KEY (tabulation_code)
)
WITH (autovacuum_enabled = FALSE);
CREATE INDEX ON public.census_tabulation_metadata USING GIN(topics);
CREATE INDEX ON public.census_tabulation_metadata (lower(table_title) text_pattern_ops);
