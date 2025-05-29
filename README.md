# 環境設定とか

## Raspy側の設定

### serial consoleの有効化
インストールイメージは64bit Lightを選択。
bootfsのconfig.txtで
```
[all]
enable_uart=1
```
screen /dev/cu.usbserial-A906UWWB 115200

### wifi接続

wifi接続
$ sudo nmcli dev wifi con SSID password PASSWORD

確認
$ nmcli con

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
dtoverlay=sc16is750-i2c,addr=0x4d,int_pin=4,xtal=14715000
```

設定後再起動すると、
/dev/ttySC0
が使えるようになる。

### RTCのインストール
DS3231　を使う。
/boot/firmware/config.txtに
# DS2321 I2C
dtoverlay=i2c-rtc,ds3231
を追加。このファイルは、FAT32のconfig.txtが参照されているようだ。

### pyUSBのインストール
* sudo apt-get update
* sudo apt-get install git
* mkdir ~/.ssh & chmod 700 ~/.ssh
* ssh-copy-id admin@cam で公開鍵を転送
* ssh git@github.comで接続確認
* /home/admin/ で　git clone git@github.com:smj320/pyUSBcam.git

```
python -m venv .venv
. ./venv/bin/activate
% cp config.ini.dist config.ini
% pip install configurator
% sudo apt-get install libopencv-dev python3-opencv #pipだと失敗する
% cd client
% bash encoder.bash -v で様子を見る。出力を確認
```
### 自動起動

cronでやる。
crontab crontab.txt

## PCの設定

### プロジェクトの展開

github用の秘密鍵を.sshにインストールして、パーミッションを0700に設定しておく。

```
% git clone git@github.com:smj320/pyUSBcam.git
% pyenv local 3.11.2
% python3 -m venv .venv
% . .venv/bin/activate
% pip install pyserial
% pip install opencv-python
% pip install configurator
% cp config.ini.dist config.ini
```
