# 解説1
import cv2
import datetime
from threading import Thread
from queue import Queue

queue = Queue()

def path_name(ext):
    # 時刻の準備
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    # ファイル名生成
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y-%m-%d_%H:%M:%S')
    fn = "%s.%s" % (d, ext)
    return fn

def tx_data():
    while True:
        print("wait")
        frame = queue.get()
        if frame is None:
            break
        path = './image/%s' % path_name("jpg")
        print(path)
        cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        print("write")

def main():

    thread = Thread(target=tx_data)
    thread.start()

    src = 'v4l2src device=/dev/video0 ! image/jpeg,'
    src += 'width=1920, height=1080,'
    src += 'framerate=(fraction)30/1 !jpegdec !videoconvert ! appsink'
    tt = 30
    # UVCカメラを開く
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(fps, ww, hh)

    fourcc = cv2.VideoWriter.fourcc(*'MJPG')  # 動画のコーデックを指定
    path = "./movie/%s" % path_name("avi")
    print(path)
    video = cv2.VideoWriter(path, fourcc, fps, (int(ww), int(hh)))

    for i in range(0, int(fps) * tt):
        ret, frame = cap.read()
        video.write(frame)
        print(i)
        if i % 10 == 0:
            queue.put(frame)

    queue.put(None)
    cap.release()
    video.release()
    thread.join()

if __name__ == "__main__":
    main()
