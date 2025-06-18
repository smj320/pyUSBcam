import glob
import os
import configparser

# 設定ファイル読み込みとポートのオープン
src_dirs = glob.glob("../client/img/*")

# なければ終了
if len(src_dirs) == 0:
    exit()

# あればmovファイルを作成
for src_dir in src_dirs:
    # ファイルの存在チェック、なければ飛ばす
    files = glob.glob(src_dir + "/*.jpg")
    if len(files) == 0:
        continue
    # src, dstを決めて変換
    dir = src_dir.split("/")[-1]
    src = src_dir + "/img_%05d.jpg"
    dst = "./mov/" + dir + ".avi"
    cmd = "ffmpeg -r 10 -i " + src + " -vcodec mjpeg -loglevel info " + dst
    print(cmd)
    os.system(cmd)
    pass
