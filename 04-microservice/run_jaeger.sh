#!/bin/bash
docker rm -f jaeger
docker run --name jaeger -d -p 6831:6831/udp -p 16686:16686 jaegertracing/all-in-one:latest
