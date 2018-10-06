from extend_qiita_api import *

from docopt import docopt


# use CLI
if __name__ == '__main__':
  _USAGE = '''
  Qiita APIから記事情報をViewsとストック数を含めて取得する
  Usage:
    get_qiita_items.py <qiita_api_token> [options]
    get_qiita_items.py --help

  Options:
    --page=<n>               ページ番号 (1から100まで)
    --per_page=<n>           1ページあたりに含まれる要素数 (1から100まで)
  '''

  options = docopt(_USAGE)

  qiita_api_token = options['<qiita_api_token>']
  page = options['--page']
  per_page = options['--per_page']

  response = get_items(qiita_api_token, page, per_page)
  print(json.dumps(response))
