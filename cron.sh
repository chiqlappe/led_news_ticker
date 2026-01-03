#!/bin/bash

PATH=/usr/local/bin

cd ~/Documents/Python/denkou
python3 rss.py | python3 bdf.py | python3 led.py

