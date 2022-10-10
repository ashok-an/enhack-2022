##### To run normally
`python app.py`

##### To run through opentelemetry
```
opentelemetry-instrument \
    --traces_exporter console \
    --metrics_exporter console \
    flask run
```
