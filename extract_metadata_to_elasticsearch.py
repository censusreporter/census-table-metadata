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
                    "synonym_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "synonym_filter",
                            "stop",
                            "ngram_filter",
                        ],
                    }
                },
                "filter": {
                    "ngram_filter": {
                        "type": "nGram",
                        "min_gram": 4,
                        "max_gram": 20,
                        "token_chars": [ "letter" ],
                    },
                    "synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "esl, ability to speak english",
                            "ability to speak english, languages, english speaking, esl, language",
                            "age of grandparent, seniors",
                            "all housing units, homes, houses, home, house, apartments, apartment",
                            "ambulatory difficulty, handicapped, disabled",
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
                        "analyzer": "synonym_analyzer",
                    },
                }
            },
            "table": {
                "properties": {
                    "table_title": {
                        "type": "string",
                        "analyzer": "synonym_analyzer",
                    },
                }
            },
            "column": {
                "properties": {
                    "column_title": {
                        "type": "string",
                        "analyzer": "synonym_analyzer",
                    },
                }
            },
        }
    })

    # print "Loading test row"
    # obj = {
    #     'uid': 'foo',
    #     'column_title': 'Ability to Speak English',
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

    # print "Loading ACS 2012 3-year tables..."
    # q = """SELECT
    #     tab.table_title,
    #     tab.table_id,
    #     10 as weight,
    #     'acs2012_3yr' as release,
    #     'acs2012_3yr_' || tab.table_id as uid,
    #     tab.universe,
    #     tab.denominator_column_id,
    #     tab.topics
    # FROM acs2012_3yr.census_table_metadata tab;"""
    # process_single_table_query(cur, es, q)

    # print "Loading ACS 2012 3-year columns..."
    # q = """SELECT
    #     col.column_title,
    #     col.column_id,
    #     tab.table_title,
    #     tab.table_id,
    #     5 as weight,
    #     'acs2012_3yr' as release,
    #     'acs2012_3yr_' || col.column_id as uid,
    #     col.parent_column_id,
    #     col.indent,
    #     tab.universe,
    #     tab.denominator_column_id,
    #     tab.topics
    # FROM acs2012_3yr.census_column_metadata col LEFT JOIN acs2012_3yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    # process_single_column_query(cur, es, q)

    # print "Loading ACS 2012 1-year tables..."
    # q = """SELECT
    #     tab.table_title,
    #     tab.table_id,
    #     10 as weight,
    #     'acs2012_1yr' as release,
    #     'acs2012_1yr_' || tab.table_id as uid,
    #     tab.universe,
    #     tab.denominator_column_id,
    #     tab.topics
    # FROM acs2012_1yr.census_table_metadata tab;"""
    # process_single_table_query(cur, es, q)

    # print "Loading ACS 2012 1-year columns..."
    # q = """SELECT
    #     col.column_title,
    #     col.column_id,
    #     tab.table_title,
    #     tab.table_id,
    #     5 as weight,
    #     'acs2012_1yr' as release,
    #     'acs2012_1yr_' || col.column_id as uid,
    #     col.parent_column_id,
    #     col.indent,
    #     tab.universe,
    #     tab.denominator_column_id,
    #     tab.topics
    # FROM acs2012_1yr.census_column_metadata col LEFT JOIN acs2012_1yr.census_table_metadata tab ON (tab.table_id=col.table_id);"""
    # process_single_column_query(cur, es, q)

    index_manager.refresh()

if __name__ == '__main__':
    main()