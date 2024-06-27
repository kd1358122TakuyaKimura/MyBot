# (c) Takuya Kimura (takuyakimura0507@gmail.com)

from datetime import datetime
from datetime import timezone
from datetime import timedelta

import random
import discord
import mybot


# 環境変数からトークンを取得
TOKEN = 'enter your discord app token is here.'

# 日本時間のタイムゾーンオフセット
JST = timezone(timedelta(hours=9))

# 権限を生成
client_permission =\
    discord.Permissions(2147617792)

# インセットを生成
client_intents =\
    discord.Intents.all()

# discordクライアントを生成
client =\
    discord.Client(intents=client_intents, permissions=client_permission)

# rebotインスタンスを生成
mybot = mybot.MyBot('./sample.mybot')


# 説明：Bot起動時に実行されるフロー
@client.event
async def on_ready():
    """
    """


# 説明：任意のユーザーによってメッセージ投稿が発生した場合に実行されるフロー
@client.event
async def on_message(message: discord.Message):

    # 日本時間の現在時刻
    jstdt = datetime.now(JST)

    # メッセージ投稿者がBot自身であった場合
    # この場合特に何もせずにフローを終了
    if message.author == client.user:
        ...

    # 朝の挨拶
    elif message.content in ('おはよう', 'おはよう！', 'おはようございます！'):

        # 実は昼だった場合
        if 11 <= jstdt.hour <= 17:
            echo_message =\
                random.choice(('もう昼やで！', 'もう昼でっせ！', '寝ぼけてはんの？'))

        # 朝だった場合
        elif jstdt.hour < 11:
            echo_message =\
                random.choice(('おはようさん！', 'おはよう！', '朝早くからどないしたん？'))

        # 実は夜だった場合
        elif jstdt.hour > 17:
            echo_message =\
                random.choice(('もう夜やで！', 'もう夜でっせ！', '体内時計狂ってるやん...'))

        # メッセージを送信
        await message.channel.send(echo_message)

    # それ以外
    else:

        # メッセージのスコアを取得
        message_scores = mybot.eval(message.content)
        message_scores =\
            sorted(message_scores.items(), key=lambda x: x[1], reverse=True)

        # メッセージを評価
        if message_scores:
            # 上位3つのタグを返却
            await message.channel.send(f'{message_scores[0][0]}の話？')
        else:
            # そもそもBotにデータが登録されていない
            await message.channel.send('ばなな☆')


# Botクライアントを起動
client.run(TOKEN)

# ボットを終了
mybot.exit()
