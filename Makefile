ACS2007_SHELLS = $(shell find acs2007_shells -type f -name '*.xls')
ACS2008_SHELLS = $(shell find acs2008_shells -type f -name '*.xls')

all: \
	precomputed/acs2007_1yr/census_table_metadata.csv \
	precomputed/acs2007_3yr/census_table_metadata.csv \
	precomputed/acs2008_1yr/census_table_metadata.csv \
	precomputed/acs2008_3yr/census_table_metadata.csv \
	precomputed/acs2009_1yr/census_table_metadata.csv \
	precomputed/acs2009_3yr/census_table_metadata.csv \
	precomputed/acs2010_1yr/census_table_metadata.csv \
	precomputed/acs2010_3yr/census_table_metadata.csv \
	precomputed/acs2010_5yr/census_table_metadata.csv \
	precomputed/acs2011_1yr/census_table_metadata.csv \
	precomputed/acs2011_3yr/census_table_metadata.csv \
	precomputed/acs2011_5yr/census_table_metadata.csv

clean:
	rm -rf acs2007_shells/ \
		acs2008_shells/ \
		precomputed/ \
		acs2007_1yr_merge_5_6.xls \
		acs2007_3yr_merge_5_6.xls \
		acs2008_1yr_merge_5_6.xls \
		acs2008_3yr_merge_5_6.xls \
		acs2009_1yr_merge_5_6.xls \
		acs2009_1yr_table_shells.xls \
		acs2009_3yr_merge_5_6.xls \
		acs2009_3yr_table_shells.xls \
		acs2010_1yr_merge_5_6.xls \
		acs2010_1yr_table_shells.xls \
		acs2010_3yr_merge_5_6.xls \
		acs2010_3yr_table_shells.xls \
		acs2010_5yr_merge_5_6.xls \
		acs2010_5yr_table_shells.xls \
		acs2011_1yr_merge_5_6.xls \
		acs2011_1yr_table_shells.xls \
		acs2011_3yr_merge_5_6.xls \
		acs2011_3yr_table_shells.xls \
		acs2011_5yr_merge_5_6.xls \
		acs2011_5yr_table_shells.xls

acs2007_shells/:
	mkdir acs2007_shells
	wget -q "http://www2.census.gov/acs/downloads/shells/2007/Detailed_Tables/" --no-parent --accept="*.xls" --recursive -nH --cut-dirs=5 -P acs2007_shells
	rm -f acs2007_shells/robots.txt
	# CENNSSUUUSS!!
	mv "acs2007_shells/B19113 .xls" "acs2007_shells/B19113.xls"

acs2007_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2007_1yr/summaryfile/merge_5_6_final.xls" -o acs2007_1yr_merge_5_6.xls

acs2008_shells/:
	mkdir acs2008_shells
	wget -q "http://www2.census.gov/acs/downloads/shells/2008/Detailed_Tables/" --no-parent --accept="*.xls" --recursive -nH --cut-dirs=5 -P acs2008_shells
	rm -f acs2008_shells/robots.txt

acs2007_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2007_3yr/summaryfile/merge_5_6_final.xls" -o acs2007_3yr_merge_5_6.xls

acs2008_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2008_1yr/summaryfile/merge_5_6.xls" -o acs2008_1yr_merge_5_6.xls

acs2008_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2008_3yr/summaryfile/merge_5_6.xls" -o acs2008_3yr_merge_5_6.xls

acs2009_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2009_1yr/summaryfile/merge_5_6.xls" -o acs2009_1yr_merge_5_6.xls
acs2009_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2009_1yr/summaryfile/ACS2009TableShells.xls" -o acs2009_1yr_table_shells.xls

acs2009_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2009_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2009_3yr_merge_5_6.xls
acs2009_3yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2009_3yr/summaryfile/ACS2009_3-Year_TableShells.xls" -o acs2009_3yr_table_shells.xls

acs2010_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2010_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2010_1yr_merge_5_6.xls
acs2010_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2010_1yr/summaryfile/ACS2010_1-Year_TableShells.xls" -o acs2010_1yr_table_shells.xls

acs2010_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2010_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2010_3yr_merge_5_6.xls
acs2010_3yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2010_3yr/summaryfile/ACS2010_3-Year_TableShells.xls" -o acs2010_3yr_table_shells.xls

acs2010_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2010_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2010_5yr_merge_5_6.xls
acs2010_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2010_5yr/summaryfile/ACS2010_5-Year_TableShells.xls" -o acs2010_5yr_table_shells.xls

