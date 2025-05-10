# 環境設定とか

## PCの設定

### カメラの調査

ffmpeg -list_devices true -f avfoundation  -i dummy
ffmpeg -f avfoundation  -i "0"

1920x1080だとスペック上は5fpsだが実際の取得・保存には1秒程度かかっている。
1260x720だと10fpsとなり、転送・書き込みの実時間も0.1秒程度で終わる。
ということで、1260x720@10fpsのパラメータで5fpsとする。

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

## カメラパラメータの確認
4l2-ctl --list-formats-ext
でできるが、opnecvからは全てのパラメータは設定できない。

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
```
% cp config.ini.dist config.ini
% pip install configurator
% sudo apt-get install libopencv-dev python3-opencv #pipだと失敗する
% sh cam_encoder.bash で様子を見る。出力されていたら
% sh cam_capture.bash で起動して,tail -f ./log/pyUSBcam.log で起動を確認
```

### 自動起動

cronでやる。
crontab crontab.txt

### I2C-UARTブリッジ　sc16is7xx

I2Cの通信可能性とアドレスを確認
$ sudo apt update
$ sudo apt install i2c-tools

```
$ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- 4d -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --  
```

ところが、システム的には、デバイスツリーファイル
/boot/firmware/overlays/sc16is750-i2c.dtbo
の中でアドレスが0x48で待機しているようで、これは
```aiignore
/sys/bus/i2c/devices/1-0048
```
でみてとれる。.dtboファイルは一般的にはソースファイルを
コンパイルしなさないとパラメータは変更できないが、
パラメータとしてとれる場合がある。
```
$ sudo dtoverlay -h sc16is750-i2c

Name:   sc16is750-i2c

Info:   Overlay for the NXP SC16IS750 UART with I2C Interface
        Enables the chip on I2C1 at 0x48 (or the "addr" parameter value). To
        select another address, please refer to table 10 in reference manual.

Usage:  dtoverlay=sc16is750-i2c,<param>=<val>

Params: int_pin                 GPIO used for IRQ (default 24)
        addr                    Address (default 0x48)
        i2c-bus                 Supports all the standard I2C bus selection
                                parameters - see "dtoverlay -h i2c-bus"
        xtal                    On-board crystal frequency (default 14745600)
```
これによると、アドレスと割込ピン、バスマスタ、xtal周波数が変数としてとれる。
この変数は/boot/firmware/config.txtに記述することで変更できる。
```
# SC16IS7xx I2C
dtoverlay=sc16is750-i2c,addr=0x4d,int_pin=4,xtal=7372800
```

設定後再起動すると、
/dev/ttySC0
が使えるようになる。


### RTC
DS3231

### 有線接続方法
screen /dev/cu.usbserial-A906UWWB 115200

### wifiの無効化/有効化
sudo systemctl disable NetworkManager
sudo systemctl enable NetworkManager

ps aux の出力 pidは2, 
1 admin
2 769
3 0.0
4 0.4
5 6092
6 2000
7 pts/0
8 S+
9 10:04
10 0:00
11 grep --color=auto capture