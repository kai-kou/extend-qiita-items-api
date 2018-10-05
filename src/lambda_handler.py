from extend_qiita_api import *

import json


def lambda_handler(event, context):
  request_json = event
  request = event
  token = None
  queryStringParameters = {}
  if request and 'queryStringParameters' in request:
    queryStringParameters = request.get('queryStringParameters')

  if request and 'headers' in request:
    token = request['headers'].get("Authorization")

  if token:
    token = token.replace('Bearer ', '')
  elif queryStringParameters and 'token' in queryStringParameters:
    token = queryStringParameters.get('token')
  else:
    token = request_json['token']

  # オプションパラメータを取得する
  page = None
  per_page = None
  if queryStringParameters and 'page' in queryStringParameters:
    page = queryStringParameters.get('page')
  elif request_json and 'page' in request_json:
    page = request_json['page']

  if queryStringParameters and 'per_page' in queryStringParameters:
    per_page = queryStringParameters.get('per_page')
  elif request_json and 'per_page' in request_json:
    per_page = request_json['per_page']

  response = get_items(token, page, per_page)

  return {
    'statusCode': '200',
    'body': json.dumps(response, ensure_ascii=False),
    'headers': {
      'Content-Type': 'application/json',
    },
  }
