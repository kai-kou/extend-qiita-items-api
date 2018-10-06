# extend-qiita-items-api

Qiita記事情報取得APIにViewsとストック数を含める拡張API  

## Description

Qiita APIから記事一覧を取得した場合、Viewsとストック数が取得できないため、それらをまとめて取得できるAPIです。  

利用したQiita APIは以下となります。  

Qiita API v2 ドキュメント  
https://qiita.com/api/v2/docs#%E6%8A%95%E7%A8%BF

- GET /api/v2/authenticated_user/items
- GET /api/v2/items/:item_id

注意事項として、記事を個別に取得する必要があるため、Qiita APIの利用制限に留意する必要があります。  

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

### AWS Lambda

```sh
> aws configure

> aws iam create-role --role-name extend_qiita_api_exec_role \
  --assume-role-policy-document settings/role-policy.json

> aws iam get-role --role-name extend_qiita_api_exec_role

> aws iam get-policy --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"

> aws iam attach-role-policy --role-name extend_qiita_api_exec_role \
  --policy-arn "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"

> aws iam list-attached-role-policies --role-name extend_qiita_api_exec_role

> cd extend-qiita-items-api/src

> pip install -r requirements.txt -t deploy

> cp *.py deploy

> cd deploy

> zip -r lambda.zip *

> aws lambda create-function \
--function-name extend_qiita_api \
--region ap-northeast-1 \
--zip-file fileb://lambda.zip \
--role arn:aws:iam::xxxxxxxxxxxx:role/extend_qiita_api_exec_role \
--handler lambda_handler.lambda_handler \
--runtime python3.6 \
--timeout 300 \
--memory-size 1024
```

## Usage

### ローカル

```sh
> python get_qiita_items.py [Qiitaのアクセストークン] --page=1 --per_page=20
```

### Cloud Functions or AWS Lambda

```sh
> curl https://[endpoint]?token=[Qiitaのアクセストークン]&page=1&per_page=20
```

```sh
> curl -sSLH "Authorization: Bearer [Qiitaのアクセストークン]" \
  https://[endpoint]?page=1&per_page=20
```

## Document

Qiita APIを利用して記事のViewsとストック数がまとめて取得できるAPIを作ってみた
https://qiita.com/kai_kou/items/3f10ce93f4aa3b57b2d0