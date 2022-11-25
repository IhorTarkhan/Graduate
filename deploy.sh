#!/bin/sh

ssh root@65.109.4.189 "
killall python3
rm -fr ~/Graduate/src
rm ~/Graduate/main.py
rm ~/Graduate/requirements.txt
"

scp -r src root@65.109.4.189:~/Graduate/src
scp requirements.txt root@65.109.4.189:~/Graduate
scp main.py root@65.109.4.189:~/Graduate

ssh root@65.109.4.189 "
cd ~/Graduate
pip3 install -r requirements.txt
python3 main.py \$(cat bot.key)
" &