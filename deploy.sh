#!/bin/sh

SERVER=dev@95.216.189.242

ssh "$SERVER" "
cd ~/Graduate
source venv/bin/activate
killall python
killall firefox
rm -fr src
rm -f main.py
rm -f requirements.txt
"

scp -r src "$SERVER":~/Graduate/src
scp requirements.txt "$SERVER":~/Graduate
scp main.py "$SERVER":~/Graduate

ssh "$SERVER" "
cd ~/Graduate
source venv/bin/activate
pip install -r requirements.txt
python main.py \$(cat bot.keys)
" &
