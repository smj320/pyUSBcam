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
    print(fps, ww, hh)

    idx = 0
    while True:
        start = time.time()
        ret, frame = cap.read()
        cv2.imwrite("./sent/sent%06d.jpg"%idx, frame)
        end = time.time()
        print(end - start)
        idx += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
