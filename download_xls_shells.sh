#/bin/bash

echo "Downloading 2007 1yr merge_5_6"
wget -q "http://www2.census.gov/acs2007_1yr/summaryfile/merge_5_6_final.xls" -O acs2007_1yr_merge_5_6.xls
echo "Downloading 2007 3yr merge_5_6"
wget -q "http://www2.census.gov/acs2007_3yr/summaryfile/merge_5_6_final.xls" -O acs2007_3yr_merge_5_6.xls
echo "Downloading 2007 shells"
mkdir acs2007_shells
cd acs2007_shells
wget -q "http://www2.census.gov/acs/downloads/shells/2007/Detailed_Tables/" --no-parent --accept="*.xls" --recursive -nH --cut-dirs=5
rm -f robots.txt
cd ..

echo "Downloading 2008 1yr merge_5_6"
wget -q "http://www2.census.gov/acs2008_1yr/summaryfile/merge_5_6_final.xls" -O acs2008_1yr_merge_5_6.xls
echo "Downloading 2008 3yr merge_5_6"
wget -q "http://www2.census.gov/acs2008_3yr/summaryfile/merge_5_6_final.xls" -O acs2008_3yr_merge_5_6.xls
echo "Downloading 2008 shells"
mkdir acs2008_shells
cd acs2008_shells
wget -q "http://www2.census.gov/acs/downloads/shells/2008/Detailed_Tables/" --no-parent --accept="*.xls" --recursive -nH --cut-dirs=5
rm -f robots.txt
cd ..

echo "Downloading 2009 1yr"
wget -q "http://www2.census.gov/acs2009_1yr/summaryfile/merge_5_6.xls" -O acs2009_1yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2009_1yr/summaryfile/ACS2009TableShells.xls" -O acs2009_1yr_TableShells.xls

echo "Downloading 2009 3yr"
wget -q "http://www2.census.gov/acs2009_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2009_3yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2009_3yr/summaryfile/ACS2009_3-Year_TableShells.xls" -O acs2009_3yr_TableShells.xls

echo "Downloading 2010 1yr"
wget -q "http://www2.census.gov/acs2010_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2010_1yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2010_1yr/summaryfile/ACS2010_1-Year_TableShells.xls" -O acs2010_1yr_TableShells.xls

echo "Downloading 2010 3yr"
wget -q "http://www2.census.gov/acs2010_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2010_3yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2010_3yr/summaryfile/ACS2010_3-Year_TableShells.xls" -O acs2010_3yr_TableShells.xls

echo "Downloading 2010 5yr"
wget -q "http://www2.census.gov/acs2010_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2010_5yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2010_5yr/summaryfile/ACS2010_5-Year_TableShells.xls" -O acs2010_5yr_TableShells.xls

echo "Downloading 2011 1yr"
wget -q "http://www2.census.gov/acs2011_1yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2011_1yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2011_1yr/summaryfile/ACS2011_1-Year_TableShells.xls" -O acs2011_1yr_TableShells.xls

echo "Downloading 2011 3yr"
wget -q "http://www2.census.gov/acs2011_3yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2011_3yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2011_3yr/summaryfile/ACS2011_3-Year_TableShells.xls" -O acs2011_3yr_TableShells.xls

echo "Downloading 2011 5yr"
wget -q "http://www2.census.gov/acs2011_5yr/summaryfile/Sequence_Number_and_Table_Number_Lookup.xls" -O acs2011_5yr_merge_5_6.xls
wget -q "http://www2.census.gov/acs2011_5yr/summaryfile/ACS2011_5-Year_TableShells.xls" -O acs2011_5yr_TableShells.xls
