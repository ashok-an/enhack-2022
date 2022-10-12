from flask import Flask
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.trace.span import Span

app = Flask(__name__)

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
   BatchSpanProcessor,
   ConsoleSpanExporter,
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider(
       resource=Resource.create({SERVICE_NAME: "notes.svc"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="jaeger",
   agent_port=6831,
)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

FlaskInstrumentor().instrument_app(app, tracer_provider=provider)

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

@app.route("/")
def hello():
    return "Hello from notes!"

import db
import requests

@tracer.start_as_current_span("get-bugs")
def get_bug(bug_id):
  current_span = trace.get_current_span()
  current_span.set_attribute("bug.id", bug_id)
  current_span.add_event(f"fetching bugs for bug_id:{bug_id}")
  r = requests.get(f"http://bugs:12345/bugs/{bug_id}")
  current_span.add_event(f"+ done fetching bugs for bug_id:{bug_id}")
  return r.json()

@app.route("/notes/<bug_id>", methods=['GET'])
def get_bugs(bug_id):
  notes = db.get_notes(bug_id=bug_id)
  if not notes:
    current_span = trace.get_current_span()
    current_span.set_status(Status(StatusCode.ERROR))
    return {}, 400

  bug = get_bug(bug_id)
  print(f"bug={bug}, notes={notes}")
  return {'data': {'bug': bug}}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=23456)

