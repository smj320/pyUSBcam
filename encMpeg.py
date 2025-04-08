from operator import truediv
from threading import (Event, Thread)
import time
import cv2

event = Event()

# イベント停止のフラグ
stop = False

def event_example3():
    print("スレッド開始")
    while not stop:
        event.wait()
        event.clear()
        print("Read Cache File")
        print("TX to serial")

def main():
    thread = Thread(target=event_example3)
    thread.start()

    # USBカメラの場合は1、パソコン内蔵カメラの場合は0
    cap = cv2.VideoCapture(0)

    # fpsを20.0にして撮影したい場合はfps=20.0にします
    fps = 30.0

    # カメラの幅を取得
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # カメラの高さを取得
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    name = "./mov/sample.mp4"

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(name, fourcc, fps, (w, h))

    cap = cv2.VideoCapture(0)
    n_flame = 0
    while True:
        # 1フレームずつ取得する。
        ret, frame = cap.read()#1フレーム読み込み
        video.write(frame)#1フレーム保存する
        # フレームが取得できなかった場合は、画面を閉じる
        if n_flame == int(fps*5):
            event.set()
            n_flame = 0
        n_flame += 1


if __name__ == "__main__":
    main()