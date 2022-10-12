import json
import random
import os
import time

import redis
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
#from flask_api_cache import ApiCache

app = Flask(__name__)

for i in ['MONGODB_URI', 'REDIS_HOST', 'REDIS_PORT']:
    print(f"Env var: {i}={os.getenv(i)}")
 
app.config["MONGO_URI"] = os.getenv('MONGODB_URI') or "mongodb://mongo:27017/db0"
mongo = PyMongo(app)

redis_host = os.getenv('REDIS_HOST') or 'redis'
redis_port = os.getenv('REDIS_PORT') or '6379'
redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port))

@app.route('/')
def root():
    return jsonify({'message': 'Valid route is /notes/<bug_id>'})

@app.route('/ping')
def ping():
    return jsonify({'message': 'pong'})

@app.route('/_bugs')
def get_bugs_with_notes():
    data = list(mongo.db.notes.find({}, limit=20))
    bugs = sorted(set([i.get('bug_id') for i in data]))
    return jsonify({'bugs': bugs})

@app.route('/notes/<bug_id>')
#@ApiCache(redis=redis_instance, expired_time=15)
def get_notes(bug_id):

    time.sleep(random.uniform(0.5, 2.0))

    data = list(mongo.db.notes.find({'bug_id': bug_id}, {'_id': 0, 'bug_id': 0}))
    if data:
        return jsonify({'bug_id': bug_id, 'notes': data[:10]})
    else:
        return {'error': f'No notes found for bug_id:{bug_id}'}, 404
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=23456)
