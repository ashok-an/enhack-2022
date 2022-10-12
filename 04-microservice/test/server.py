# server.py
from collections import defaultdict

import requests

from flask import Flask, request

app = Flask(__name__)
CACHE = defaultdict(int)

from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor


# SpanExporter receives the spans and send them to the target location.
exporter = JaegerSpanExporter(
    service_name="service-example",
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchExportSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

@app.route("/")
def fetch():
  url = request.args.get("url")
  CACHE[url] += 1
  resp = requests.get(url)
  return resp.content

@app.route("/cache")
def cache():
  keys = CACHE.keys()
  return "{}".format(keys)

if __name__ == "__main__":
  app.run()
