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

または
```angular2html
sudo nmcli connection up preconfigured
[connection]
id=preconfigured
uuid=fe2889e5-fa03-4766-b312-0abb62ae1e25
type=wifi
timestamp=1744387820

[wifi]
mode=infrastructure
ssid=AM24

[wifi-security]
key-mgmt=wpa-psk
psk=67Sumikiku

[ipv4]
address1=192.168.1.100/24,192.168.1.1
dns=8.8.8.8;
method=manual

[ipv6]
addr-gen-mode=default
method=auto

[proxy]
```
を修正する。修正後
```angular2html
$ sudo nmcli connection reload
$ sudo nmcli connection up preconfigured
```
nslokupとかは
```angular2html
$ sudo apt-get install dnsutils
```

## カメラパラメータの確認
```
admin@df3cam01:~ $ v4l2-ctl --list-formats-ext
ioctl: VIDIOC_ENUM_FMT
	Type: Video Capture
	[0]: 'MJPG' (Motion-JPEG, compressed)
		Size: Discrete 1920x1080
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 960x540
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 848x480
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 640x480
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 640x360
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 424x240
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 320x240
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 320x180
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 176x144
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 160x120
			Interval: Discrete 0.033s (30.000 fps)
	[1]: 'YUYV' (YUYV 4:2:2)
		Size: Discrete 1920x1080
			Interval: Discrete 0.200s (5.000 fps)
		Size: Discrete 1280x720
			Interval: Discrete 0.100s (10.000 fps)
		Size: Discrete 960x540
			Interval: Discrete 0.050s (20.000 fps)
		Size: Discrete 848x480
			Interval: Discrete 0.050s (20.000 fps)
		Size: Discrete 640x480
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 640x360
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 424x240
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 320x240
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 320x180
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 176x144
			Interval: Discrete 0.033s (30.000 fps)
		Size: Discrete 160x120
			Interval: Discrete 0.033s (30.000 fps)
```