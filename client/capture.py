"""
mac用。フレームシンクワードで見分けて、jpegをシリアルからダンプする。
pip pySerial
pip install opencv-python
pip install matplotlib
"""
import os
import time
from threading import Thread
import queue

import serial
import configparser
from datetime import datetime
from zoneinfo import ZoneInfo
import cv2

global writeSer  # serial writer

# global fsw_arr  # frame sync word

def encode(q):
    global writeSer

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

        # 実体出力
        cnt = 0
        b_arr = bytearray(jpeg)
        for b in b_arr:
            writeSer.write(b.to_bytes(1))
            if cnt % 10000 == 0:
                print("%7d:%02X" % (cnt, b), flush=True)
            cnt += 1
        print("SENT %06d" % cnt, flush=True)


# ディレクトリ名, ファイル名、タイムスタンプ
def time_stamp():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    ts = ("%04d-%02d-%02d %02d:%02d:%02d.%04d" %
          (now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond / 1000))
    return str(ts)


def get_img_dir(project_root):
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    img_dir = project_root + "/client/img/%04d%02d%02d_%02d%02d%02d" % \
              (now.year, now.month, now.day, now.hour, now.minute, now.second)
    os.makedirs(img_dir, exist_ok=True)
    # YYYYMMDD_HHMMSS
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
    n_img = int(config['COMMON']['N_IMG'])

    # 設定ファイル読み込みとポートのオープン
    dev = config['CLIENT']['SERIAL_TX']
    bps = int(config['COMMON']['BPS'])
    writeSer = serial.Serial(dev, bps, timeout=3)

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
    # fps=10で動くおうに待機させたい
    target_fps = 10
    target_ms_per_frame = int(1000 / target_fps)
    while True:
        start_time = time.time()
        # キャプチャしてタイムスタンプを打って保存
        ret, frame = cap.read()
        ts = time_stamp()
        cv2.putText(frame, ts, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        img_path = img_dir + "/img_%05d.jpg" % frame_count
        cv2.imwrite(img_path, frame)
        frame_count += 1

        #　待機時間計装
        end_time = time.time()  # フレーム処理終了時間
        elapsed_time_ms = (end_time - start_time) * 1000  # 処理にかかった時間 (ミリ秒)
        wait_time_ms = max(1, target_ms_per_frame - int(elapsed_time_ms))
        if cv2.waitKey(wait_time_ms) & 0xFF == ord('q'):
            break

        # 10秒おきに1枚転送する
        if frame_count % 100 == 0:
            q.put(img_path)

        # 36000フレームとごにディレクトリを切り替える
        if frame_count == n_img:
            img_dir = get_img_dir(project_root)
            frame_count = 0


if __name__ == "__main__":
    main()
