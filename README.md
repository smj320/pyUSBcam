# 環境設定とか

## PCの設定

```angular2html
% git clone git@github.com:smj320/pyUSBcam.git
% pyenv local 3.11.2
% python --version
Python 3.11.2
% python3 -m venv .venv
% . .venv/bin/activate
% pip install pyserial
% pip install opencv-python
% cp config.ini.dist config.ini

```

## Raspy側の設定

### OSのインストール
* sshを効くようにして、admin/domef3 でログインできるようにする。
* SSID は2.4Gのものを指定する。SDから編集できるのだろうか？
* 重いので、raspi-configでGUIログインを停める。
* 固定IPはcmdline.txtに下記を追記
```angular2html
ip=192.168.0.5::192.168.1.50:255.255.255.0:rpi:eth0:off
```
ssh-keygen -R 192.168.1.xx
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
```angular2html
% cp config.ini.dist config.ini
% sh pyUSBcam.sh で様子を見る
```

### exec.shとwebcamd.sh

デーモンス起動クリプト
webcam.service
これを下記に配置する。

```angular2html
$ sudo cp webcam.service /etc/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl enable pyUSBcam
テストは
$ sudo systemctl start/stop pyUSBcam
```

/etc/systemd/system/webcam.serviceを変更したときにはreloadする。

