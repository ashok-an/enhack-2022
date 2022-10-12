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
       resource=Resource.create({SERVICE_NAME: "bugs.svc"})
)
jaeger_exporter = JaegerExporter(
   agent_host_name="jaeger",
   agent_port=6831,
)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

#def request_hook(span: Span, environ: WSGIEnvironment):
#    if span and span.is_recording():
#        span.set_attribute("custom_user_attribute_from_request_hook", "some-value")

#def response_hook(span: Span, status: str, response_headers: List):
#    if span and span.is_recording():
#        span.set_attribute("custom_user_attribute_from_response_hook", "some-value")

FlaskInstrumentor().instrument_app(app, tracer_provider=provider)
#FlaskInstrumentor().instrument_app(app, tracer_provider=provider, request_hook=request_hook, response_hook=response_hook)

@app.route("/")
def hello():
    return "Hello from bugs!"

import db

@app.route("/bugs/<bug_id>")
def get_bugs(bug_id):
  bug_id = None if not bug_id.startswith('BUG') else bug_id
  bugs = db.get_bugs(bug_id)
  print(f"bugs: {bugs}")
  return {'bugs': bugs}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=12345)

