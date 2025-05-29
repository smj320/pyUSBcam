"""
mac用。フレームシンクワードで見分けて、jpegをシリアルからダンプする。
pip pySerial
pip install opencv-python
pip install matplotlib
"""
import os
from threading import Thread
import queue

import serial
import configparser
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import cv2

global writeSer  # serial writer
global fsw_arr  # frame sync word


def encode(q):
    global writeSer
    global fsw_arr

    # ---------------------
    # ファイル名を受信,保存ファイル名を生成
    # ---------------------
    while True:
        img_path = q.get()
        sent_path = img_path.replace('/img/', '/sent/')
        print("Save to  %s" % sent_path, flush=True)

        # ---------------------
        # リサイズして保存　1280x720 /3 -> 640x360
        # ---------------------
        img = cv2.imread(img_path)
        cv2.resize(img, (640, 360))
        cv2.imwrite(sent_path, img, [cv2.IMWRITE_JPEG_QUALITY, 20])

        # ---------------------
        # 再読込して送信
        # ---------------------
        with open(sent_path, 'rb') as f:
            jpeg = f.read()
        # サイズ計測
        img_size = len(jpeg)
        print("Size %d" % img_size, flush=True, end="")
        size_arr = len(jpeg).to_bytes(4, byteorder='big')

        # ヘッダ出力
        for fs in fsw_arr:
            writeSer.write(fs.to_bytes(1))
            print(format(fs, "X"), flush=True, end="")
        # サイズ出力
        for s in size_arr:
            writeSer.write(s.to_bytes(1))
            print(format(s, "X"), flush=True, end="")
        # 実体出力
        cnt = 0
        b_arr = bytearray(jpeg)
        for b in b_arr:
            writeSer.write(b.to_bytes(1))
            if cnt % 10000 == 0:
                print("%7d:%02X" % (cnt, b), flush=True)
            cnt += 1
        print("SENT %06d/%06d" % (cnt, img_size), flush=True)


# ディレクトリ名, ファイル名、タイムスタンプ
def time_stamp():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    ts = "%04d-%02d-%02d %02d:%02d:%02d" % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return str(ts)


def get_img_dir(project_root):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    img_dir = project_root + "/client/img/%04d%02d%02d_%02d%02d%02d" % \
              (now.year, now.month, now.day, now.hour, now.minute, now.second)
    os.makedirs(img_dir, exist_ok=True)
    sent_dir = project_root + "/client/sent/%04d%02d%02d_%02d%02d%02d" % \
               (now.year, now.month, now.day, now.hour, now.minute, now.second)
    os.makedirs(sent_dir, exist_ok=True)
    return str(img_dir)


def get_img_path(img_dir, idx):
    img_path = img_dir + "/%06d.jpg" % idx
    return str(img_path)


def main():
    global writeSer
    global fsw_arr

    # Configの読込
    config = configparser.ConfigParser()
    config.read("../config.ini", encoding='utf-8')
    project_root = config['CLIENT']['PROJECT_ROOT']

    # 設定ファイル読み込みとポートのオープン
    dev = config['CLIENT']['SERIAL_TX']
    bps = int(config['COMMON']['BPS'])
    writeSer = serial.Serial(dev, bps, timeout=3)

    # ヘッダを準備
    fsw = 0xEB9038C7
    fsw_arr = fsw.to_bytes(4, byteorder='big')

    # macで0はPhoneのカメラとかになるので,デスクトップカメラは1
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # 変更を確認
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(fps, ww, hh)

    # スレッドスタート
    q = queue.Queue()
    t = Thread(target=encode, args=(q,))
    t.start()

    # 重複なしのフォルダを作る
    img_dir = get_img_dir(project_root)
    frame_count = 0
    while True:
        # 時間計測開始
        start = time.time()
        # キャプチャしてタイムスタンプを打って保存
        ret, frame = cap.read()
        ts = time_stamp()
        cv2.putText(frame, ts, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        img_path = get_img_path(img_dir, frame_count)
        cv2.imwrite(img_path, frame)
        frame_count += 1

        # 5秒おきに1枚転送する
        if frame_count % 50 == 0:
            q.put(img_path)

        # 経過時間計測終了
        end = time.time()
        # print("Time %0.3f" % (end - start))


if __name__ == "__main__":
    main()
