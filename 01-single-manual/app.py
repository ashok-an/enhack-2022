import datetime
import logging
import requests

import flask

######################
## initialization
######################
app = flask.Flask(__name__)
start = datetime.datetime.now()
_url = 'https://dummyjson.com/products'

######################
## logging
######################
from flask.logging import default_handler

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)


######################
## routes
######################
@app.route('/', methods=['GET'])
def root():
  return flask.jsonify({'message': 'flask app root/'})

@app.route('/healthz', methods=['GET'])
def healthz():
  now = datetime.datetime.now()
  return flask.jsonify({'message': f'up and running since {(now - start)}'})

@app.route('/products', methods=['GET'])
def products():
  r = requests.get(_url)
  if not r.status_code == 200:
    return flask.jsonify({'error': 'product list failed'}), 500

  return flask.jsonify(r.json())

@app.route('/search/<_id>', methods=['GET'])
def search(_id):
  r = requests.get(f'{_url}/search?q={_id}&limit=10&select=title,price')
  if not r.status_code == 200:
    return flask.jsonify({'error': 'product search failed'}), 500

  return flask.jsonify(r.json())


######################
if __name__ == '__main__':
######################
  app.run(debug=True, host='0.0.0.0', port=5000)
