# (c) Takuya Kimura (takuyakimura0507@gmail.com)

import json
import math


# 説明：任意のテキストからトピックごとにそのテキストの類似度を計算する
#    単語ごとにタグを付与したデータ群を準備しておく(self.dataとして読み込む)。
#    与えられた任意のテキスト内の各単語をカウントし、
#    単語に関連付けられたタグにスコアを付与し、テキスト内の各単語の出現回数の重複から
#    テキストの各タグに対する関連性を計算する。
class MyBot:

    # 説明：Botを初期化する
    # 引数：
    #     path ... Botデータが記録されているファイルへのパス
    def __init__(self, path: str) -> None:
        self.data = {}  # Botが保持する単語とタグの対応データ
        self.rate = {}  # 単語に対してタグが付与される割合によってスコアを正規化する補正係数
        self.path = path  # ターゲットパス
        self.load()

    # 説明：Botデータをファイルに読み込む
    def load(self):

        # データの読み込み
        with open(self.path, 'r') as fp:
            self.data = json.load(fp)

        # 補正係数を初期化する
        self.rate.clear()

        # 補正係数を再計算する
        for tags in self.data.values():
            for tag in tags:
                self.rate.setdefault(tag, 0)
                self.rate[tag] += 1

        for tag in self.rate:
            # sqrtを利用するのは単純な逆数係数による極端なポイントの分配を防止するため
            # sqrtの引数が(0,1)の区間内の場合、戻り値は非線形により大きくなる。
            # ここで、rateの要素はすべて1以上であることが保証されている
            self.rate[tag] = math.sqrt(1/self.rate[tag])

    # 説明：Botデータをファイルに書き込む
    def save(self):
        with open(self.path, 'w') as fp:
            json.dump(self.data, fp)

    # 説明：テキストをデータをもとに評価
    # 引数：
    #     text ... キーワードが含まれている任意のテキスト
    # 返却：タグ名がキー、スコアが値の辞書
    def eval(self, text: str) -> dict:
        text = text.lower()
        scores = {}
        for key, tags in self.data.items():
            score = text.count(key.lower())
            for tag in tags:
                scores.setdefault(tag, 0)
                scores[tag] += score
        for tag in self.rate:
            scores[tag] *= self.rate[tag]
        return scores

    # 説明：終了処理を列挙する
    def exit(self):
        self.save()
