# 解説1
import cv2
import datetime


def path_name(ext):
    # 時刻の準備
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    # ファイル名生成
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y-%m-%d_%H:%M:%S')
    fn = "%s.%s" % (d, ext)
    return fn


def main():
    src = 'v4l2src device=/dev/video0 ! image/jpeg, '
    src += 'width=640, height=480, '
    src += 'framerate=(fraction)30/1 !jpegdec !videoconvert ! appsink'
    tt = 30
    # UVCカメラを開く
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(fps, ww, hh)

    fourcc = cv2.VideoWriter.fourcc(*'mjpg')  # 動画のコーデックを指定
    path = "./movie/%s" % path_name("avi")
    print(path)
    video = cv2.VideoWriter(path, fourcc, fps, (int(ww), int(hh)))

    for i in range(0, int(fps) * tt):
        ret, frame = cap.read()
        video.write(frame)
        if i % int(fps) == 0:
            path = './image/%s' % path_name("jpg")
            print(path)
            cv2.imwrite(path, frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        print(i)

    cap.release()
    video.release()


if __name__ == "__main__":
    main()
