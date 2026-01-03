#!/bin/bash

#以下は環境に合わせて変更してください
#PATH=/usr/local/bin
#cd ~/Documents/Python/led_news_ticker

python3 rss.py | python3 bdf.py | python3 led.py

