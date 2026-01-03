#!/usr/bin/env python3
# coding=utf-8

# 標準入力から取得した文字列をBDFビットマップに変換し、標準出力から出力するプログラム

import sys
from pprint import pprint


BDF_FILE_8 = "8x16rk.bdf"    # JIS-X0201-1976
BDF_FILE_16 = "jiskan16.bdf" # JIS-X0208


def parse_bdf(filename):
    glyphs = {}
    with open(filename, errors="ignore") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("STARTCHAR"):
            name = line.split()[1]
            encoding = None
            width = height = None
            bitmap = []

            i += 1
            while not lines[i].startswith("ENDCHAR"):
                l = lines[i].strip()

                if l.startswith("ENCODING"):
                    encoding = int(l.split()[1])

                elif l.startswith("BBX"):
                    _, w, h, _, _ = l.split()
                    width = int(w)
                    height = int(h)

                elif l.startswith("BITMAP"):
                    for _ in range(height):
                        i += 1
                        n = int(lines[i].strip(), 16)
                        bitmap.append(n)

                i += 1

            if encoding is not None:
                glyphs[encoding] = {
                    "name": name,
                    "width": width,
                    "height": height,
                    "bitmap": bitmap
                }

        i += 1

    return glyphs


def dump(bitmap):
    for b in bitmap:
        print(f"{b:02X}", end=" ")
    print("\n0 0") #1ドット間をあける


def utf82jis(code):
    # EUC-JP は 0xA0 を足した値なので、引けば JIS X 0208 の本来の値になります。(chatGPT)
    try:
        euc = code.encode("euc_jp")
    except Exception as e:
        code = "〓" # 未登録文字用
        euc = code.encode("euc_jp")

    jis_raw = bytes([euc[0] - 0x80, euc[1] - 0x80])
    jis = int.from_bytes(jis_raw, byteorder='big', signed=False)
    return jis


def rotate_font_90_right_word(font):
    """
    font: list[int] or tuple[int], length=16
          各要素は 0x0000〜0xFFFF
    return: list[int], length=16
    """
    assert len(font) == 16

    out = [0] * 16

    for y in range(16):
        row = font[y]
        for x in range(16):
            if row & (1 << (15 - x)):   # MSBが左
                out[x] |= (1 << (15 - y))

    return out


glyphs_8  = parse_bdf(BDF_FILE_8)
glyphs_16 = parse_bdf(BDF_FILE_16)

for target in sys.stdin:

    for code in target:

        if ord(code) < 0x20:
            continue

        elif ord(code) < 0x100:
            jis = ord(code)
            if jis in glyphs_8:
                array = rotate_font_90_right_word(glyphs_8[jis]["bitmap"])
                del array[:8] # 8ドット幅に修正
                dump(array)
            else:
                print(f"{jis} not found in {BDF_FILE_8}")
                sys.exit(1)

        else:
            jis = utf82jis(code)

            if jis in glyphs_16:
                array = rotate_font_90_right_word(glyphs_16[jis]["bitmap"])
                dump(array)
            else:
                print(f"{jis} not found in {BDF_FILE_16}")
                sys.exit(1)

sys.exit(0)

