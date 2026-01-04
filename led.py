#!/usr/bin/env python3
# coding=utf-8

# 標準入力から取得したBDFビットマップデータを、「LED電光掲示板ボード」にシリアル送信するプログラム

import sys
import serial
import serial.tools.list_ports
import time

PORT = "/dev/cu.UC-232AC" # 環境に合わせて変更してください
BAUD = 19200

def sendData(data):
    global ser
    data += '\r'
    data = data.encode('utf-8')
    ser.write(data)
    time.sleep(0.1)


def recvData():
    global ser
    data = ser.readline()

    if not data:
        data = "E Timeout"
    else:
        data = data.strip()
        data = data.decode('utf-8')

    return data


error_flag = False
ser = serial.Serial(port=PORT, baudrate=BAUD, timeout=0.5)
time.sleep(0.1) # USB-UART安定待ち

sendData("echo 0")
sendData("sync")
sendData("rom_format")
sendData("rom_scroll")
sendData("rom_set speed 1")
sendData("rom_check")

ser.reset_input_buffer() # 受信バッファ破棄

#送信(tx)
for data in sys.stdin:

    if (error_flag == False):
        sendData("rom_dwrite " + data)

        #受信(rx)
        data = recvData()
        if (data.startswith("E")):
            error_flag = True
            print(data)

sendData("rom_dclose")

ser.close()
sys.exit(0)

