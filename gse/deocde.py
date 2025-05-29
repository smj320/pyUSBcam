"""
mac用。フレームシンクワードで見分けて、jpegをシリアルからダンプする。
pip pySerial
pip install opencv-python
pip install matplotlib
"""
import datetime
import configparser
import serial
import cv2


def path_name():
    # 時刻の準備
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    # ファイル名生成
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    fn = "./sent/%s.jpg" % d
    return fn


def main():
    # 設定ファイル読み込みとポートのオープン
    config = configparser.ConfigParser()
    config.read("../config.ini")
    dev = config["GSE"]["SERIAL_RX"]
    bps = int(config["COMMON"]["BPS"])

    # ロゴ画面
    window_name = config["GSE"]["NAME"]
    bgr = (130, 151, 237)
    fnt_size = 0.6
    fnt_org = (20, 20)
    img = cv2.imread("./logo/df3_logo.jpg")
    cv2.putText(img, "Now, Loading...", fnt_org, cv2.FONT_HERSHEY_DUPLEX, fnt_size, bgr)
    cv2.imshow(window_name, img)
    cv2.waitKey(1)

    # シリアルの準備
    readSer = serial.Serial(dev, bps, timeout=20)
    readSer.reset_input_buffer()

    # シリアルを監視
    stat = 0
    fn = None
    f_name = None
    b_stack = bytearray()
    while True:
        # ヘッダ検知
        if stat == 0:
            # 1文字読んでログに記録,スタックに積む
            cc = readSer.read(1)
            b_stack.extend(cc)
            if len(b_stack) < 2:
                continue
            print("%02d %02X%02X" % (len(b_stack),b_stack[0],b_stack[1]), flush=True)
            # 一致したのでスタック破棄してステート進行
            if b_stack[0] == 0xFF and b_stack[1] == 0xD8:
                b_stack.clear()
                print(" Found FFD8", flush=True)
                # ファイルオープン
                f_name = path_name()
                fn = open(f_name, "wb")
                # ヘッダをファイルに格納
                fn.write(0xFFD8.to_bytes(2, byteorder='big'))
                # マーカークリア
                b_stack.clear()
                # ステート進行
                stat = 1
                continue
            # 一致しないので先頭を削除してやりなおし
            b_stack.pop(0)
            continue
        # データ読込
        if stat == 1:
            cc = readSer.read(1)
            # ファイルに出力
            fn.write(cc)
            # マーカーバッファにデータを入れる,2以下なら継続
            b_stack.extend(cc)
            if len(b_stack) < 2:
                continue
            # 2以上なら完了チェック
            if b_stack[0] == 0xFF and b_stack[1] == 0xD9:
                # ファイルクローズ,マーカリセット
                fn.close()
                b_stack.clear()
                # 再読み込みと表示
                img = cv2.imread(f_name)
                cv2.imshow(window_name, img)
                cv2.waitKey(1)
                stat = 0
                continue
            else:
                b_stack.pop(0)
                continue


if __name__ == "__main__":
    main()
