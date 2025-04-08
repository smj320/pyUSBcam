from operator import truediv
from threading import (Event, Thread)
import cv2

import serial
import configparser

event = Event()
img_cache = "./img_s/cache.jpg"

# 設定ファイル読み込みとポートのオープン
config = configparser.ConfigParser()
config.read("config.ini")
PORT_TX = config["PORT"]["TX"]
BPS = int(config["PORT"]["BPS"])
writeSer = serial.Serial(PORT_TX, BPS, timeout=3)

# 撮像
fps = 10.0
q_low_period = 10
q_low_w = 320
q_low_h = 240
q_high_period = q_low_period * 4
q_high_w = q_low_w * 2
q_high_h = q_low_h * 2

# GPIO
# is_low = True
is_low = False

"""
UART 送信スレッド
"""


def serial_tx():
    print("スレッド開始")
    # ヘッダを準備
    fsw = 0xEB9038C7
    fsw_arr = fsw.to_bytes(4, byteorder='big')
    while True:
        # 待機解除
        event.wait()
        event.clear()
        # キャッシュ読込
        with open(img_cache, "rb") as f:
            print("Read Cache", flush=True)
            b_arr = f.read()
        size = len(b_arr)
        size_arr = size.to_bytes(4, byteorder='big')
        # ヘッダ出力
        for fs in fsw_arr:
            writeSer.write(fs.to_bytes(1))
        # サイズ出力
        for s in size_arr:
            writeSer.write(s.to_bytes(1))
            # print(format(s,"X"), flush=True)
        # 実体出力
        cnt = 0
        for b in b_arr:
            writeSer.write(b.to_bytes(1))
            if cnt % 5000 == 0:
                print("%7d:%02X" % (cnt, b), flush=True)
            cnt += 1
        print("END", flush=True)


"""
メインスレッド
"""
def main():
    thread = Thread(target=serial_tx)
    thread.start()

    # USBカメラの場合は1、パソコン内蔵カメラの場合は0
    cap = cv2.VideoCapture(0)

    # 動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    name = "./mp4/sample.mp4"

    # カメラの幅を取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # カメラの高さを取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(name, fourcc, fps, (w, h))

    n_flame = 0
    while True:
        # 1フレームずつ取得する。
        ret, frame = cap.read()
        video.write(frame)
        # 画質選択
        period = q_low_period if is_low else q_high_period
        img_w = q_low_w if is_low else q_high_w
        img_h = q_low_h if is_low else q_high_h
        if n_flame == fps * period:
            print("Output Cache", flush=True)
            tx_img = cv2.resize(frame, (img_w, img_h))
            cv2.imwrite(img_cache, tx_img, [cv2.IMWRITE_JPEG_QUALITY, 50])
            event.set()
            n_flame = 0
        n_flame += 1


if __name__ == "__main__":
    main()
