from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
   BatchSpanProcessor,
   ConsoleSpanExporter,
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from pymongo import MongoClient
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

import datetime
import logging

# Setup tracing
_provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "mongo.bugs.svc"})
)
_jaeger_exporter = JaegerExporter(
   agent_host_name="jaeger",
   agent_port=6831,
)

_processor = BatchSpanProcessor(ConsoleSpanExporter())
_provider.add_span_processor(BatchSpanProcessor(_jaeger_exporter))
PymongoInstrumentor().instrument(tracer_provider=_provider)

client = MongoClient('mongodb://mongo:27017')
db = client.db0
bugs = db.bugs
notes = db.notes

def add_bug(_id, title, engineer):
  data = {'_id': _id, 'title': title, 'engineer': engineer, 'timestamp': datetime.datetime.utcnow()}
  logging.info("bugs.add({data})")
  bugs.insert_one(data)

def add_note(_id, bug_id, note):
  data = {'_id': _id, 'bug_id': bug_id, 'note': note, 'timestamp': datetime.datetime.utcnow()}
  logging.info(f"notes.add({data})")
  notes.insert_one(data)

import bson

def convert(data):
  return bson.json_util.dump(data)

def get_bugs(bug_id=None):
  if bug_id:
    r = bugs.find({'_id': bug_id})
  else:
    r = bugs.find({}, limit=10)
  logging.info("bugs.get({bug_id})={r}")
  return list(r)
  return [convert(i) for i in r]

def get_notes(bug_id):
  r = notes.find({'bug_id': bug_id}, limit=10)
  logging.info("notes.get({bug_id})={r}")
  return list(r)
  return [convert(i) for i in r]


if __name__ == '__main__':
  print(get_bugs())
  print(get_notes('CSC13471'))
