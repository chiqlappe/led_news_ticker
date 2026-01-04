#!/usr/bin/env python3
# coding=utf-8

# RSSフィードを取得し標準出力から出力するプログラム

import sys
import feedparser
from datetime import datetime


MAX_TITLES = 10 # 出力するタイトルの最大数


def output(url, title, splitter):
    print(splitter * 2 + title + splitter * 2, end = " ")
    feed = feedparser.parse(url)

    if (feed.bozo == False):
        n = 0
        for entry in feed.entries:
            print(entry.title, end = "　"+splitter+"　")
            n += 1
            if (n==MAX_TITLES):
                break
        return True
    else :
        return False


dt = datetime.now() # 更新時刻
datetime_str = dt.strftime("%H:%M")
print(datetime_str, end=" ");

min = int(dt.minute / 10) # 更新時間でフィードを選択する

match min:
    case 0:
        url = "https://news.web.nhk/n-data/conf/na/rss/cat0.xml"
        title = "NHKニュース"
        splitter = "◆"

    case 1:
        url = "http://feeds.cnn.co.jp/rss/cnn/cnn.rdf"
        title = "CNN国際ニュース"
        splitter = "★"

    case 2:
        url = "https://assets.wor.jp/rss/rdf/minkabufx/commodity.rdf"
        title = "株式ニュース"
        splitter = "＄"

    case 3:
        url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
        title = "Yahooニュース"
        splitter = "☆"

    case 4:
        url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"
        title = "ITmedia"
        splitter = "＠"

    case 5:
        url = "https://web.gekisaka.jp/feed"
        title = "ゲキサカ"
        splitter = "＃"


if (output(url, title, splitter) == False):
    print(title + "の読み込みに失敗しました")
    sys.exit(1)
else :
    sys.exit(0)

