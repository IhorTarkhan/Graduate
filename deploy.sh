#!/bin/sh

ssh dev@65.109.4.189 "
killall firefox
cd ~/Graduate
source venv/bin/activate
killall python python3
rm -fr src
rm -f main.py
rm -f requirements.txt
"

scp -r src dev@65.109.4.189:~/Graduate/src
scp requirements.txt dev@65.109.4.189:~/Graduate
scp main.py dev@65.109.4.189:~/Graduate

ssh dev@65.109.4.189 "
cd ~/Graduate
source venv/bin/activate
pip install -r requirements.txt
python main.py \$(cat bot.key)
" &
