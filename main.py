import tweepy
import os
import json

# --- 認証設定 ---
auth = tweepy.OAuth1UserHandler(
    os.environ['API_KEY'],
    os.environ['API_SECRET'],
    os.environ['ACCESS_TOKEN'],
    os.environ['ACCESS_TOKEN_SECRET']
)
api = tweepy.API(auth)

# --- つぶやき候補をJSONファイルから読み込む ---
with open('tweets.json', encoding='utf-8') as f:
    tweets = json.load(f)

# --- index情報をJSONファイルから読み込む ---
STATE_FILE = 'state.json'
try:
    with open(STATE_FILE, encoding='utf-8') as f:
        state = json.load(f)
        index = state.get('index', 0)
except FileNotFoundError:
    index = 0

# --- 範囲を超えた場合は最初に戻る ---
if index >= len(tweets):
    index = 0

tweet = tweets[index]

# --- 投稿 ---
api.update_status(tweet)

print(f"Posted tweet #{index+1}")

# --- インデックスを進めてファイルに記録 ---
new_index = index + 1
with open(STATE_FILE, 'w', encoding='utf-8') as f:
    json.dump({'index': new_index}, f)
