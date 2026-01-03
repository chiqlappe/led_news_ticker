# LED news ticker

## このプログラムについて
* [ハンブルソフト社製「LED電光掲示板」](https://www.humblesoft.com/j405board/index.html) をニュースティッカーにするプログラム
* chatGPTを使って作成しました

## 動作環境
* Python3

## 実行方法
`python3 rss.py | python3 bdf.py | python3 led.py`

## プログラムの説明

`rss.py`
* RSSフィードを取得し、タイトルを標準出力から出力するプログラム
* 登録されているRSSフィードはサンプルです

`bdf.py`
* 標準入力から取得した文字列を、BDFビットマップデータに変換して標準出力から出力するプログラム

`led.py`
* 標準入力から取得したBDFビットマップデータを、「LED電光掲示板ボード」にシリアル送信するプログラム
* 動作環境に合わせてPORTの値を修正してください

`cron.sh`
* crontab内で実行するためのスクリプト
* 動作環境に合わせて内容を修正してください
