#!/usr/bin/env python

import argparse
import pprint
import os
import random

import pymongo
from essential_generators import DocumentGenerator

def get_id(prefix='BUG'):
    return prefix + str(random.randint(1000, 9999))

def get_name():
    names = ['andy', 'brandy', 'cindy', 'mindy', 'randy', 'sandy']
    return random.choice(names)

def get_time():
    day = random.choice(['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    hour = random.randint(10, 23)
    min_ = random.randint(10, 59)
    return f'{day} {hour}:{min_}'

def gen_bugs(count):
    gen = DocumentGenerator()
    template = {
        '_id': get_id,
        'title': 'sentence',
        'severity': [1, 2, 3, 4, 5, 6],
        'engineer': get_name,
        'headline': 'sentence',
        'description': 'paragraph',
        'url': 'url',
        'age': 'small_int',
        'component': ['frontend', 'backend', 'middleware', 'infra', 'others'],
    }
    gen.set_template(template)
    documents = gen.documents(count)
    return documents

mongodb_host = os.getenv('MONGODB_HOST') or "localhost"
mongodb_port = os.getenv('MONGODB_PORT') or "27017"
client = pymongo.MongoClient(f'mongodb://{mongodb_host}:{mongodb_port}/')
db = client["db0"]

def seed_bugs(bug_list):
    bugs = db["bugs"]

    for bug in bug_list:
        try:
            bugs.insert_one(bug)
        except Exception as e:
            print(f'Insert failed for bug:{bug.get("_id")}. Exception={e}')
        else:
            print(f'+ Inserted bug:{bug.get("_id")}')
    

def seed_notes(bug_id):
    gen = DocumentGenerator()
    note_list = []
    for i in range(random.randint(1, 10)):
        note_list.append({
                'bug_id': bug_id, 
                'note': gen.sentence(),
                'time': get_time(),
                'user': get_name()
        })

    notes = db["notes"]
    x = notes.insert_many(note_list)
    print(f'+ Added {len(x.inserted_ids)} notes for bug:{bug_id}')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', help='Number of records to generate', type=int, required=True)

    args = parser.parse_args()
    bugs = gen_bugs(args.count)

    seed_bugs(bugs)
    for i in bugs:
        c = random.choice([True, False])
        if c:
            seed_notes(i.get('_id'))
        else:
            print(f'- Skip notes for bug:{i.get("_id")}')
