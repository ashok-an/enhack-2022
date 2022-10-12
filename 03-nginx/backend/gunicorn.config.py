from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

bind = "backend:5000"

# Sample Worker processes
workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Sample logging
errorlog = "-"
loglevel = "info"
accesslog = "-"
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    resource = Resource.create(attributes={"service.name": "api-service"})

    trace.set_tracer_provider(TracerProvider(resource=resource))
    # This uses insecure connection for the purpose of example. Please see the
    # OTLP Exporter documentation for other options.
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://collector:4317", insecure=True)
    )
    trace.get_tracer_provider().add_span_processor(span_processor)
