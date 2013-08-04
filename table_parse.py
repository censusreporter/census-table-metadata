# Scratch code to "factor" table names into some sort of matrix.
#
# table IDs are always 6 long, unless:
#   racial or puerto rican subclass
#   a handful of imputation tables
# 
# more cleanup: field names, inconsistent with colons such as 
# potential table filters:
#   'in puerto rico' (de facto all ending in 'PR')
#   'in united states' (opposite of above, but also five more tables whose names indicate 'IN THE UNITED STATES')
#   'technical tables': 2 unweighted counts; 10 quality measures; 97 imputations
#   racial breakdowns

import re
from titlecase import titlecase
from collections import defaultdict
import csv
import sys

def load_rows(): # a bunch of other things in here expect data in a common format that this produces.
    # specifically, table_id, table_name, universe, subject_area 
    table_data = defaultdict(dict)
    r = csv.reader(open("acs2011_1yr_Sequence_Number_and_Table_Number_Lookup.csv"))
    headers = r.next()
    for fileid,table_id,seq,line_number,position,cells,total,table_title,subject_area in r:
        if line_number: continue # skip rows with a line number as unimportant to this process
        if 'universe' in table_title.lower():
            table_data[table_id]['universe'] = table_title.split(':')[-1].strip()
        else:
            table_data[table_id]['title'] = table_title
            table_data[table_id]['subject_area'] = subject_area

    rows = []
    for table_id in sorted(table_data):
        data = table_data[table_id]
        rows.append((table_id,data['title'],data['universe'],data['subject_area']))
    return rows

SUBJECT_AREA_TO_TOPICS = {
    'Age-Sex': 'age, sex',
    'Hispanic Origin': 'race',
    'Race': 'race',

    'Earnings': 'income',
    'Employment Status': 'employment',
    'Health Insurance': 'health insurance',
    'Income': 'income',
    'Industry-Occupation-Class of Worker': 'employment',
    'Journey to Work': 'commute',
    'Poverty': 'poverty',
    'Transfer Programs': 'public assistance',

    'Ancestry': 'ancestry',
    'Children - Relationship': 'children',
    'Disability': 'disability',
    'Educational Attainment': 'education',
    'Fertility': 'fertility',
    'Foreign Birth': 'place of birth',
    'Grand(Persons) - Age of HH Members': 'children, grandparents',
    'Households - Families': 'families',
    'Language': 'language',
    'Marital Status': 'marital status',
    'Place of Birth - Native': 'place of birth',
    'Residence Last Year - Migration': 'migration',
    'School Enrollment': 'education',
    'Veteran Status': 'veterans',

    'Housing': 'housing',
    'Unweighted Count': 'technical',
    'Group Quarters': 'group quarters',
    'Quality Measures': 'technical',
    'Imputations': 'technical',
}

TABLE_NAME_TEXT_TO_TOPICS = {
    'ancestry': 'ancestry',
    'race': 'race',
    'total population': 'age, sex',
    'children': 'children',
    'disability': 'disability',
    'bachelor\'s degree': 'education',
    'education': 'education',
    'school': 'education',
    'employ': 'employment',
    'occupation': 'employment',
    'work': 'employment',
    'families': 'families',
    'family': 'families',
    'grandparent': 'grandparents',
    'health insurance': 'health insurance',
    'living arrang': 'families',
    'household': 'families',
    'earnings': 'income',
    'income': 'income',
    'geographical mobility': 'migration',
    'poverty': 'poverty',
    'food stamps': 'public assistance',
    'public assistance': 'public assistance',
    '65 years and over': 'seniors',
    'va health care': 'veterans',
    'veteran': 'veterans',
    'means of transportation': 'commute',
    'travel time': 'commute',
    'vehicles': 'commute',
    'workplace geography': 'commute',
    'time leaving home': 'commute',
    'imputation': 'technical',
    'unweighted': 'technical',
    'coverage rate': 'technical',
    'nonresponse rate': 'technical',
    'movers': 'migration',
    'place of work': 'commute',
    'workers': 'employment',
    'group quarters': 'group quarters',
    'had a birth': 'fertility',
    'income deficit': 'poverty',
    'difficulty': 'disability',
    'disabilities': 'disability',
    'tricare': 'health insurance',
    'medicare': 'health insurance',
    'medicaid': 'health insurance',
    'va health care': 'health insurance',
    'gross rent': 'costs and value',
    'contract rent': 'costs and value',
    'rent asked': 'costs and value',
    'price asked': 'costs and value',
    'value': 'costs and value',
    'utilities': 'costs and value',
    'costs': 'costs and value',
    'real estate taxes': 'costs and value',
    'rooms': 'physical characteristics', # including bedrooms
    'facilities': 'physical characteristics',
    'heating': 'physical characteristics',
    'units in structure': 'physical characteristics',
    'year structure built': 'physical characteristics',
    'tenure': 'tenure',
    'moved into unit': 'tenure',
    'occupan': 'occupancy', # add vacancy to topic?
    'vacan': 'occupancy',
    'mortgage': 'mortgage',
    'under 18 years': 'children',
    'family type': 'families',
    'household': 'families',
}

