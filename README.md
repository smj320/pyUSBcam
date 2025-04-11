# 環境設定とか

## PCの設定

```bash
% git clone git@github.com:smj320/pyUSBcam.git
% pyenv local 3.11.2
% python --version
Python 3.11.2
% python3 -m venv .venv
% . .venv/bin/activate
% pip install pyserial
% pip install opencv-python
% pip install configurator
% cp config.ini.dist config.ini
```
接続で蹴られたら　ssh-keygen -R 192.168.1.xx

## Raspy側の設定

### OSのインストール
* sshを効くようにして、admin/domef3 でログインできるようにする。
* SSID は2.4Gのものを指定する。SDから編集できるのだろうか？
* 重いので、raspi-configでGUIログインを停める。
* 周辺機器のシリアルポートを有効にして、ログインには使わないように設定->再起動になる
* sudo apt-get install lsusb
* sudo apt-get install fswebcam


### pyUSBのインストール
* sudo apt-get install git
* mkdir ~/.ssh & chmod 700 ~/.ssh
* id_rsa_githubをid_rsaとしてコピーして、600
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

## 固定IPの振り方
固定IPの振り方
一回DHCPでWifiに繋ぎ、その後固定に変更する。

シリアルからの接続を確認するために、以下のコマンドを実行


```angular2html
nmcli connection
[結果]
NAME           UUID                                  TYPE      DEVICE 
preconfigured  fe2889e5-fa03-4766-b312-0abb62ae1e25  wifi      wlan0
[設定]
sudo nmcli con mod "SSIDから付けられているID" ipv4.method "manual" ipv4.addresses "192.168.1.39/24" ipv4.gateway "192.168.1.1" 
sudo nmcli connection up SSIDから付けられているID
[反映]
sudo nmcli connection reload
sudo nmcli connection up SSIDから付けられているID
```

