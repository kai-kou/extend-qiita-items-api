# extend-qiita-items-api

Qiita記事情報取得APIにViewsとストック数を含める拡張API  

## Description

Qiita APIから記事一覧を取得した場合、Viewsとストック数が取得できないため、それらをまとめて取得できるAPI。  

注意事項として、記事を個別に取得する必要があるため、Qiita APIの利用制限に留意する必要があります。

APIアクセス回数制限

- 認証なし:    60回/h
- 認証あり: 1,000回/h

## Requirement

### requests

Qiita APIにアクセスするために利用しています。

### joblib

記事ごとにViews、ストック数を取得する際に並列で取得するのに利用しています。

### docopt

CLIから実行する際に、パラメータチェックのため利用しています。


## Install

```sh
> git clone https://github.com/kai-kou/extend-qiita-items-api.git
> cd extend-qiita-items-api/src
> pip install -r requirements.txt
```

## Deploy

### Google Cloud Functions

```sh
> cd extend-qiita-items-api/src
> gcloud functions deploy extend_qiita_get_items_api \
  --runtime=python37\
  --region=asia-northeast1 \
  --memory=512MB \
  --trigger-http
```

## Usage

### ローカル

```sh
> python get_qiita_items.py アクセストークン --page=1 --per_page=20
```

### Cloud Functions

```sh
> curl https://us-central1-[GCPプロジェクトID].cloudfunctions.net/extend_qiita_get_items_api?token=[Qiitaのアクセストークン]?page=1&per_page=20
```

```sh
> curl -sSLH "Authorization: Bearer [Qiitaのアクセストークン]" https://us-central1-[GCPプロジェクトID].cloudfunctions.net/extend_qiita_get_items_api?page=1&per_page=20
```

## Document
