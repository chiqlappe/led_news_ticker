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
    data = data.strip()
    data = data.decode('utf-8')

    return data


ser = serial.Serial(port=PORT, baudrate=BAUD, parity= 'N')

print("writing...")

sendData("echo 0")
sendData("rom_format")

#送信(tx)
for data in sys.stdin:
    sendData("rom_dwrite " + data)
    
    #受信(rx)
    while(ser.in_waiting):
        data = recvData()
        if (data.startswith("E")):
            print(data)
            ser.close()
            sys.exit(1)

sendData("rom_dclose")
sendData("rom_scroll")
sendData("rom_set speed 1")
sendData("rom_check")

ser.close()

print("done.")

sys.exit(0)

