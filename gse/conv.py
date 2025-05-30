import glob
import os

# imvのディレクトリを列挙
src_dirs = glob.glob("./img/20*")

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
    src = "./img/" + dir + "/%06d.jpg"
    dst = "./mov/" + dir + ".avi"
    cmd = "ffmpeg -r 10 -i " + src + " -vcodec mjpeg " + dst
    print(cmd)
    os.system(cmd)
    pass
