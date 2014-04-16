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

        row['name_suggest'] = {
            'input': row.get('names'),
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

        row['name_suggest'] = {
            'input': row.get('names'),
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
                            ""
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