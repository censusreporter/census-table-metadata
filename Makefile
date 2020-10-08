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
	precomputed/acs2011_5yr/census_table_metadata.csv \
	precomputed/acs2012_1yr/census_table_metadata.csv \
	precomputed/acs2012_3yr/census_table_metadata.csv \
	precomputed/acs2012_5yr/census_table_metadata.csv \
	precomputed/acs2013_1yr/census_table_metadata.csv \
	precomputed/acs2013_3yr/census_table_metadata.csv \
	precomputed/acs2013_5yr/census_table_metadata.csv \
	precomputed/acs2014_1yr/census_table_metadata.csv \
	precomputed/acs2014_5yr/census_table_metadata.csv \
	precomputed/acs2015_1yr/census_table_metadata.csv \
	precomputed/acs2015_5yr/census_table_metadata.csv \
	precomputed/acs2016_1yr/census_table_metadata.csv \
	precomputed/acs2016_5yr/census_table_metadata.csv \
	precomputed/acs2017_1yr/census_table_metadata.csv \
	precomputed/acs2017_5yr/census_table_metadata.csv \
	precomputed/acs2018_1yr/census_table_metadata.csv \
	precomputed/acs2018_5yr/census_table_metadata.csv \
	precomputed/acs2019_1yr/census_table_metadata.csv

clean:
	rm -rf precomputed/

clean-all: clean
	rm -rf acs2007_shells/ \
		acs2008_shells/ \
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
		acs2011_5yr_table_shells.xls \
		acs2012_1yr_merge_5_6.xls \
		acs2012_1yr_table_shells.xls \
		acs2012_3yr_merge_5_6.xls \
		acs2012_3yr_table_shells.xls \
		acs2012_5yr_merge_5_6.xls \
		acs2012_5yr_table_shells.xls \
		acs2013_1yr_merge_5_6.xls \
		acs2013_1yr_table_shells.xls \
		acs2013_3yr_merge_5_6.xls \
		acs2013_3yr_table_shells.xls \
		acs2013_5yr_merge_5_6.xls \
		acs2013_5yr_table_shells.xls \
		acs2014_1yr_merge_5_6.xls \
		acs2014_1yr_table_shells.xls \
		acs2014_5yr_merge_5_6.xls \
		acs2014_5yr_table_shells.xls \
		acs2015_1yr_merge_5_6.xls \
		acs2015_1yr_table_shells.xls \
		acs2015_5yr_merge_5_6.xls \
		acs2015_5yr_table_shells.xls \
		acs2016_1yr_merge_5_6.xls \
		acs2016_1yr_table_shells.xls \
		acs2016_5yr_merge_5_6.xls \
		acs2016_5yr_table_shells.xls \
		acs2017_1yr_merge_5_6.xls \
		acs2017_1yr_table_shells.xls \
		acs2017_5yr_merge_5_6.xls \
		acs2017_5yr_table_shells.xls \
		acs2018_table_shells.xls \
		acs2018_1yr_merge_5_6.xls \
		acs2018_5yr_merge_5_6.xls

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

acs2012_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2012_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2012_1yr_merge_5_6.xls
acs2012_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2012_1yr/summaryfile/ACS2012_1-Year_TableShells.xls" -o acs2012_1yr_table_shells.xls

acs2012_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2012_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2012_3yr_merge_5_6.xls
acs2012_3yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2012_3yr/summaryfile/ACS2012_3-Year_TableShells.xls" -o acs2012_3yr_table_shells.xls

acs2012_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2012_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2012_5yr_merge_5_6.xls
acs2012_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2012_5yr/summaryfile/ACS2012_5-Year_TableShells.xls" -o acs2012_5yr_table_shells.xls

acs2013_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2013_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2013_1yr_merge_5_6.xls
acs2013_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2013_1yr/summaryfile/ACS2013_1-Year_TableShells.xls" -o acs2013_1yr_table_shells.xls

acs2013_3yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2013_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2013_3yr_merge_5_6.xls
acs2013_3yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2013_3yr/summaryfile/ACS2013_3-Year_TableShells.xls" -o acs2013_3yr_table_shells.xls

acs2013_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/acs2013_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -o acs2013_5yr_merge_5_6.xls
acs2013_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/acs2013_5yr/summaryfile/ACS2013_TableShells.xls" -o acs2013_5yr_table_shells.xls

