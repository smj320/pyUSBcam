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
        file_input = q.get()
        if file_input == "#DONE":
            return

        file_sent = file_input.replace('/img/', '/sent/')
        dir = os.path.dirname(file_sent)
        os.makedirs(dir, exist_ok=True)
        print("Save to  %s" % file_sent, flush=True)

        # ---------------------
        # リサイズして保存　1280x720 /3 -> 640x360
        # ---------------------
        img = cv2.imread(file_input)
        cv2.resize(img, (640, 360))
        cv2.imwrite(file_sent, img, [cv2.IMWRITE_JPEG_QUALITY, 20])

        # ---------------------
        # 再読込して送信
        # ---------------------
        with open(file_sent, 'rb') as f:
            jpeg = f.read()

        # ヘッダ出力
        size_arr = len(jpeg).to_bytes(4, byteorder='big')
        for fs in fsw_arr:
            writeSer.write(fs.to_bytes(1))
            print(format(fs, "X"), flush=True, end="")
        # サイズ出力
        for s in size_arr:
            writeSer.write(s.to_bytes(1))
            print(format(s, "X"), flush=True, end="")
        # 実体出力
        cnt = 0
        print("")
        b_arr = bytearray(jpeg)
        for b in b_arr:
            writeSer.write(b.to_bytes(1))
            if cnt % 10000 == 0:
                print("%7d:%02X" % (cnt, b), flush=True)
            cnt += 1
        print("END", flush=True)


# ディレクトリ名, ファイル名、タイムスタンプ
def file_names(idx):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    ms = int(now.microsecond / 1000.0)
    file_save = "/img_%08d.jpg" % idx
    ts = "%04d-%02d-%02d %02d:%02d:%02d.%03d" % (now.year, now.month, now.day, now.hour, now.minute, now.second, ms)
    return str(file_save), str(ts)


def dir_names(project_root):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    dir = project_root + "/client/img/%04d-%02d-%02d_%02d:%02d:%02d" % \
          (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return str(dir)


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
    dir = dir_names(project_root)
    os.makedirs(dir, exist_ok=True)
    print("Save to %s" % dir, flush=True)

    idx = 0
    while True:
        try:
            # 時間計測開始
            start = time.time()

            # ファイル名とキャプチャ
            file_name, ts = file_names(idx)
            ret, frame = cap.read()
            file_path = dir + file_name

            # キャプチャ画像にタイムスタンプをつけて保存
            cv2.putText(frame, ts, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imwrite(file_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

            # 5秒おきに1枚転送する
            if idx % 50 == 0:
                q.put(file_path)

            # 経過時間計測終了
            end = time.time()
            print("Time %0.3f" % (end - start))

            # カウントアップ
            idx += 1
        except KeyboardInterrupt:
            print("Terminate")
            q.put("#DONE")
            t.join()
            exit(0)

if __name__ == "__main__":
    main()
