# 環境設定とか

## PCの設定

```bash
% git clone git@github.com:smj320/pyUSBcam.git
% pyenv local 3.11.2
% python3 -m venv .venv
% . .venv/bin/activate
% pip install pyserial
% pip install opencv-python
% pip install configurator
% cp config.ini.dist config.ini
```

## Raspy側の設定

### OSのインストール
NetworkManagerというやつでネットワークを管理している。設定ファイルtは

```ini
設定ファイルのipv4をDHCPから固定に変更
/etc/NetworkManager/system-connections/preconfigured.nmconnection 
[ipv4]
address1=192.168.1.100/24,192.168.1.1
dns=192.168.1.1;
method=manual
```
* 接続で蹴られたら　ssh-keygen -R 192.168.1.xx
* 重いので、raspi-configでGUIログインを停める。
* 周辺機器のシリアルポートを有効にして、ログインには使わないように設定->再起動になる
* sudo apt-get install lsusb
* sudo apt-get install fswebcam

### pyUSBのインストール
* sudo apt-get update
* sudo apt-get install git
* mkdir ~/.ssh & chmod 700 ~/.ssh
* ssh-copy-id admin@cam で公開鍵を転送
* ssh git@github.comで接続確認
* /home/admin/proj で　git clone git@github.com:smj320/pyUSBcam.git
* pyUSBcamに移動
* /etc/fstabに下記を追加してリブート
* tmpfs /home/admin/proj/pyUSBcam/img_s tmpfs defaults,size=4m,mode=0777 0 0
* 
```bash
% cp config.ini.dist config.ini
% pip install configurator
% sudo apt-get install libopencv-dev python3-opencv #pipだと失敗する
% sh pyUSBcam.sh で様子を見る。出力されていたら
% sh pyUSBcamd.sh で起動して,tail -f ./log/pyUSBcam.log で起動を確認
```

### 自動起動
サービス登録用クリプト
webcam.service
これを下記のように登録して実行、テストする。
```bash
$ sudo cp webcam.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable pyUSBcam
テストは
$ sudo systemctl start/stop pyUSBcam　で./log/pyUSBcam.logを確認
```

/etc/systemd/system/webcam.serviceを変更したときにはreloadする。

## カメラパラメータの確認
4l2-ctl --list-formats-ext
でできるが、実際にはこのパラメータに設定できない。