TABLE_NAME_TEXT_TO_FACETS = {
    'by age': 'age',
    'age by': 'age',
    'citizenship': 'citizenship',
    'naturalization': 'citizenship, place of birth',
    'by famil': 'family type',
    'by sex': 'sex',
    'sex by': 'sex',
    # 'by household': 'household type',
    # 'household type by': 'household type',
    'language': 'language',
    'marriage': 'marital status',
    'marital': 'marital status',
    'nativity': 'place of birth',
    'place of birth': 'place of birth',
    'by relationship': 'relationship type',
    '(white': 'race',
    '(black': 'race',
    'american indian': 'race',
    'asian alone': 'race',
    'alaska native': 'race',
    'native hawaiian': 'race',
    'some other race': 'race',
    'two or more races': 'race',
    'hispanic': 'race',
}

        
SUBTABLE_STRINGS = [ 
 re.compile('\(AMERICAN INDIAN AND ALASKA NATIVE ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(AMERICAN INDIAN AND ALASKA NATIVE ALONE\)',re.IGNORECASE),
 re.compile('\(ASIAN ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(ASIAN ALONE\)',re.IGNORECASE),
 re.compile('\(BLACK OR AFRICAN AMERICAN ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(BLACK OR AFRICAN AMERICAN ALONE\)',re.IGNORECASE),
 re.compile('\(NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(NATIVE HAWAIIAN AND OTHER PACIFIC ISLANDER ALONE\)',re.IGNORECASE),
 re.compile('\(SOME OTHER RACE ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(SOME OTHER RACE ALONE\)',re.IGNORECASE),
 re.compile('\(WHITE ALONE HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(WHITE ALONE\)',re.IGNORECASE),
 re.compile('\(WHITE ALONE, NOT HISPANIC OR LATINO HOUSEHOLDER\)',re.IGNORECASE),
 re.compile('\(WHITE ALONE, NOT HISPANIC OR LATINO\)',re.IGNORECASE),
 re.compile('\(Hispanic or Latino\)',re.IGNORECASE),
 re.compile('\(Two or More Races\)',re.IGNORECASE),
 re.compile('\(Hispanic or Latino Householder\)',re.IGNORECASE),
 re.compile('\(Two or More Races Householder\)',re.IGNORECASE),
]

def strip_subtable_string(table_name):
    for pattern in SUBTABLE_STRINGS:
        if pattern.search(table_name):
            table_name = re.sub(pattern,'',table_name)
            table_name = table_name.strip()
            return re.sub('\s+',' ',table_name)
    return table_name.strip()
    
def build_subtable_map(rows):
    """
    outlier: a PR table with no corresponding US table (relates to B06010/B06010PR) only seems to omit income levels for foreign born. can we just skip this one?
    ('C06010PR',
      'PLACE OF BIRTH BY INDIVIDUAL INCOME IN THE PAST 12 MONTHS (IN 2011 INFLATION-ADJUSTED DOLLARS) IN PUERTO RICO',
      'Population 15 years and over in Puerto Rico')
    """
    SUBTABLE_PATTERN = re.compile('^(\w+\d+)(\w+)$')
    smap = defaultdict(dict)
    for x in rows:
        table_id = x[0]
        if table_id[-1].isalpha():
            base_table_id, code = SUBTABLE_PATTERN.match(table_id).groups()
            smap[base_table_id][code] = x
    for x in rows: # there seem to be 18 out of 111 'subtable groups' which don't have a 'root'
        if x[0] in smap:
            smap[x[0]]['root'] = x
    return smap
    
def prune_subtables(rows):
    """Partition off all table codes which end in alphabetic (racial subgroup or puerto rico) and any tables which are 'parents' to those."""
    rows = list(rows)
    smap = build_subtable_map(rows)
    for v in smap.values():
        for tup in v.values():
            rows.remove(tup)
    return rows, smap

