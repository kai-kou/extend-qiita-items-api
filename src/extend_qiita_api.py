import requests

import json

from joblib import Parallel, delayed


BASE_API_URL = 'https://qiita.com//api/v2/'


def get_items(qiita_api_token, page=1, per_page=20):
  """Qiita APIを利用して記事一覧を取得する
  Args:
        qiita_api_token (string): Qiitaのアプリケーショントークン
        page (int): ページ番号 (1から100まで)
        per_page (int): 1ページあたりに含まれる要素数 (1から100まで)
  """
  headers = {'Authorization': f'Bearer {qiita_api_token}'}
  params = {}
  if page != None:
    params['page'] = page
  if per_page != None:
    params['per_page'] = per_page

  itemsUrl = f'{BASE_API_URL}authenticated_user/items'
  itemsRes = requests.get(itemsUrl, headers=headers, params=params)
  itemsRes.raise_for_status()

  # 記事ごとにViewsとストック数を取得する
  items = json.loads(itemsRes.text)
  items = Parallel(n_jobs=-1, verbose=0)(
    [delayed(get_item_detail)(headers, item) for item in items])

  return items


def get_item_detail(headers, item):
  """Qiita APIを利用してViewsとストック数を含めて記事を取得する
  Args:
        headers (dict): アクセストークンを含めたリクエストヘッダー情報
        item (dict): Qiitaの記事情報
  """
  itemId = item['id']

  itemUrl = f'{BASE_API_URL}items/{itemId}'
  try:
    # 認証された状態で記事を取得するとViewsが取得できる
    itemRes = requests.get(itemUrl, headers=headers)
    itemRes.raise_for_status()
    authenticatedItem = json.loads(itemRes.text)
    item['page_views_count'] = authenticatedItem['page_views_count']

    # 記事IDからストック数を取得する
    stokersUrl = f'{BASE_API_URL}items/{itemId}/stockers'
    stokersRes = requests.get(stokersUrl, headers=headers)
    stokersRes.raise_for_status()
    item['stockers_count'] = int(stokersRes.headers.get('Total-Count'))

  finally:
    # エラーが発生したら無視して返す
    return item