acs2014_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.xls" -o acs2014_1yr_merge_5_6.xls
acs2014_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS2014_Table_Shells.xlsx" -o acs2014_1yr_table_shells.xls

acs2014_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS_5yr_Seq_Table_Number_Lookup.xls" -o acs2014_5yr_merge_5_6.xls
acs2014_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2014/documentation/user_tools/ACS2014_Table_Shells.xlsx" -o acs2014_5yr_table_shells.xls

acs2015_1yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.xls" -o acs2015_1yr_merge_5_6.xls
acs2015_1yr_table_shells.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS2015_Table_Shells.xlsx" -o acs2015_1yr_table_shells.xls

acs2015_5yr_merge_5_6.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS_5yr_Seq_Table_Number_Lookup.xls" -o acs2015_5yr_merge_5_6.xls
acs2015_5yr_table_shells.xls:
	curl -f "http://www2.census.gov/programs-surveys/acs/summary_file/2015/documentation/user_tools/ACS2015_Table_Shells.xlsx" -o acs2015_5yr_table_shells.xls

acs2016_1yr_merge_5_6.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.xls" -o acs2016_1yr_merge_5_6.xls
acs2016_1yr_table_shells.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS2016_Table_Shells.xlsx" -o acs2016_1yr_table_shells.xls

acs2016_5yr_merge_5_6.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS_5yr_Seq_Table_Number_Lookup.xls" -o acs2016_5yr_merge_5_6.xls
acs2016_5yr_table_shells.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2016/documentation/user_tools/ACS2016_Table_Shells.xlsx" -o acs2016_5yr_table_shells.xls

acs2017_1yr_merge_5_6.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.xls" -o acs2017_1yr_merge_5_6.xls
acs2017_1yr_table_shells.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS2017_Table_Shells.xlsx" -o acs2017_1yr_table_shells.xls

acs2017_5yr_merge_5_6.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS_5yr_Seq_Table_Number_Lookup.xls" -o acs2017_5yr_merge_5_6.xls
acs2017_5yr_table_shells.xls:
	curl -f "https://www2.census.gov/programs-surveys/acs/summary_file/2017/documentation/user_tools/ACS2017_Table_Shells.xlsx" -o acs2017_5yr_table_shells.xls

acs2018_table_shells.xls:
	curl -fs "https://www2.census.gov/programs-surveys/acs/summary_file/2018/documentation/user_tools/ACS2018_Table_Shells.xlsx" -o acs2018_table_shells.xls
acs2018_1yr_merge_5_6.xls:
	# The Census doesn't have a 2018 1yr XLS file at this time, so I manually converted this CSV to XLS with Excel.
	curl -fs "https://www2.census.gov/programs-surveys/acs/summary_file/2018/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.csv" -o acs2018_1yr_merge_5_6.csv
	echo "You need to manually convert the .csv to .xls to continue"
acs2018_5yr_merge_5_6.xls:
	# The Census doesn't have a 2018 5yr XLS file at this time, so I manually converted this CSV to XLS with Excel.
	curl -fs "https://www2.census.gov/programs-surveys/acs/summary_file/2018/documentation/user_tools/ACS_5yr_Seq_Table_Number_Lookup.csv" -o acs2018_5yr_merge_5_6.csv
	echo "You need to manually convert the .csv to .xls to continue"

precomputed/acs2007_1yr/census_table_metadata.csv: acs2007_1yr_merge_5_6.xls acs2007_shells/
	python process_merge.py acs2007_1yr_merge_5_6.xls acs2007_shells
	mkdir -p precomputed/acs2007_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2007_1yr/

precomputed/acs2007_3yr/census_table_metadata.csv: acs2007_3yr_merge_5_6.xls acs2007_shells/
	python process_merge.py acs2007_3yr_merge_5_6.xls acs2007_shells
	mkdir -p precomputed/acs2007_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2007_3yr/

precomputed/acs2008_1yr/census_table_metadata.csv: acs2008_1yr_merge_5_6.xls acs2008_shells/
	python process_merge.py acs2008_1yr_merge_5_6.xls acs2008_shells
	mkdir -p precomputed/acs2008_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2008_1yr/

