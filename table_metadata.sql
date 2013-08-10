CREATE TABLE acs2007_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_1yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_1yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_1yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2007_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_3yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_3yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2007_3yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2008_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_1yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_1yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_1yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2008_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_3yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_3yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2008_3yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2009_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_1yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_1yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_1yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2009_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_3yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_3yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2009_3yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2010_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_1yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_1yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_1yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2010_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_3yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_3yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_3yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2010_5yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_5yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_5yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2010_5yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2011_1yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_1yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_1yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_1yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2011_3yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_3yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_3yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_3yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);

CREATE TABLE acs2011_5yr.census_table_metadata (
    table_id varchar(10),
    sequence_number smallint,
    table_title text,
    simple_table_title text,
    subject_area text,
    universe text,
    denominator_column_id varchar(16),
    PRIMARY KEY (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_5yr.census_topics (
    topic_id smallint,
    topic text,
    PRIMARY KEY (topic_id),
    UNIQUE (topic)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_5yr.census_table_topics (
    table_id varchar(10),
    sequence_number smallint,
    topic_id smallint,
    PRIMARY KEY (table_id, sequence_number),
    FOREIGN KEY (topic_id) REFERENCES census_topics (topic_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);
CREATE TABLE acs2011_5yr.census_column_metadata (
    table_id varchar(10),
    sequence_number smallint,
    line_number numeric(4,1),
    column_id varchar(16),
    column_title text,
    indent smallint,
    parent_column_id varchar(16),
    PRIMARY KEY (column_id),
    FOREIGN KEY (table_id, sequence_number) REFERENCES census_table_metadata (table_id, sequence_number)
)
WITH (autovacuum_enabled = FALSE);