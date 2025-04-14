# 解説1
import cv2


def main():
    src = 'v4l2src device=/dev/video0 ! image/jpeg, '
    src += 'width=1280, height=720, '
    src += 'framerate=(fraction)30/1 !jpegdec !videoconvert ! appsink'
    tt = 30
    # UVCカメラを開く
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(fps, ww, hh)

    fourcc = cv2.VideoWriter.fourcc(*'mjpg')  # 動画のコーデックを指定
    video = cv2.VideoWriter("./video/movie.avi", fourcc, fps, (int(ww/4), int(hh/4)))

    for i in range(0, int(fps) * tt):
        ret, frame = cap.read()
        mini = cv2.resize(frame, (int(ww/4), int(hh/4)))
        video.write(mini)
        if i % 10 == 0:
            cv2.imwrite('./image/%06d.jpg' % i, frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        print(i)

    cap.release()
    video.release()


if __name__ == "__main__":
    main()