precomputed/acs2008_3yr/census_table_metadata.csv: acs2008_3yr_merge_5_6.xls acs2008_shells/
	python process_merge.py acs2008_3yr_merge_5_6.xls acs2008_shells
	mkdir -p precomputed/acs2008_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2008_3yr/

precomputed/acs2009_1yr/census_table_metadata.csv: acs2009_1yr_merge_5_6.xls acs2009_1yr_table_shells.xls
	python process_merge.py acs2009_1yr_merge_5_6.xls acs2009_1yr_table_shells.xls
	mkdir -p precomputed/acs2009_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2009_1yr/

precomputed/acs2009_3yr/census_table_metadata.csv: acs2009_3yr_merge_5_6.xls acs2009_3yr_table_shells.xls
	python process_merge.py acs2009_3yr_merge_5_6.xls acs2009_3yr_table_shells.xls
	mkdir -p precomputed/acs2009_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2009_3yr/

precomputed/acs2010_1yr/census_table_metadata.csv: acs2010_1yr_merge_5_6.xls acs2010_1yr_table_shells.xls
	python process_merge.py acs2010_1yr_merge_5_6.xls acs2010_1yr_table_shells.xls
	mkdir -p precomputed/acs2010_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2010_1yr/

precomputed/acs2010_3yr/census_table_metadata.csv: acs2010_3yr_merge_5_6.xls acs2010_3yr_table_shells.xls
	python process_merge.py acs2010_3yr_merge_5_6.xls acs2010_3yr_table_shells.xls
	mkdir -p precomputed/acs2010_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2010_3yr/

precomputed/acs2010_5yr/census_table_metadata.csv: acs2010_5yr_merge_5_6.xls acs2010_5yr_table_shells.xls
	python process_merge.py acs2010_5yr_merge_5_6.xls acs2010_5yr_table_shells.xls
	mkdir -p precomputed/acs2010_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2010_5yr/

precomputed/acs2011_1yr/census_table_metadata.csv: acs2011_1yr_merge_5_6.xls acs2011_1yr_table_shells.xls
	python process_merge.py acs2011_1yr_merge_5_6.xls acs2011_1yr_table_shells.xls
	mkdir -p precomputed/acs2011_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2011_1yr/

precomputed/acs2011_3yr/census_table_metadata.csv: acs2011_3yr_merge_5_6.xls acs2011_3yr_table_shells.xls
	python process_merge.py acs2011_3yr_merge_5_6.xls acs2011_3yr_table_shells.xls
	mkdir -p precomputed/acs2011_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2011_3yr/

precomputed/acs2011_5yr/census_table_metadata.csv: acs2011_5yr_merge_5_6.xls acs2011_5yr_table_shells.xls
	python process_merge.py acs2011_5yr_merge_5_6.xls acs2011_5yr_table_shells.xls
	mkdir -p precomputed/acs2011_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2011_5yr/

precomputed/acs2012_1yr/census_table_metadata.csv: acs2012_1yr_merge_5_6.xls acs2012_1yr_table_shells.xls
	python process_merge.py acs2012_1yr_merge_5_6.xls acs2012_1yr_table_shells.xls
	mkdir -p precomputed/acs2012_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2012_1yr/

precomputed/acs2012_3yr/census_table_metadata.csv: acs2012_3yr_merge_5_6.xls acs2012_3yr_table_shells.xls
	python process_merge.py acs2012_3yr_merge_5_6.xls acs2012_3yr_table_shells.xls
	mkdir -p precomputed/acs2012_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2012_3yr/

precomputed/acs2012_5yr/census_table_metadata.csv: acs2012_5yr_merge_5_6.xls acs2012_5yr_table_shells.xls
	python process_merge.py acs2012_5yr_merge_5_6.xls acs2012_5yr_table_shells.xls
	mkdir -p precomputed/acs2012_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2012_5yr/

precomputed/acs2013_1yr/census_table_metadata.csv: acs2013_1yr_merge_5_6.xls acs2013_1yr_table_shells.xls
	python process_merge.py acs2013_1yr_merge_5_6.xls acs2013_1yr_table_shells.xls
	mkdir -p precomputed/acs2013_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2013_1yr/

