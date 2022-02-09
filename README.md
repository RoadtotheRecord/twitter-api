# Road to the Record API
## セットアップ
たぶん環境次第でやり方変わってくるので迷ったら @gunimus に聞いてください
1. [Docker](https://www.docker.com/get-started) 入れる
1. このリポジトリをチェックアウトする
1. チェックアウトしてきたディレクトリで
    1. `docker-compose build`
    1. `docker-compose up`
1. ブラウザで `http://localhost:8000/docs/` にアクセス

## API一覧
### 投稿
`GET http://localhost:8000/twitter/`
`GET http://localhost:8000/twitter/show`
`POST http://localhost:8000/twitter/post`
`POST http://localhost:8000/twitter/destroy`

`GET http://localhost:8000/spreadsheet/`

## 構成
* Docker
* FastAPI