acs2011_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2011_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2011_1yr_merge_5_6.xls
acs2011_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2011_1yr/summaryfile/ACS2011_1-Year_TableShells.xls" -o acs2011_1yr_table_shells.xls

acs2011_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2011_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2011_3yr_merge_5_6.xls
acs2011_3yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2011_3yr/summaryfile/ACS2011_3-Year_TableShells.xls" -o acs2011_3yr_table_shells.xls

acs2011_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2011_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2011_5yr_merge_5_6.xls
acs2011_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2011_5yr/summaryfile/ACS2011_5-Year_TableShells.xls" -o acs2011_5yr_table_shells.xls

precomputed/acs2007_1yr/census_table_metadata.csv: acs2007_1yr_merge_5_6.xls acs2007_shells/
	python process_merge.py acs2007_1yr_merge_5_6.xls acs2007_shells
	mkdir -p precomputed/acs2007_1yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2007_1yr/

precomputed/acs2007_3yr/census_table_metadata.csv: acs2007_3yr_merge_5_6.xls acs2007_shells/
	python process_merge.py acs2007_3yr_merge_5_6.xls acs2007_shells
	mkdir -p precomputed/acs2007_3yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2007_3yr/

precomputed/acs2008_1yr/census_table_metadata.csv: acs2008_1yr_merge_5_6.xls acs2008_shells/
	python process_merge.py acs2008_1yr_merge_5_6.xls acs2008_shells
	mkdir -p precomputed/acs2008_1yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2008_1yr/

precomputed/acs2008_3yr/census_table_metadata.csv: acs2008_3yr_merge_5_6.xls acs2008_shells/
	python process_merge.py acs2008_3yr_merge_5_6.xls acs2008_shells
	mkdir -p precomputed/acs2008_3yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2008_3yr/

precomputed/acs2009_1yr/census_table_metadata.csv: acs2009_1yr_merge_5_6.xls acs2009_1yr_table_shells.xls
	python process_shells.py acs2009_1yr_table_shells.xls acs2009_1yr_merge_5_6.xls
	mkdir -p precomputed/acs2009_1yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2009_1yr/

precomputed/acs2009_3yr/census_table_metadata.csv: acs2009_3yr_merge_5_6.xls acs2009_3yr_table_shells.xls
	python process_shells.py acs2009_3yr_table_shells.xls acs2009_3yr_merge_5_6.xls
	mkdir -p precomputed/acs2009_3yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2009_3yr/

precomputed/acs2010_1yr/census_table_metadata.csv: acs2010_1yr_merge_5_6.xls acs2010_1yr_table_shells.xls
	python process_shells.py acs2010_1yr_table_shells.xls acs2010_1yr_merge_5_6.xls
	mkdir -p precomputed/acs2010_1yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2010_1yr/

precomputed/acs2010_3yr/census_table_metadata.csv: acs2010_3yr_merge_5_6.xls acs2010_3yr_table_shells.xls
	python process_shells.py acs2010_3yr_table_shells.xls acs2010_3yr_merge_5_6.xls
	mkdir -p precomputed/acs2010_3yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2010_3yr/

precomputed/acs2010_5yr/census_table_metadata.csv: acs2010_5yr_merge_5_6.xls acs2010_5yr_table_shells.xls
	python process_shells.py acs2010_5yr_table_shells.xls acs2010_5yr_merge_5_6.xls
	mkdir -p precomputed/acs2010_5yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2010_5yr/

precomputed/acs2011_1yr/census_table_metadata.csv: acs2011_1yr_merge_5_6.xls acs2011_1yr_table_shells.xls
	python process_shells.py acs2011_1yr_table_shells.xls acs2011_1yr_merge_5_6.xls
	mkdir -p precomputed/acs2011_1yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2011_1yr/

precomputed/acs2011_3yr/census_table_metadata.csv: acs2011_3yr_merge_5_6.xls acs2011_3yr_table_shells.xls
	python process_shells.py acs2011_3yr_table_shells.xls acs2011_3yr_merge_5_6.xls
	mkdir -p precomputed/acs2011_3yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2011_3yr/

precomputed/acs2011_5yr/census_table_metadata.csv: acs2011_5yr_merge_5_6.xls acs2011_5yr_table_shells.xls
	python process_shells.py acs2011_5yr_table_shells.xls acs2011_5yr_merge_5_6.xls
	mkdir -p precomputed/acs2011_5yr/
	mv census_column_metadata.csv census_table_metadata.csv census_table_topics.csv census_topics.csv precomputed/acs2011_5yr/