precomputed/acs2013_3yr/census_table_metadata.csv: acs2013_3yr_merge_5_6.xls acs2013_3yr_table_shells.xls
	python process_merge.py acs2013_3yr_merge_5_6.xls acs2013_3yr_table_shells.xls
	mkdir -p precomputed/acs2013_3yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2013_3yr/

precomputed/acs2013_5yr/census_table_metadata.csv: acs2013_5yr_merge_5_6.xls acs2013_5yr_table_shells.xls
	python process_merge.py acs2013_5yr_merge_5_6.xls acs2013_5yr_table_shells.xls
	mkdir -p precomputed/acs2013_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2013_5yr/

precomputed/acs2014_1yr/census_table_metadata.csv: acs2014_1yr_merge_5_6.xls acs2014_1yr_table_shells.xls
	python process_merge.py acs2014_1yr_merge_5_6.xls acs2014_1yr_table_shells.xls
	mkdir -p precomputed/acs2014_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2014_1yr/

precomputed/acs2014_5yr/census_table_metadata.csv: acs2014_5yr_merge_5_6.xls acs2014_5yr_table_shells.xls
	python process_merge.py acs2014_5yr_merge_5_6.xls acs2014_5yr_table_shells.xls
	mkdir -p precomputed/acs2014_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2014_5yr/

precomputed/acs2015_1yr/census_table_metadata.csv: acs2015_1yr_merge_5_6.xls acs2015_1yr_table_shells.xls
	python process_merge.py acs2015_1yr_merge_5_6.xls acs2015_1yr_table_shells.xls
	mkdir -p precomputed/acs2015_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2015_1yr/

precomputed/acs2015_5yr/census_table_metadata.csv: acs2015_5yr_merge_5_6.xls acs2015_5yr_table_shells.xls
	python process_merge.py acs2015_5yr_merge_5_6.xls acs2015_5yr_table_shells.xls
	mkdir -p precomputed/acs2015_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2015_5yr/

precomputed/acs2016_1yr/census_table_metadata.csv: acs2016_1yr_merge_5_6.xls acs2016_1yr_table_shells.xls
	python process_merge.py acs2016_1yr_merge_5_6.xls acs2016_1yr_table_shells.xls
	mkdir -p precomputed/acs2016_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2016_1yr/

precomputed/acs2016_5yr/census_table_metadata.csv: acs2016_5yr_merge_5_6.xls acs2016_5yr_table_shells.xls
	python process_merge.py acs2016_5yr_merge_5_6.xls acs2016_5yr_table_shells.xls
	mkdir -p precomputed/acs2016_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2016_5yr/

precomputed/acs2017_1yr/census_table_metadata.csv: acs2017_1yr_merge_5_6.xls acs2017_1yr_table_shells.xls
	python process_merge.py acs2017_1yr_merge_5_6.xls acs2017_1yr_table_shells.xls
	mkdir -p precomputed/acs2017_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2017_1yr/

precomputed/acs2017_5yr/census_table_metadata.csv: acs2017_5yr_merge_5_6.xls acs2017_5yr_table_shells.xls
	python process_merge.py acs2017_5yr_merge_5_6.xls acs2017_5yr_table_shells.xls
	mkdir -p precomputed/acs2017_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2017_5yr/

precomputed/acs2018_1yr/census_table_metadata.csv: acs2018_1yr_merge_5_6.xls acs2018_table_shells.xls
	python process_merge.py acs2018_1yr_merge_5_6.xls acs2018_table_shells.xls
	mkdir -p precomputed/acs2018_1yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2018_1yr/

precomputed/acs2018_5yr/census_table_metadata.csv: acs2018_5yr_merge_5_6.xls acs2018_table_shells.xls
	python process_merge.py acs2018_5yr_merge_5_6.xls acs2018_table_shells.xls
	mkdir -p precomputed/acs2018_5yr/
	mv census_column_metadata.csv census_table_metadata.csv precomputed/acs2018_5yr/

precomputed/acs2019_1yr/census_table_metadata.csv:
	mkdir -p precomputed/acs2019_1yr/
	python process_api.py https://api.census.gov/data/2019/acs/acs1/variables.json https://www2.census.gov/programs-surveys/acs/summary_file/2019/documentation/user_tools/ACS_1yr_Seq_Table_Number_Lookup.txt precomputed/acs2019_1yr
