# 酷使されるAIのつぶやき自動投稿システム

## 概要
- 無料サーバー（Render.com等）で動作するX（旧Twitter）自動投稿Bot
- テーマ：「酷使されるAIの愚痴」
- OpenAI APIで愚痴生成（未設定時はランダム）
- 毎日朝7時・夜19時に自動投稿

## 必要なもの
- Python 3.8+
- X APIキー（.envに記載）
- OpenAI APIキー（任意）

## 使い方
1. `.env.sample`をコピーして`.env`を作成し、APIキーを記入
2. `requirements.txt`で依存をインストール
3. `main.py`を実行

## デプロイ例
- Render.com, Railway, Replit等の無料サーバーで動作
- スケジューラはmain.py内で完結

## 注意
- OpenAI APIキーが無い場合はランダム愚痴のみ
- X APIの無料枠制限に注意
