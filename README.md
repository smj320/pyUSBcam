# 環境設定とか

## Raspy側の設定

### OSのインストール
* sshを効くようにして、admin/domef3 でログインできるようにする。
* SSID は2.4Gのものを指定する。SDから編集できるのだろうか？
* DHCP-DNSの組み合わせによっては
ssh admin@df3cma01.local
で呼び出せることもある。見つからなければ
nmap -p 22 192.168.1.0/24　で探す
hostがかぶっていると言われたら
ssh-keygen -R 192.168.1.xx

### 行う設定
* 重いので、raspi-configでGUIログインを停める。
* 周辺機器のシリアルポートを有効にして、ログインには使わないように設定。

### パスとか
ホスト名はdf3cma01とか
プロジェクトルートパスは/usr/admin/proj/pyUSBcam
コマンドとかもここにおく。

mkdir -p /home/admin/proj/pyC/img_l
mkdir -p /home/admin/proj/pyUSBcam/img_s
mkdir -p /home/admin/proj/pyUSBcam/log
/home/admin/proj/pyUSBcam/img_s/current.jpg を送信する。


### 必要なもの
touch encode.py
touch config.ini
touch exec.sh
vi でコピペが確実。上で述べた作業ディレクトリ2つは作っておく。

sudo apt-get install lsusb カメラを確認
sudo apt-get install fswebcam　出力を確認
sudo apt-get install pipenv

raspiの場合はpyserialは最初から入っているので入れない。
daemon化したときにパスが解らなくなる

### exec.shとwebcamd.sh

exec.shはfswebcamで画像をとって、encode.pyでシステムに送る。
webcamd.shはdaemon用のスクリプトで、出力を./log/webcam.logに 集める。

デーモンス起動クリプト
webcam.service
これを下記に配置する。

```angular2html
$ sudo cp webcam.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable webcam
テストは
$ sudo systemctl start/stop webcam
```

/etc/systemd/system/webcam.serviceを変更したときにはreloadする。

