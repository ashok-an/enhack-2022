FROM python:3-slim
COPY ./requirements.txt requirements.txt
COPY ./app.py app.py
COPY ./gunicorn.config.py gunicorn.config.py
RUN pip install -r requirements.txt
CMD python app.py
