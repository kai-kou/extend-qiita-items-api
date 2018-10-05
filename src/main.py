from extend_qiita_api import *

from flask import make_response, jsonify


# use Google Cloud Functions
def extend_qiita_get_items_api(request):
  # APIトークンを取得する
  request_json = request.get_json()
  token = request.headers.get("Authorization")
  if token:
    token = token.replace('Bearer ', '')
  elif request.args and 'token' in request.args:
    token = request.args.get('token')
  else:
    token = request_json['token']

  # オプションパラメータを取得する
  page = None
  per_page = None
  if request.args and 'page' in request.args:
    page = request.args.get('page')
  elif request_json and 'page' in request_json:
    page = request_json['page']

  if request.args and 'per_page' in request.args:
    per_page = request.args.get('per_page')
  elif request_json and 'per_page' in request_json:
    per_page = request_json['per_page']

  response = get_items(token, page, per_page)
  return make_response(jsonify(response), 200)
