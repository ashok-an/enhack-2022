1. Initialize 
`opentelemetry-bootstrap -a install`

2. Run
```
 opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    flask run
```
