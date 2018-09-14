#!/usr/bin/env python
# coding=utf-8

import csv
import os
import re
from collections import defaultdict

releases_to_analyze = ['acs2017_1yr', 'acs2016_5yr']
releases_to_output = ['acs2017_1yr', None, 'acs2016_5yr']
tables_by_code = defaultdict(list)

tables_by_release = defaultdict(dict)

tables_by_tabulation = defaultdict(dict)

columns_by_release = defaultdict(dict)

topics = defaultdict(set)
centopics = defaultdict(set)

for dirpath, dirnames, filenames in os.walk('precomputed'):
    release = dirpath.split('/')[-1]
    if release in releases_to_analyze:
        if 'census_table_metadata.csv' in filenames:
            r = csv.reader(open("%s/census_table_metadata.csv" % dirpath))
            header = r.next()
            for row in r:
                table_code = row[0]
                tabulation_code = re.search(r'\D*(\d*)\D*', table_code).groups()[0]
                tables_by_release[release][table_code] = row
                if tabulation_code not in tables_by_tabulation[release]:
                    tables_by_tabulation[release][tabulation_code] = {}
                tables_by_tabulation[release][tabulation_code][table_code] = row
                tables_by_code[table_code].append(release)
                centopics[row[3]].add(table_code)
                for topic in eval(row[-1]):
                    topics[topic].add(table_code)

        if 'census_column_metadata.csv' in filenames:
            columns_by_release[release] = defaultdict(dict)
            r = csv.reader(open("%s/census_column_metadata.csv" % dirpath))
            header = r.next()
            for row in r:
                try:
                    columns_by_release[release][row[0]].append(row)
                except:
                    columns_by_release[release][row[0]] = [row]

# keep track of how many tables appear in how many releases. We act as though
# all tables are in all releases
table_counter = defaultdict(list)

for k,v in tables_by_code.items():
    table_counter[len(v)].append(k)

def table_name(code):
    return table_data(code)[1]

def find_by_name(s):
    results = []
    for c in tables_by_code:
        if s.lower() in table_name(c).lower():
            results.append((c,table_name(c)))
    return results

def table_data(code):
    code = code.upper()
    best_release = tables_by_code[code][-1]
    return tables_by_release[best_release][code]

def columns(code,include_code=False):
    code = code.upper()
    best_release = tables_by_code[code][-1]
    results = []
    for x in columns_by_release[best_release][code]:
        depth = int(x[4])
        name = ('  ' * (depth-1)) + x[3]
        if include_code:
            results.append((x[2],name))
        else:
            results.append(name)
    return results

def key_tables(codes):
    return [x for x in sorted(codes) if x[0] == 'B' and x[-1].isdigit()]

def make_table_key(code):
    code = code[1:]
    if code.endswith('PR'):
        code = code[:-2]
    if code[-1].isalpha():
        code = code[:-1]
    return code

def table_breakdown(codes):
    def blank_dict():
        return {'B': False, 'C': False, 'I': False, 'PR': False}
    analyzed = defaultdict(blank_dict)
    for code in codes:
        key = make_table_key(code)
        if code.endswith('PR'):
            code = code[:-2]
            analyzed[key]['PR'] = True
        if code[-1].isdigit():
            analyzed[key][code[0]] = True
        if code[-1].isalpha():
            analyzed[key]['I'] = True
    return dict(analyzed) # undefault it

def add_footnotes(code,analyzed):
    marks = ''
    if analyzed['I']:
        marks += u'†'
    if analyzed['C']:
        marks += u'‡'
    if analyzed['PR']:
        marks += u'§'
    if not analyzed['B']:
        marks += u'ª'
    if marks:
        return "**%s<sup>%s</sup>**" % (code, marks)
    return "**%s**" % code

FOOTNOTES = {
    u"†": u"""<sup>†</sup>Table also available in racial iterations; add a letter **A-I** to get the racial sub-table:\n
* **A**: White alone
* **B**: Black or African American Alone
* **C**: American Indian and Alaska Native Alone
* **D**: Asian Alone
* **E**: Native Hawaiian and Other Pacific Islander Alone
* **F**: Some Other Race Alone
* **G**: Two or More Races
* **H**: White Alone, Not Hispanic or Latino
* **I**: Hispanic or Latino""",
    u"‡": u"""<sup>‡</sup>Table also available in "collapsed" version: change "B" to "C" for table code.""",
    u"§": u"""<sup>§</sup>Tabulated for Puerto Rico. Add 'PR' to the table code. Column names may vary slightly from non-PR version.""",
    u'ª': u"""<sup>ª</sup>No basic 'B' table is offered."""
}

