"""
Raspy用。カメラをキャプチャして、フレームシンクワードをつけてjpegをシリアルに送る
pySerialが必要
"""
import serial
import configparser

# 設定ファイル読み込みとポートのオープン
config = configparser.ConfigParser()
config.read("config.ini")
PORT_TX = config["PORT"]["TX"]
BPS = int(config["PORT"]["BPS"])
writeSer = serial.Serial(PORT_TX, BPS, timeout=3)

# ヘッダを準備
fsw = 0xEB9038C7
fsw_arr = fsw.to_bytes(4, byteorder='big')

# ./cam/current.カメラのデータを読む
with open("./img_s/current.jpg", 'rb') as f:
    b_arr = f.read()
size = len(b_arr)
size_arr = size.to_bytes(4, byteorder='big')
# ヘッダ出力
for fs in fsw_arr:
    writeSer.write(fs.to_bytes(1))
    # print(format(fs,"X"), flush=True)
# サイズ出力
for s in size_arr:
    writeSer.write(s.to_bytes(1))
    # print(format(s,"X"), flush=True)
# 実体出力
cnt = 0
for b in b_arr:
    writeSer.write(b.to_bytes(1))
    if cnt % 5000 == 0:
        print("%7d:%02X"%(cnt,b), flush=True)
    cnt += 1

print("END", flush=True)
