#!/usr/bin/env python
# coding: UTF-8
# はてなブックマークコメントの数を取得するプログラム
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import date as ddate
from datetime import datetime as datetime
from datetime import timedelta as timedelta
import pymysql
import re,sys
from collections import Counter
from janome.tokenizer import Tokenizer
from tqdm import tqdm


#終了処理を行う
def endProcess(starttime):
    #ターミナルに実行結果を表示
    elapsedtime = datetime.now() - starttime
    strElapsedtime =  "経過時間: " + str(elapsedtime)[:10]
    print(strElapsedtime)

    cur.close()
    conn.close()
    print(u"\n処理が終了しました。")
    sys.exit()

if __name__ == '__main__':

    try:
        #ローカルのMysqlに接続確認
        conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                user='root', passwd=None, db='mysql', charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("USE dailydata")
    except:
        sys.exit()

    starttime = datetime.now() #開始時刻の取得


    cur.execute("select title from hatenabookmark limit 1000;")

    titles = cur.fetchall()
    t = Tokenizer()
    lists = []
    for title in tqdm(titles):
        tokens = t.tokenize(title[0])

        for token in tokens:
            if token.part_of_speech[:2] == "名詞":
                lists.append(token.surface)

    print(Counter(lists).most_common())
    print(len(lists))
    print(len(set(lists)))
    endProcess(starttime)