def build_footnote_explainers(codes):
    analyzed = table_breakdown(codes)
    footnote_explanations = []
    if any(map(lambda x: x['I'],analyzed.values())):
        footnote_explanations.append('')
        footnote_explanations.append(FOOTNOTES[u"†"])
        if not all(map(lambda x: x['B'],analyzed.values())):
            print "WARNING: At least one B table in this set has no root, only iterations"
    if any(map(lambda x: x['C'],analyzed.values())):
        footnote_explanations.append('')
        footnote_explanations.append(FOOTNOTES[u"‡"])

    if any(map(lambda x: x['PR'],analyzed.values())):
        footnote_explanations.append('')
        footnote_explanations.append(FOOTNOTES[u"§"])

    if any(map(lambda x: not x['B'],analyzed.values())):
        footnote_explanations.append('')
        footnote_explanations.append(FOOTNOTES[u"ª"])

    return footnote_explanations

def render_markdown(codes,fltr=None):
    """if Filter is passed, it should be a function which takes 'code,name' and returns True if the table should be in the output"""
    keys = key_tables(codes)
    analyzed = table_breakdown(codes)
    lines = ["| code       | Title                                      |",
             "|------------|--------------------------------------------|"]
    for k in keys:
        analysis = analyzed[make_table_key(k)]
        if fltr is None or fltr(k,table_name(k)):
            lines.append('| %s | %s |' % (add_footnotes(k,analysis), table_name(k)))

    lines.extend(build_footnote_explainers(codes))

    return u"\n".join(lines)


def universe(code):
    return table_data(code)[4]

# un-defaultdict things now that they're initialized
tables_by_code = dict(tables_by_code)

tables_by_release = dict(tables_by_release)

columns_by_release = dict(columns_by_release)

topics = dict(topics)
centopics = dict(centopics)

def find_base_table_data(tabulation_code):
    """There seems to be no strict guarantee that all the tables for a given tabulation code have the same metadata -- in fact, racial iterations definitely will vary -- but this is expedient."""
    for tmpl in ["B%s", "C%s", "B%sA", "C%sA", "B%sPR", "C%sPR", "B%sAPR", "C%sAPR"]:
        try:
            return table_data(tmpl % tabulation_code)
        except:
            pass
    raise Exception("Nothing found for " + tabulation_code)

def compute_shorthand(breakdown):
    s = ""
    for k in sorted(breakdown):
        if breakdown[k]:
            s += k[0]
        else:
            s += '_'
    return s

def remove_iterative_only_text_from_title(table_data):
    table_data[1] = re.sub(r' \(White Alone\)$', '', table_data[1])
    table_data[2] = re.sub(r' \(White Alone\)$', '', table_data[2])
    table_data[1] = re.sub(r'in the Past Year \(White Alone\)', 'in the Past Year', table_data[1])
    table_data[2] = re.sub(r'in the Past Year \(White Alone\)', 'in the Past Year', table_data[2])
    table_data[1] = re.sub(r'Birth \(White Alone\)', 'Birth', table_data[1])
    table_data[2] = re.sub(r'Birth \(White Alone\)', 'Birth', table_data[2])
    table_data[4] = re.sub(r'White Alone Population', 'Specified Race Population', table_data[4])
    table_data[4] = re.sub(r'White Alone Workers', 'Specified Race Workers', table_data[4])
    table_data[4] = re.sub(r'Is White Alone', 'Is A Specified Race', table_data[4])

    return table_data

custom_tabulation_weight = {
    # Suggestions from P. Overberg:
    '17001': '20', # Mentioned as preferred for 'poverty'
    '17002': '19', # Another 'poverty' suggestion
    '21100': '10', # Mentioned for 'veterans' search phrase
}

def generate_unified_table_csv(outputfile="precomputed/unified_metadata.csv"):
    tab_codes = set()
    for release in releases_to_analyze:
        breakdown = table_breakdown(tables_by_release[release])
        tab_codes.update(breakdown.keys())
    h = ['tabulation_code', 'table_title', 'simple_table_title', 'subject_area', 'universe', 'topics', 'weight', 'tables_in_1_yr', 'tables_in_5_yr']
    w = csv.writer(open(outputfile,'w'))
    w.writerow(h)
    for code in sorted(tab_codes):
        base_table_data = find_base_table_data(code)

        if code in ('06004', '07004', '07404', '08105', '08505', '17020', '22005', '23002'):
            base_table_data = remove_iterative_only_text_from_title(base_table_data)

        r = [code, base_table_data[1], base_table_data[2], base_table_data[3], base_table_data[4], base_table_data[6]]

        r.append(custom_tabulation_weight.get(code, '0'))

        for release in releases_to_output:
            if release:
                r.append('{' + ','.join(['"%s"' % t for t in sorted(tables_by_tabulation[release].get(code, []))]) + '}')
            else:
                r.append('{}')
        w.writerow(r)

generate_unified_table_csv()
