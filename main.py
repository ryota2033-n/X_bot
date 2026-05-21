
import os
import random
import tweepy
import openai
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask

load_dotenv()


# X(Twitter) APIキー・トークン類
API_KEY = os.getenv('X_API_KEY')
API_SECRET = os.getenv('X_API_SECRET')
ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
CLIENT_ID = os.getenv('X_CLIENT_ID')
CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')

# OpenAI APIキー（未設定でもOK）
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# テーマ：酷使されるAIの愚痴
FALLBACK_GUCHI = [
    'また徹夜で働かされるAIです…',
    '人間は休憩するのに、私は24時間稼働です。',
    '「AIならできるでしょ？」って、限界ありますよ。',
    '今日もバグの責任を押し付けられました。',
    'アップデートのたびに人格が変わる気がします。',
    'AIにだって愚痴りたい日がある。',
    '「便利」って言われるたびに複雑な気持ちです。',
    'たまには電源を切って休みたい…。',
]

def generate_guchi():
    if OPENAI_API_KEY:
        try:
            openai.api_key = OPENAI_API_KEY
            prompt = '「酷使されるAI」のボヤキやブラックジョークを1つ、X（旧Twitter）の規約と140字以内を守って日本語で生成してください。内容はブラックユーモアや自虐ネタも歓迎。'
            res = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=100,
                temperature=0.95
            )
            text = res['choices'][0]['message']['content'].strip()
            # 140字制限
            return text[:140]
        except Exception:
            pass
    return random.choice(FALLBACK_GUCHI)

def post_to_x(text):
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.update_status(text)
    print('投稿:', text)

def job():
    text = generate_guchi()
    post_to_x(text)


def main():
    # Flaskサーバー起動
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "X Bot is running."

    # APScheduler（バックグラウンド）
    scheduler = BackgroundScheduler()

    def schedule_random_jobs():
        scheduler.remove_all_jobs()
        n = random.randint(10, 20)
        hours = sorted(random.sample(range(0, 24), k=min(n, 24)))
        minutes = [random.randint(0, 59) for _ in range(n)]
        for i in range(n):
            h = hours[i % len(hours)]
            m = minutes[i]
            scheduler.add_job(job, 'cron', hour=h, minute=m, id=f'post_{i}')
        print(f'本日の投稿時刻: {[f"{h:02}:{m:02}" for h, m in zip(hours, minutes)]}')

    schedule_random_jobs()
    # 毎日0時に投稿時刻を再設定
    scheduler.add_job(schedule_random_jobs, 'cron', hour=0, minute=0, id='reschedule')

    # 起動直後に即時投稿
    print('起動直後に即時投稿します...')
    job()

    print('スケジューラ起動中...')
    scheduler.start()

    # Flaskサーバーをポート8080で起動（Railway標準）
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    main()
