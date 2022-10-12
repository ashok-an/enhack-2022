from flask import Flask, request
import math

from jaeger_client import Config
from flask_opentracing import FlaskTracing

application = Flask(__name__)


jconfig = Config(
        config={
            "logging": True,
            "reporter_batch_size": 1,
            "local_agent": {"reporting_host": "jaeger"},
            "sampler": 
            {
                "type": "const",
                "param": 1
             }
           },
        service_name="service")
jaeger_tracer = jconfig.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, application)

plist = []

@tracing.trace()
@application.route("/")
def inc_hits():
    spandata = {}
    if len(plist) > 0:
        spandata["previous_prime"] = plist[-1]
    find_next_prime()
    spandata['calculated_prime'] = plist[-1]
    with jaeger_tracer.start_active_span('inc_hits_span') as scope:
        scope.span.log_kv(spandata)
    return "current prime: " + str(plist[-1])


def find_next_prime():
    global plist
    if len(plist) == 0:
        plist = [2]
        return
    outnum = plist[-1]
    while True:
        outnum = outnum + 1
        found_factor = False
        sqrt_outnum = math.ceil(math.sqrt(outnum))
        for y in plist:
            if y > sqrt_outnum:
                break
            if outnum % y == 0:
                found_factor = True
                break
        if not found_factor:
            plist += [outnum]
            return

if __name__ == "__main__":
    application.run("backend", port=5000)
