import logging
import itertools
import sys
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

        input_names = []
        input_names.extend(row.get('names'))
        input_names.append(row.get('table_id'))

        row['name_suggest'] = {
            'input': input_names,
            'output': row.get('table_title'),
            'payload': {
                'table_id': row.get('table_id')
            },
        }

        yield row

def process_single_table_query(cur, es, query):
    cur.execute(query)

    for obj in convert_table_rows(cur):
        es.index(obj, index='census', doc_type="table", id=obj['uid'], bulk=True)

    es.force_bulk()

def convert_column_rows(rows):
    for row in rows:

        input_names = []
        input_names.extend(row.get('names'))
        input_names.append(row.get('column_id'))

        row['name_suggest'] = {
            'input': input_names,
            'output': row.get('column_title'),
            'payload': {
                'column_id': row.get('column_id'),
                'table_id': row.get('table_id'),
                'table_title': row.get('table_title'),
            },
        }

        yield row

def process_single_column_query(cur, es, query):
    cur.execute(query)

    for obj in convert_column_rows(cur):
        es.index(obj, index='census', doc_type="column", id=obj['uid'], bulk=True)

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
                    "suggest_synonyms": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": [ "my_synonyms" ]
                    },
                    "synonyms_expand": {
                        "type": "custom",
                        "filter": [
                            "standard",
                            "lowercase",
                            "stop",
                            "my_synonyms",
                        ],
                        "tokenizer": "standard"
                    }
                },
                "filter": {
                    "my_synonyms": {
                        "type": "synonym",
                        "synonyms": [
                            "speak english, language",
                            "grandparent, grandparents, 65 years and over, seniors",
                            "grandchildren, grandkids",
                            "housing unit, housing units, rent, residence, homes, home, houses, house",
                            "ambulatory difficulty, living difficulty, disability, handicapped, disabled, disabilities",
                            "american indian, native, native american",
                            "ancestry, heritage",
                            "household, family, families",
                            "public assistance, welfare, government assistance, medicaid, medicare",
                            "children, kids",
                            "citizenship, immigrant, foreign",
                            "employed, employment, jobs, workers",
                            "earnings, money, income, salary, salaries",
                            "18 to 64, 18 years and over, 25 years and over, 65 years and over, adults",
                            "under 18, kids",
                            "cognitive difficulty, learning impaired, disabled",
                            "graduate school, college, higher education, grad school, first major",
                            "divorced, divorces, marriage, marital status",
                            "educational attainment, schools, learning",
                            "employer-based, jobs, workers, benefits",
                            "females, women",
                            "fertility, births",
                            "ancestry, heritage",
                            "income inequality, poverty, money, class",
                            "hearing difficulty, deaf, disability, disabilities",
                            "heating, utility, utilities, homes",
                            "kitchen, housing, utilities",
                            "labor force, jobs, workers",
                            "ability to speak english, language spoken at home, immigrants, esl, immigration",
                            "school, education",
                            "living alone, living arrangements, family, families, housing",
                            "mobility, migration, moving",
                            "mobile home, housing, houses",
                            "nativity, place of birth, nationality",
                            "nonfamily household, nonrelative, roommates, unrelated individuals, cohabitation, unmarried partner",
                            "vehicles, driving",
                            "commuting, commute, driving",
                            "military service, veterans",
                            "price asked, list price, listing price, listed price, housing, houses, homes",
                            "poverty level, poor",
                            "real estate, home",
                            "retirement, seniors",
                            "tribal, tribes, native american",
                            "self-care, disabled",
                            "shares of household, inequality",
                            "social security, retirement",
                            "supplemental security income, welfare, public assistance, poverty, poor, seniors, disabled",
                            "telephone, utilities, utility",
                            "arriving at work, to go to work, commute, commuting, jobs, traffic",
                            "bachelor's degrees, college, education, higher education",
                            "units in structure, year structure built, construction, housing",
                            "hours worked, jobs, workers, labor",
                            "vacancy, vacant, housing",
                            "vision difficulty, disabled, disabilities, disability, blindness, blind",
                            "widowed, death, marital status, marriages",
                            "who had a birth, fertility",
                        ]
                    }
                }
            }
        },
        "mappings": {
            "table": {
                "properties": {
                    "names": {
                        "type": "string",
                        "analyzer": "synonyms_expand"
                    },
                    "name_suggest": {
                        "type": "completion",
                        "analyzer": "suggest_synonyms",
                        "payloads": True
                    }
                }
            },
            "column": {
                "properties": {
                    "names": {
                        "type": "string",
                        "analyzer": "synonyms_expand"
                    },
                    "name_suggest": {
                        "type": "completion",
                        "analyzer": "suggest_synonyms",
                        "payloads": True
                    }
                }
            }
        }
    })

    print "Loading ACS 2012 5-year tables..."
    q = """SELECT
        ARRAY[
            tab.table_title
        ] as names,
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
        ARRAY[
            col.column_title
        ] as names,
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
    FROM acs2012_5yr.census_column_metadata col LEFT OUTER JOIN acs2012_5yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

    print "Loading ACS 2012 3-year tables..."
    q = """SELECT
        ARRAY[
            tab.table_title
        ] as names,
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
        ARRAY[
            col.column_title
        ] as names,
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
    FROM acs2012_3yr.census_column_metadata col LEFT OUTER JOIN acs2012_5yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

    print "Loading ACS 2012 1-year tables..."
    q = """SELECT
        ARRAY[
            tab.table_title
        ] as names,
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
        ARRAY[
            col.column_title
        ] as names,
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
    FROM acs2012_1yr.census_column_metadata col LEFT OUTER JOIN acs2012_5yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    process_single_column_query(cur, es, q)

if __name__ == '__main__':
    main()