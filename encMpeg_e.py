from operator import truediv
from threading import (Event, Thread)
import cv2

"""
メインスレッド
"""
def main():
    # USBカメラの場合は1、パソコン内蔵カメラの場合は0
    cap = cv2.VideoCapture(0)

    # 動画保存時の形式を設定
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    name = "./mp4/sample.mp4"

    # カメラの幅を取得
    # w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # カメラの高さを取得
    # h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # (保存名前、fourcc,fps,サイズ)
    video = cv2.VideoWriter(name, fourcc, 30, (640, 480))

    n_flame = 0
    while True:
        # 1フレームずつ取得する。
        ret, frame = cap.read()
        video.write(frame)
        n_flame += 1
        if n_flame % 30*5 == 0:
            break

if __name__ == "__main__":
    main()