UNIVERSE_FIXES = [
    (re.compile(r'^amilies',re.IGNORECASE),'Families'),
    (re.compile(r'^ative',re.IGNORECASE),'Native'),
    (re.compile(r'^enter-',re.IGNORECASE),'Renter-'),
    (re.compile(r'^hite',re.IGNORECASE),'White'),
    (re.compile(r'^ispanic',re.IGNORECASE),'Hispanic'),
    (re.compile(r'^ivilian',re.IGNORECASE),'Civilian'),
    (re.compile(r'^lack',re.IGNORECASE),'Black'),
    (re.compile(r'^merican',re.IGNORECASE),'American'),
    (re.compile(r'^ome',re.IGNORECASE),'Home'),
    (re.compile(r'^opulation',re.IGNORECASE),'Population'),
    (re.compile(r'^oreign',re.IGNORECASE),'Foreign'),
    (re.compile(r'^orkers',re.IGNORECASE),'Workers'),
    (re.compile(r'^otal',re.IGNORECASE),'Total'),
    (re.compile(r'^ousing',re.IGNORECASE),'Housing'),
    (re.compile(r'^sian',re.IGNORECASE),'Asian'),
    (re.compile(r'^wn',re.IGNORECASE),'Own'),
    (re.compile(r'^wo',re.IGNORECASE),'Two'),
]
def fix_universe(univ):
    for pat,rep in UNIVERSE_FIXES:
        if pat.search(univ):
            return re.sub(pat,rep,univ)
    return univ
    
def prune_technical(rows):
    rows = list(rows)
    tech = [x for x in rows if x[0][1:3] in ['00','98','99']]
    for x in tech:
        rows.remove(x)
    return rows, tech
    
def megapruned(rows):
    rows, smap = prune_subtables(rows)
    rows, tech = prune_technical(rows)
    return rows,smap,tech
    
"""
Exactly 7 tables have the word 'FOR' more than once. 3 are imputation tables. The other 4:

[('B10010',
  'MEDIAN FAMILY INCOME FOR FAMILIES WITH GRANDPARENT HOUSEHOLDERS AND/OR SPOUSES LIVING WITH OWN GRANDCHILDREN UNDER 18 YEARS BY RESPONSIBILITY FOR OWN GRANDCHILDREN AND PRESENCE OF PARENT OF GRANDCHILDREN',
  'amilies with grandparent householders and/or spouses living with grandchildren'),
 ('B10050',
  'GRANDPARENTS LIVING WITH OWN GRANDCHILDREN UNDER 18 YEARS BY RESPONSIBILITY FOR OWN GRANDCHILDREN BY LENGTH OF TIME RESPONSIBLE FOR OWN GRANDCHILDREN FOR THE POPULATION 30 YEARS AND OVER',
  'Population 30 years and over'),
 ('B15010',
  "DETAILED FIELD OF BACHELOR'S DEGREE FOR FIRST MAJOR FOR THE POPULATION 25 YEARS AND OVER",
  "POPULATION 25 YEARS AND OVER WITH A BACHELOR'S DEGREE OR HIGHER ATTAINMENT"),
 ('B15011',
  "SEX BY AGE BY FIELD OF BACHELOR'S DEGREE FOR FIRST MAJOR FOR THE POPULATION 25 YEARS AND OVER",
  "POPULATION 25 YEARS AND OVER WITH A BACHELOR'S DEGREE OR HIGHER ATTAINMENT")]

"""    
def factor_table_name(table_name):
    """From some experiments at factoring table_names to tease out topics"""
    table_name = strip_subtable_string(table_name)
    d = { 'original_name': table_name, 'components': [] }
    parts = table_name.rsplit(' FOR ',1) # see above; sometimes 'FOR' appears more than once
    if len(parts) == 2:
        d['universe_from_name'] = parts[1]
        table_name = parts[0]
    for component in re.split(re.compile(r'\bby\b',re.IGNORECASE),table_name):
        d['components'].extend(re.split(re.compile(r'\band\b',re.IGNORECASE),component))
    d['components'] = map(lambda x: x.strip(),d['components'])
    return d

def unique_clean_table_names(by_length=False):
    """A handy utility while exploring data"""
    tns  = set(x[2] for x in build_pretty_table())
    simpler = set(map(strip_subtable_string,tns))
    if by_length:
        tups = [(len(x),x) for x in simpler]
        tups.sort()
        tups.reverse()
        return [x[-1] for x in tups]
    return sorted(simpler)

