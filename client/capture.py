"""
mac用。フレームシンクワードで見分けて、jpegをシリアルからダンプする。
pip pySerial
pip install opencv-python
pip install matplotlib
"""
import signal
import time
import cv2

def main():
    global cap
    global idx
    # macで0はPhoneのカメラとかになるので,デスクトップカメラは1
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # 変更を確認
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(fps, ww, hh)

    idx = 0
    while True:
        start = time.time() #
        ret, frame = cap.read()
        cv2.imwrite("./img_s/img_%06d.jpg" % idx, frame)
        end = time.time() #
        print("Time %0.3f" % (end - start))
        idx += 1

if __name__ == "__main__":
    main()
