"""
mac用。フレームシンクワードで見分けて、jpegをシリアルからダンプする。
pip pySerial
pip install opencv-python
pip install matplotlib
"""
import time
import cv2

def main():

    src = 'v4l2src device=/dev/video0 ! image/jpeg,'
    src += 'width=1920, height=1080,'
    src += 'framerate=(fraction)30/1 !jpegdec !videoconvert ! appsink'
    # UVCカメラを開く。macでは、0はiPhoneのカメラとかになるので,デスクトップカメラは1
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Default")
    print(fps, ww, hh)

    ww = cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    hh = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print("Sset")
    print(ww, hh)

    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Result")
    print(fps, ww, hh)

if __name__ == "__main__":
    main()