TABLE_NAME_REPLACEMENTS = [ # mostly problems with slashes and -- characters
    (r'minor Civil Division Level for 12 Selected States \(Ct, Me, Ma, Mi, Mn, Nh, Nj, Ny, Pa, Ri, Vt, Wi\)',
        'Minor Civil Division Level for 12 Selected States (CT, ME, MA, MI, MN, NH, NJ, NY, PA, RI, VT, WI)'),
    (r'/snap','/SNAP'),
    (r'\(Ssi\)','(SSI)'),
    (r'Va Health Care',r'VA Health Care'),
    (r'Medicaid/means-tested',r'Medicaid/Means-tested'),
    (r'/military',r'/Military'),
    (r'--metropolitan',r'--Metropolitan'),
    (r'--micropolitan',r'--Micropolitan'),
    (r'--place Level',r'--Place Level'),
    
    (r'--state',r'--State'),
    (r'\(Aian\)',r'(AIAN)'),
]

COLLOQUIAL_REPLACEMENTS = [
    (re.compile(r'in the Past 12 Months'),''),
    (re.compile(r'\(In \d{4} Inflation-adjusted Dollars\)',re.IGNORECASE),''),
    (re.compile('for the Population \d+ Years and Over',re.IGNORECASE), ''),
    (re.compile('Civilian Employed Population 16 Years and Over',re.IGNORECASE),'Civilian Population'),
    (re.compile(r'((grand)?children) Under 18 Years',re.IGNORECASE),r'\1'), 
    (re.compile(r'Women \d+ to \d+ Years Who Had a Birth'),'Women Who Had a Birth'),
    (re.compile(r'Field of Bachelor\'s Degree for First Major the Population 25 Years and Over',re.IGNORECASE),'Field of Bachelor\'s Degree for First Major'),
    (re.compile(r'Married Population 15 Years and Over',re.IGNORECASE),'Married Population'),
    (re.compile(r'Population 16 Years and Over',re.IGNORECASE),'Population'), # seems to always have to do with employment, where I think we can take the age for granted
    (re.compile(r'Place of Work for Workers 16 Years and Over',re.IGNORECASE),'Place of Work'),
    (re.compile(r'For Workplace Geography',re.IGNORECASE),''),
    (re.compile(r'\(In Minutes\)',re.IGNORECASE),''),
]    

def build_topics(table_name, subject_area=None):
    all_areas = set()
    if subject_area:
        all_areas.update(map(lambda x: x.strip(),SUBJECT_AREA_TO_TOPICS[subject_area].split(',')))
    for k,v in TABLE_NAME_TEXT_TO_TOPICS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x: x.strip(),v.split(',')))
    for k,v in TABLE_NAME_TEXT_TO_FACETS.items():
        if k in table_name.lower():
            all_areas.update(map(lambda x:x.strip(),v.split(',')))
    return sorted(set(map(lambda x: x.strip(), all_areas)))

def clean_table_name(table_name):
    """ title case, strip bogus white space, a few observed direct fixes for title casing..."""
    table_name = re.sub('\s+',' ',table_name) # some have multiple white spaces
    table_name = titlecase(table_name.lower())
    for problem,fix in TABLE_NAME_REPLACEMENTS:
        table_name = re.sub(problem,fix,table_name)
    return table_name.strip()

def simplified_table_name(table_name):
    """Make some editorial choices about how to simplify table names for more casual use"""
    for regexp,substitution in COLLOQUIAL_REPLACEMENTS:
        table_name = re.sub(regexp,substitution,table_name)
    table_name = re.sub('\s+',' ',table_name)
    return table_name.strip()

def build_pretty_table():
    x = []
    for table_id, table_name, universe, subject_area in load_rows():
        table_id = table_id.strip()     
        table_name = clean_table_name(table_name)
        simple_name = simplified_table_name(table_name)
        universe = titlecase(fix_universe(universe.lower()))
        topics = build_topics(table_name,subject_area)
        topics = '|'.join(topics)
        x.append([table_id,table_name,simple_name,universe,topics])
    return x

def find_dependent_upon_subject_area():
    rows = build_pretty_table()
    problems = []
    for row in rows:
        if row[0].endswith('08202'): continue # Journey to Work but not commute so don't bug me
        old_topics = set(row[-1].split('|'))
        new_topics = set(build_topics(row[1]))
        if new_topics != old_topics:
            diff = old_topics.difference(new_topics)
            if 'housing' in diff: continue # we're losing that one happily
            if 'fertility' in diff: continue # that one checks out
            if 'children' in diff: continue # that one checks out
            problems.append((row,diff))
    return problems

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        w = csv.writer(open(filename,"w"))
    except IndexError:
        print "No filename specified, writing to standard out"
        w = csv.writer(sys.stdout)
    w.writerow(['table_id','table_title','colloquial_title','universe','topics'])
    w.writerows(build_pretty_table())

