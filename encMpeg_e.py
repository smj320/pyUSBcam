# 解説1
import cv2


def main():
    codec = 'mjpg'
    name = "./mp4/sample.avi"
    # UVCカメラを開く
    cap = cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    ww = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    hh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    fourcc = cv2.VideoWriter.fourcc(*codec)  # 動画のコーデックを指定
    video = cv2.VideoWriter(name, fourcc, fps, (int(ww), int(hh)), True)

    for i in range(0, 20):
        ret, frame = cap.read()
        video.write(frame)
        if i % 10 == 0:
            print(i)

    cap.release()
    video.release()


if __name__ == "__main__":
    main()
