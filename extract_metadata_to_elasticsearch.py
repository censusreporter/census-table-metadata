"""
Extracts table information from the Postgres database, translates it
into something that makes sense for Elasticsearch, and loads it into Elasticsearch.

To use this, open up a tunnel to the API server (assuming you have the SSH key):

    ssh -i ~/.ssh/censusreporter.ec2_key.pem -L 5432:localhost:5432 -L 9200:localhost:9200 ubuntu@censusreporter.org

(Port 5432 is for Postgres and 9200 is for Elasticsearch)

Then run this script to perform the load:

    python extract_metadata_to_elasticsearch.py

You can then test the results by curling directly against the Elasticsearch HTTP search endpoint:

    curl http://localhost:9200/census/tabulation,table,column/_search -d '
    {
        "query": {
            "term": { "column_title": "housing" }
        }
    }
    '
"""

import logging
import itertools
import pyes
import psycopg2
import psycopg2.extras

logging.basicConfig()

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

def convert_table_rows(rows):
    for row in rows:
        yield row

def process_single_table_query(cur, es, query):
    cur.execute(query)

    for obj in convert_table_rows(cur):
        es.index(obj, index='census', doc_type='table', id=obj.pop('uid'), bulk=True)

    es.force_bulk()

def convert_column_rows(rows):
    for row in rows:
        yield row

def process_single_column_query(cur, es, query):
    cur.execute(query)

    for obj in convert_column_rows(cur):
        es.index(obj, index='census', doc_type='column', id=obj.pop('uid'), bulk=True)

    es.force_bulk()

def convert_tabulation_rows(rows):
    for row in rows:
        yield row

def process_single_tabulation_query(cur, es, query):
    cur.execute(query)

    for obj in convert_tabulation_rows(cur):
        es.index(obj, index='census', doc_type='tabulation', id=obj.pop('uid'), bulk=True)

    es.force_bulk()

