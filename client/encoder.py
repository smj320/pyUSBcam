"""
Raspy用。カメラをキャプチャして、フレームシンクワードをつけてjpegをシリアルに送る
pySerialが必要
"""
import glob
import serial
import configparser
import cv2






def main():
    # Configの読込
    config = configparser.ConfigParser()
    config.read("../config.ini", encoding='utf-8')

    # 設定ファイル読み込みとポートのオープン
    dev = config['CLIENT']['SERIAL_TX']
    bps = int(config['COMMON']['BPS'])
    writeSer = serial.Serial(dev, bps, timeout=3)

    # ヘッダを準備
    fsw = 0xEB9038C7
    fsw_arr = fsw.to_bytes(4, byteorder='big')

    while True:
        # ---------------------
        # 最新の一つ前の画像を検索
        # ---------------------
        find = config['CLIENT']['PROJECT_ROOT']+'/client/img/*.jpg'
        files = sorted(glob.glob(find), reverse=True)
        if len(files) <= 1:
            print("No images found")
            break
        file_input = files[1]
        file_sent = file_input.replace('/img/', '/sent/')
        print("Globed path  %s" % file_input, flush=True)

        # ---------------------
        # リサイズして保存
        # ---------------------
        img = cv2.imread(file_input)
        # resize 1280x720 /3 -> 640x360
        cv2.resize(img, (640,360))
        cv2.imwrite(file_sent, img, [cv2.IMWRITE_JPEG_QUALITY, 20])

        # ---------------------
        # 再読込して送信
        # ---------------------
        with open(file_sent, 'rb') as f:
            jpeg = f.read()

        # ヘッダ出力
        size_arr = len(jpeg).to_bytes(4, byteorder='big')
        for fs in fsw_arr:
            writeSer.write(fs.to_bytes(1))
            print(format(fs,"X"), flush=True ,end="")
        # サイズ出力
        for s in size_arr:
            writeSer.write(s.to_bytes(1))
            print(format(s,"X"), flush=True ,end="")
        # 実体出力
        cnt = 0
        print("")
        b_arr = bytearray(jpeg)
        for b in b_arr:
            writeSer.write(b.to_bytes(1))
            if cnt % 10000 == 0:
                print("%7d:%02X"%(cnt,b), flush=True)
            cnt += 1
        print("END", flush=True)

    if __name__ == "__main__":
        main()
