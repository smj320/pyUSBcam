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

def path_name(ext):
    # 時刻の準備
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    # ファイル名生成
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y-%m-%d_%H:%M:%S')
    fn = "./sent/%s.%s" % (d, ext)
    return fn


def main():
    # ヘッダを準備
    fsw = 0xEB9038C7
    fsw_arr = fsw.to_bytes(4, byteorder='big')

    # 設定ファイル読み込みとポートのオープン
    config = configparser.ConfigParser()
    config.read("../config.ini")
    dev = config["GSE"]["SERIAL_RX"]
    bps = int(config["COMMON"]["BPS"])

    # ロゴ画面
    window_name = config["GSE"]["NAME"]
    bgr = (130,151,237)
    fnt_size = 0.6
    fnt_org = (20,20)
    img = cv2.imread("./logo/df3_logo.jpg")
    cv2.putText(img, "Now, Loading...", fnt_org, cv2.FONT_HERSHEY_DUPLEX, fnt_size, bgr)
    cv2.imshow(window_name, img)
    cv2.waitKey(1)

    # シリアルの準備
    readSer = serial.Serial(dev, bps, timeout=20)
    readSer.reset_input_buffer()

    # ログファイル
    f_log = open(path_name("log"), "wb")

    # シリアルを監視
    stat = 0
    data_size = 0
    b_stack = bytearray()
    while True:
        # ヘッダ検知
        if stat == 0:
            # 1文字読んでログに記録,スタックに積む
            cc = readSer.read(1)
            b_stack.extend(cc)
            # 待機マーカー
            print("%02X"%cc[0], flush=True, end='')
            #
            f_log.write(cc)
            f_log.flush()
            if len(b_stack) <= 3:
                continue
            # 一致したのでスタック破棄してステート進行
            if b_stack == fsw_arr:
                b_stack.clear()
                print(" Found FSW", flush=True)
                stat = 1
                continue
            # 一致しないので先頭を削除してやりなおし
            b_stack.pop(0)
            continue
        # データ長取得
        if stat == 1:
            # 長さ解析のため、1文字読んでログに記録,スタックに積む
            cc = readSer.read(1)
            b_stack.extend(cc)
            f_log.write(cc)
            f_log.flush()
            if len(b_stack) <= 3:
                stat = 1
                continue
            # バッファが育ったので解読,1M越えたらやりなおし
            data_size = int.from_bytes(bytes(b_stack), byteorder='big')
            print("Data size %02d Byte" % data_size, flush=True)
            if data_size > 1024 * 1024 * 1024:
                b_stack.clear()
                stat = 0
                continue
            # バッファクリア,ファイルオープン,書き込みポインタクリア、次のステート
            b_stack.clear()
            stat = 2
            continue
        # データ読込
        if stat == 2:
            cc = readSer.read(1)
            b_stack.extend(cc)
            if len(b_stack) % 5000 == 0:
                print("Received {:5.1f}%".format(len(b_stack) * 100 / data_size), flush=True)
            # ファイルサイズ書き切ったらファイルをクローズしてスタートを戻す
            if len(b_stack) == data_size:
                fn = path_name("jpg")
                with open(fn, "wb") as f:
                    f.write(b_stack)
                    b_stack.clear()
                print("Saved %s" % fn, flush=True)
                # 画面表示
                img = cv2.imread(fn)
                cv2.imshow(window_name, img)
                cv2.waitKey(1)
                stat = 0
            continue


if __name__ == "__main__":
    main()