def main():
    conn = psycopg2.connect(
        host='localhost',
        user='census',
        password='censuspassword',
        database='census'
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    es = pyes.ES()
    index_manager = pyes.managers.Indices(es)

    print "Deleting old index..."
    index_manager.delete_index_if_exists('census')
    print "Creating new index..."
    index_manager.create_index('census', {
        "settings": {
            "analysis": {
                "analyzer": {
                    "synonym_ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": [
                            "synonym_filter",
                            "ngram_filter",
                            "stop",
                            "lowercase",
                        ],
                    },
                    "synonym_analyzer": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": [
                            "synonym_filter",
                            "stop",
                            "lowercase",
                        ],
                    },
                },
                "filter": {
                    "ngram_filter": {
                        "type": "nGram",
                        "min_gram": 2,
                        "max_gram": 20,
                        "token_chars": [ "letter", "digit" ],
                    },
                    "synonym_filter": {
                        "type": "synonym",
                        "expand": True,
                        "synonyms": [
                            "Ability to Speak English, languages, english-speaking, ESL, language",
                            "Age of Grandparent, seniors",
                            "All Housing Units, homes, houses, home, house, apartments, apartment",
                            "Ambulatory Difficulty, handicapped, disabled",
                            "American Indian and Alaska Native, native americans, native american",
                            "Ancestry, heritage",
                            "Bedrooms, homes, houses, home, house, apartments, apartment",
                            "Cash Public Assistance Income, welfare, government assistance",
                            "Children Under 18 Years in Households, kids, families, family",
                            "Citizenship Status, immigrants, immigrant, foreign",
                            "Civilian Employed Population 16 Years and Over, jobs, workers",
                            "Civilian Noninstitutionalized Population 16 Years and Over With Earnings, money, income",
                            "Civilian Population 18 to 64 Years, adults, adult",
                            "Civilian Population 18 Years and Over, adults, adult",
                            "Civilian Population 18 Years and Over With Income, adults, adult",
                            "Civilian Population 25 Years and Over, adults, adult",
                            "Civilian Population 65 Years and Over, seniors, senior",
                            "Class of Worker, jobs, job, job type",
                            "Class of Worker and Median Earnings, jobs, job, job type, income",
                            "Cognitive Difficulty, retarded, learning impaired, disabled, dyslexic",
                            "College or Graduate School Enrollment, higher education, grad school",
                            "Contract Rent, homes, houses, home, house, apartments, apartment",
                            "Current Residence, homes, houses, home, house, apartments, apartment",
                            "Disability Items, handicapped, disabled, disabilities",
                            "Disability Status, handicapped, disabled, disabilities",
                            "Disability Status of Grandparents Living With Own Grandchildren Under 18 Years, handicapped, disabled, disabilities, seniors, grandkids",
                            "Divorced, marriage, marital status",
                            "Divorces in the Last Year, marriage, marital status",
                            "Earnings, income, money, wage, wages",
                            "Educational Attainment, schools, learning, education",
                            "Employer-based Health Insurance, jobs, workers, benefits",
                            "Employment Status, jobs, workers, employed",
                            "Employment Status of Grandparents Living With Own Grandchildren Under 18 Years, jobs, workers, seniors, grandkids, kids, employed",
                            "Employment Status of Parents, jobs, workers, families, employed",
                            "Enrollment Status, education, schools",
                            "Families, family",
                            "Families and Presence of Own Children, family, kids",
                            "Families With Grandparent Householders And/or Spouses Living With Own Grandchildren Under 18 Years, seniors, grandkids, kids",
                            "Family Income, families, money, budget, wage, wages",
                            "Family Size, families",
                            "Family Type, families",
                            "Family Type and Age, families",
                            "Females 15 to 50 Years, women, girls, teens, teenagers, youth",
                            "Females 20 to 64 Years, women",
                            "Fertility of Women 15 to 50 Years, births, females, girls, teens, teenagers, youth",
                            "Field of Bachelor's Degree, college, higher education",
                            "Field of Degree, college, higher education",
                            "First Ancestry Reported, heritage",
                            "First Major, college, degree, higher education",
                            "Food Stamps/SNAP Receipt, welfare, public assistance, government assistance",
                            "Foreign-born Population, immigrants, immigrant, nationality",
                            "Full-time, Year-round Civilian Employed, jobs, workers, occupations",
                            "Geographical Mobility in the Past Year, migration, moving, relocate, relocation",
                            "Gini Index of Income Inequality, poverty, money, classes",
                            "Grade Enrolled, schools, education",
                            "Grandchild, kids, kid, grandkids, grandkid, families, family",
                            "Grandchildren Under 18 Years, kids, kid, grandkids, grandkid, families, family",
                            "Grandchildren Under 18 Years Living With a Grandparent Householder, kids, kid, grandkids, grandkid, families, family, seniors",
                            "Grandparent, seniors",
                            "Grandparent Responsibility and Presence of Parent, seniors, family, families",
                            "Grandparents Living With Grandchildren Under 18 Years, kids, kid, grandkids, grandkid, families, family, seniors",
                            "Grandparents Living With Own Grandchildren Under 18 Years, kids, kid, grandkids, grandkid, families, family, seniors",
                            "Grandparents Responsible, seniors, family, families",
                            "Gross Rent, housing costs",
                            "Gross Rent as a Percentage of Household Income, housing costs, family, families",
                            "Group Quarters Population, jail, prison, dormitory, retirement home, assisted living facility, nursing home, institutionalized, group home, student housing, barracks, military housing, hospice, correctional facility",
                            "Hearing Difficulty, deaf, disability, disabilities",
                            "House Heating Fuel, homes, utility, utilities, energy use",
                            "Household, family, families",
                            "Household Income, families, money, budget, wages",
                            "Household Income Quintile Upper Limits, families, money, budget, wages",
                            "Household Language, family, families",
                            "Household Size, family, families",
                            "Household Type, family, families",
                            "Household Type and Age of Householder, family, families",
                            "Household Type and Presence and Age of Own Children, family, families, kids, kid",
                            "Householder, home owner, homeowner, home-owner",
                            "Householder Status, home owner, homeowner, home-owner",
                            "Households, family, families",
                            "Households in Which No One 14 and Over Speaks English Only or Speaks a Language Other Than English at Home and Speaks English Very Well, family, families, esl, immigrants, immigration",
                            "Households With Grandparents Living With Own Grandchildren Under 18 Years, family, families, seniors, kids, kid",
                            "Housing Costs as a Percentage of Household Income, family, families, money, budget",
                            "Inclusion of Utilities in Rent, housing costs",
                            "Income, money, earnings, salary, salaries, budget",
                            "Income Deficit, money, earnings, salary, salaries, budget",
                            "Income Deficit  of Unrelated Individuals, money, earnings, salary, salaries, budget",
                            "Independent Living Difficulty, disability, disabilities",
                            "Individual Income, money, earnings, salary, salaries, budget",
                            "Individuals Income, money, earnings, salary, salaries, budget",
                            "Industry, jobs, occupations, workers, labor, job, occupation, worker",
                            "Industry and Median Earnings, jobs, occupations, workers, labor, job, occupation, worker, income, money, salary, salaries",
                            "Interest, Dividends, or Net Rental Income, investments, housing",
                            "Kitchen Facilities, housing, utilities",
                            "Labor Force Participation, jobs, workers, job, worker",
                            "Labor Force Status, jobs, workers, job, worker",
                            "Language and Ability to Speak English of Grandparents Living With Own Grandchildren Under 18 Years, seniors, kids, esl, immigrants, imigrant, kid, senior, immigration",
                            "Language Spoken at Home, esl, immigrants, immigrant, immigration",
                            "Language Spoken at Home and Ability to Speak English, esl, immigrants, immigrant, immigration",
                            "Language Status, fluent, fluency",
                            "Length of Time Grandparent Responsible, seniors, senior",
                            "Level of School, education, attainment",
                            "Living Alone, family, families",
                            "Living Arrangements, family, families, housing",
                            "Living Arrangements and Nativity of Parents, family, families, housing, foreign, immigrant",
                            "Lower Contract Rent Quartile, housing costs",
                            "Lower Value Quartile, housing costs",
                            "Marital Status, marriages, marriage",
                            "Marriages Ending in Widowhood in the Last Year, marital status, deaths, death, widow",
                            "Marriages in the Last Year, marital status",
                            "Married, marriages, marital status",
                            "Married Population 15 Years and Over, marriages, marital status",
                            "Meals Included in Rent, housing costs",
                            "Mean Household Income of Quintiles, money, earnings",
                            "Mean Usual Hours Worked, jobs, full-time, part-time, full time, part time",
                            "Means of Transportation to Work, commute, commuting, jobs, transit",
                            "Median Age at First Marriage, marital status",
                            "Median Contract Rent, housing costs",
                            "Median Duration of Current Marriage in Years, marital status",
                            "Median Earnings, money, income, wage, wages",
                            "Median Family Income, households, families, money, earnings, wage, wages",
                            "Median Gross Rent, housing costs",
                            "Median Gross Rent as a Percentage of Household Income, housing costs, family, families, money, earnings, wage, wages",
                            "Median Household Income, family, families, money, earnings, budget, wage, wages",
                            "Median Household Income the Past 12 Months, family, families, money, earnings, budget, wage, wages",
                            "Median Income, money, earnings, budget, wage, wages",
                            "Median Nonfamily Household Income, money, earnings, budget, roommates, cohabitation",
                            "Median Number of Rooms, housing, homes, houses",
                            "Median Real Estate Taxes Paid, housing costs, home owner, homeowner, home-owner",
                            "Median Selected Monthly Owner Costs, housing costs, home owner, homeowner, home-owner",
                            "Median Selected Monthly Owner Costs as a Percentage of Household Income, housing costs, budget, family, families, home owner, homeowner, home-owner",
                            "Median Value, housing costs",
                            "Median Year Householder Moved Into Unit, housing, homes, houses",
                            "Median Year Structure Built, construction, housing, homes, houses, age",
                            "Medicaid/Means-tested Public Coverage, public assistance, health, government assistance",
                            "Medicare Coverage, public assistance, health, government assistance",
                            "Mobile Homes, housing, houses, trailor, trailors",
                            "Mobility Status, migration, moving",
                            "Monthly Housing Costs as a Percentage of Household Income, family, families, budget, wage, wages",
                            "Mortgage Status, housing, homes, houses, home owner, homeowner, home-owner",
                            "Movers Between Regions, mobility, migration, moving",
                            "Multigenerational Households, seniors, families, family",
                            "Nativity, place of birth, nationality, immigrant",
                            "Nativity of Children Under 18 Years in Families, place of birth, nationality, kids, kid, family, immigrant",
                            "Nonfamily Household Income, roommates, cohabitation, budget, money, wage, wages",
                            "Nonfamily Households, roommates, roommate, cohabitation",
                            "Nonrelatives, roommates, roommate, cohabitation",
                            "Number and Nativity of Parents, family, families, place of birth, nationality",
                            "Number of Disabilities, disabled, disability, handicapped",
                            "Number of Earners in Family, families, budget, income, money",
                            "Number of Own Children Under 18 Years, family, families, kids, kid, parents, teenagers, teenager, youth",
                            "Number of Persons in Family, people, family, families, kids, kid, parents",
                            "Number of Related Children Under 18 Years, family, families, kids, kid, teenagers, teenager, youth",
                            "Number of Rooms, housing, homes, houses",
                            "Number of Times Married, marital status, marriage, divorces",
                            "Number of Vehicles (Car, Truck, or Van) Used in Commuting, commute, jobs, workers, job, worker, driving, drive",
                            "Number of Vehicles Available, driving, drive",
                            "Number of Workers in Family, jobs, employed",
                            "Number of Workers in Household, jobs, employed",
                            "Occupancy Status, housing, homes, houses",
                            "Occupants Per Room, housing, homes, houses",
                            "Occupation, jobs, job, industry, workers, profession",
                            "Occupied Housing Units, homes, houses",
                            "Other Types of Income, money, earnings",
                            "Own Children Under 18 Years, family, families, kids, kid, teenagers, teenager, youth",
                            "Own Children Under 18 Years in Families and Subfamilies, family, kids, kid, teenagers, teenager, youth",
                            "Own Grandchildren, kids, seniors",
                            "Own Grandchildren Under 18 Years, kids, seniors, senior, kid, teenagers, teenager, youth",
                            "Owner-occupied Housing Units, home owner, homeowner, home-owner, houses",
                            "People Reporting Ancestry, heritage",
                            "People Reporting Multiple Ancestry, heritage",
                            "People Reporting Single Ancestry, heritage",
                            "Per Capita Income, money, wages, earnings",
                            "Percent of Income Imputed, money, wages, earnings",
                            "Period of Military Service, veterans, veteran",
                            "Period of Naturalization, nationality, immigration",
                            "Place of Birth, nationality, immigration",
                            "Place of Work, jobs, job, occupations, profession",
                            "Plumbing Facilities, utilities, housing, houses, homes",
                            "Population 16 to 19 Years, kids, kid, teenagers, teenager, youth",
                            "Population 18 Years and Over, adults, adult",
                            "Population 20 to 64 Years, adults, adult",
                            "Population 25 to 64 Years, adults, adult",
                            "Population 25 Years and Over, adults, adult",
                            "Population 30 Years and Over, adults",
                            "Population 65 Years and Over, seniors, senior",
                            "Population Under 18 Years, kids, kid, teenagers, teenager, youth",
                            "Poverty Status, poor",
                            "Presence and Age of Own Children Under 18 Years, family, families, kids",
                            "Presence and Age of Related Children Under 18 Years, family, families, kids",
                            "Presence of Children Under 18 Years, family, families, kids, kid, teenagers, teenager, youth",
                            "Presence of Nonrelatives, roommates, cohabitation",
                            "Presence of Own Children Under 18 Years, family, families, kids, kid, teenagers, teenager, youth",
                            "Presence of Own Children Under 18 Years in Married-couple Families, family, families, kids, kid, teenagers, teenager, youth",
                            "Presence of Parent of Grandchild, seniors, senior, kids, kid, teenagers, teenager, youth",
                            "Presence of Parent of Grandchildren, seniors, senior, kids, kid, teenagers, teenager, youth",
                            "Presence of Parent of Grandchildren and Age of Grandparent, seniors, senior, kids, kid, teenagers, teenager, youth",
                            "Presence of People 60 Years and Over, seniors, senior ",
                            "Presence of People 65 Years and Over, Household Size and Household Type, seniors, senior ",
                            "Presence of People Under 18 Years, kids, kid, teenagers, teenager, youth, child, children",
                            "Presence of Related Children Under 18 Years, kids, kid, teenagers, teenager, youth, child",
                            "Presence of Unmarried Partner, cohabitation, domestic partner",
                            "Presence of Unmarried Partner of Householder, cohabitation, domestic partner",
                            "Price Asked, list price, listing price, listed price, housing, houses, homes",
                            "Public Assistance Income, welfare, government assistance",
                            "Public Assistance Income or Food Stamps/SNAP, welfare, government assistance",
                            "Ratio of Income to Poverty Level, poor",
                            "Ratio of Income to Poverty Level of Families, poor, family",
                            "Real Estate Taxes Paid, housing costs, homeowner, home owner, home-owner",
                            "Receipt of Food Stamps/SNAP, welfare, government assistance",
                            "Receipt of Public Assistance Income, welfare, government assistance",
                            "Receipt of Supplemental Security Income (SSI), Cash Public Assistance Income, or Food Stamps/SNAP, welfare, government assistance",
                            "Related Children, kids, kid, teenagers, teenager, youth, child",
                            "Related Children Under 18 Years, kids, kid, teenagers, teenager, youth, child",
                            "Relatives, family, families",
                            "Rent Asked, housing costs",
                            "Residence 1 Year Ago, migration, moving",
                            "Retirement Income, seniors",
                            "Rooms, housing, houses, homes",
                            "School Enrollment, education",
                            "Second Ancestry Reported, heritage",
                            "Selected Monthly Owner Costs, housing, budget",
                            "Selected Monthly Owner Costs as a Percentage of Household Income, housing, budget",
                            "Selected Tribal Groupings, tribes, native americans",
                            "Self-care Difficulty, disabled, disability, disabilities",
                            "Self-employment Income, jobs, workers, earnings, money, wage, wages",
                            "Service-connected Disability-rating Status and Ratings, disabled, disabilities",
                            "Sex, gender",
                            "Sex of Grandparents Living With Own Grandchildren Under 18 Years, gender, seniors, kids",
                            "Sex of Householder, gender",
                            "Sex of Partner, gender",
                            "Sex of Workers, gender",
                            "Shares of Household Income, inequality",
                            "Social Security Income, retirement, wages, earnings",
                            "Specific Origin, ancestry, heritage",
                            "Supplemental Security Income (SSI), welfare, public assistance, poor, poverty, seniors, disabled, disability, disabilities, government assistance",
                            "Telephone Service Available, utilities, housing, homes, houses",
                            "Tenure of Grandparents Living With Own Grandchildren Under 18 Years, seniors, kids",
                            "Time Arriving at Work From Home, commute, commuting, jobs, traffic, drive, driving",
                            "Time Leaving Home to Go to Work, commute, commuting, jobs, traffic, drive, driving",
                            "Times Married, marital status, divorces, marriage",
                            "Total Ancestry Reported, heritage",
                            "Total Fields of Bachelor's Degrees Reported, college, education, higher education",
                            "Travel Time to Work, commute, commuting, jobs, traffic, drive, driving",
                            "Type of School, education",
                            "Units in Structure, construction, housing",
                            "Units in Structure of Grandparents Living With Own Grandchildren Under 18 Years, construction, housing, seniors, kids",
                            "Unmarried-partner Households, cohabitation, domestic partner",
                            "Unrelated Individuals, roommates, cohabitation",
                            "Upper Contract Rent Quartile, housing costs",
                            "Upper Value Quartile, housing costs",
                            "Usual Hours Worked, jobs, workers, labor, part-time, full-time, part time, full time",
                            "Usual Hours Worked Per Week, jobs, workers, labor, part-time, full-time, part time, full time",
                            "Vacancy Status, housing",
                            "Vacant - Current Residence Elsewhere, housing",
                            "Vision Difficulty, disabled, disabilities, disability, blindness",
                            "Weeks Worked, jobs, workers, labor",
                            "Widowed, deaths, marital status, marriages",
                            "Women 15 to 50 Years, females",
                            "Women 15 to 50 Years Who Had a Birth, females, fertility, fertile, pregnant, gave birth",
                            "Women 16 to 50 Years Who Had a Birth, females, fertility, fertile, pregnant, gave birth",
                            "Work Experience, jobs, workers, labor, professional",
                            "Work Experience of Householder and Spouse, jobs, workers, labor, professional",
                            "Work Experience of Unrelated Individuals, jobs, workers, labor, professional",
                            "Work Status, jobs, workers, labor, professional",
                            "Worker Population, jobs, labor, job",
                            "Workers, jobs, labor, job",
                            "Workers' Earnings, jobs, labor, income, money, wages",
                            "Year Householder Moved Into Unit, housing, migration, moving",
                            "Year Last Married, marital status, marriages, marriage",
                            "Year of Entry, immigration, nationality",
                            "Year of Naturalization, immigration, nationality",
                            "Year Structure Built, housing, construction, constructed",
                            "Young Adults Aged 19 to 25, youth",
                        ]
                    },
                },
            }
        },
        "mappings": {
            "tabulation": {
                "properties": {
                    "table_title": {
                        "type": "string",
                        "index_analyzer": "synonym_ngram_analyzer",
                        "search_analyzer": "synonym_analyzer",
                    },
                    "topics": {
                        "type": "string",
                        "index": "not_analyzed",
                    },
                }
            },
            "table": {
                "properties": {
                    "table_title": {
                        "type": "string",
                        "index_analyzer": "synonym_ngram_analyzer",
                        "search_analyzer": "synonym_analyzer",
                    },
                    "topics": {
                        "type": "string",
                        "index": "not_analyzed",
                    },
                }
            },
            "column": {
                "properties": {
                    "column_title": {
                        "type": "string",
                        "index_analyzer": "synonym_ngram_analyzer",
                        "search_analyzer": "synonym_analyzer",
                    },
                    "topics": {
                        "type": "string",
                        "index": "not_analyzed",
                    },
                }
            },
        }
    })

    # print "Loading test row"
    # obj = {
    #     'uid': 'foo',
    #     'column_title': 'Vacant - Current Residence Elsewhere',
    # }
    # es.index(obj, index='census', doc_type='column', id=obj.pop('uid'))

    print "Loading tabulation data."
    q = """SELECT
        tab.table_title,
        tab.tabulation_code,
        (SELECT unnest(tables_in_one_yr || tables_in_three_yr || tables_in_five_yr)
            FROM census_tabulation_metadata
            WHERE tabulation_code=tab.tabulation_code
            LIMIT 1) as table_id,
        5 as weight,
        tab.tabulation_code as uid,
        tab.universe,
        tab.topics
    FROM public.census_tabulation_metadata tab;"""
    process_single_tabulation_query(cur, es, q)

    print "Loading ACS 2012 5-year tables..."
    q = """SELECT
        tab.table_title,
        tab.table_id,
        10 as weight,
        'acs2012_5yr' as release,
        'acs2012_5yr_' || tab.table_id as uid,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_5yr.census_table_metadata tab;"""
    process_single_table_query(cur, es, q)

    print "Loading ACS 2012 5-year columns..."
    q = """SELECT
        col.column_title,
        col.column_id,
        tab.table_title,
        tab.table_id,
        5 as weight,
        'acs2012_5yr' as release,
        'acs2012_5yr_' || col.column_id as uid,
        col.parent_column_id,
        col.indent,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_5yr.census_column_metadata col LEFT JOIN acs2012_5yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

    print "Loading ACS 2012 3-year tables..."
    q = """SELECT
        tab.table_title,
        tab.table_id,
        10 as weight,
        'acs2012_3yr' as release,
        'acs2012_3yr_' || tab.table_id as uid,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_3yr.census_table_metadata tab;"""
    process_single_table_query(cur, es, q)

    print "Loading ACS 2012 3-year columns..."
    q = """SELECT
        col.column_title,
        col.column_id,
        tab.table_title,
        tab.table_id,
        5 as weight,
        'acs2012_3yr' as release,
        'acs2012_3yr_' || col.column_id as uid,
        col.parent_column_id,
        col.indent,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_3yr.census_column_metadata col LEFT JOIN acs2012_3yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

    print "Loading ACS 2012 1-year tables..."
    q = """SELECT
        tab.table_title,
        tab.table_id,
        10 as weight,
        'acs2012_1yr' as release,
        'acs2012_1yr_' || tab.table_id as uid,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_1yr.census_table_metadata tab;"""
    process_single_table_query(cur, es, q)

    print "Loading ACS 2012 1-year columns..."
    q = """SELECT
        col.column_title,
        col.column_id,
        tab.table_title,
        tab.table_id,
        5 as weight,
        'acs2012_1yr' as release,
        'acs2012_1yr_' || col.column_id as uid,
        col.parent_column_id,
        col.indent,
        tab.universe,
        tab.denominator_column_id,
        tab.topics
    FROM acs2012_1yr.census_column_metadata col LEFT JOIN acs2012_1yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

    index_manager.refresh()

if __name__ == '__main__':
    main()