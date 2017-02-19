#!/usr/bin/env python
# coding: UTF-8
# DBに格納されている、URLのリンク先が生きているかを確認するスクリプト
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import date as ddate
from datetime import datetime as datetime
from datetime import timedelta as timedelta
import pymysql
import re
import sys
import json


# 該当日のURLのホットエントリーをパースしてMysqlにINSERTする関数
def getlink(line):

    # SQLを実行して結果を受け取る
    sql = "SELECT id,title,url,htnurl \
           from hatenabookmark where id = " + str(line)
    try:
        cur.execute(sql)

    except:
        pass  # エラー処理を書こう！

    row = cur.fetchall()
    # ↑row[0][0]= id row[0][1]=title row[0][2] = url row[0][3]=htnurl
    error = ""
    errorcontent = ""
    errottitle = str(row[0][0]) + " " + row[0][1]
    title = ""
    try:
        url = row[0][2]
        html = urlopen(url).read()
        bsObj = BeautifulSoup(html, "html.parser")

    except HTTPError as e:
        print(errottitle)
        print(str(e))
        errorcontent = str(e)
        error = "HTTPError"
        print("")

    except URLError as e:
        print(errottitle)
        print(str(e))
        errorcontent = str(e)
        error = "URLError"
        print("")
    except:
        print(errottitle)
        error = "otherError"
        print("otherError")
        print("")

# テストエリア

    jsonurl = "http://b.hatena.ne.jp/entry/jsonlite/?url="
    url = jsonurl + quote(url)
    print(url)
    html = urlopen(url).read().decode('utf-8')
    responsjson = json.loads(html)
    comment_count = 0
    for i in range(len(responsjson["bookmarks"])):
        if responsjson["bookmarks"][i]["comment"] != "":
            comment_count += 1

    print(row[0][1])
    print("コメント数" + str(comment_count))
    print("")

    comment_count = str(comment_count)
# テストエリア

    if error == "":
        # ターゲットのURLのタイトル

        if bsObj.find("title") is None:
            print(errottitle)
            print("NotitleError")
            error = "NoTitleError"
            title = "NoTitle"
            print("")

        elif bsObj.find("title").string is None:
            print(errottitle)
            print("NotitleError")
            error = "NoTitleError"
            title = "NoTitle"
            print("")

        else:
            title = bsObj.find("title").string

    if error == "":

        sql = "UPDATE hatenabookmark SET nowtitle = \"" + title + \
            "\", comment_count = \"" + comment_count + \
            "\" WHERE id = " + str(line)

        try:
            cur.execute(sql)
        except:
            print("#エラー処理を書こう！")

        finally:
            cur.connection.commit()

    else:
        sql = "UPDATE hatenabookmark SET linkerror = \"" + error +  \
            "\", errorcontent = \"" + errorcontent + \
            "\", comment_count = \"" + comment_count + \
            "\", nowtitle = \"" + title + \
            "\" WHERE id = " + str(line)

        try:
            cur.execute(sql)
        except:
            print("#エラー処理を書こう！")

        finally:
            cur.connection.commit()

# 終了処理を行う


def endProcess(starttime):
    # ターミナルに実行結果を表示
    elapsedtime = datetime.now() - starttime
    strElapsedtime = "経過時間: " + str(elapsedtime)[:10]
    print(strElapsedtime)

    cur.close()
    conn.close()
    print(u"\n処理が終了しました。")
    sys.exit()

if __name__ == '__main__':

    try:
        # ローカルのMysqlに接続確認
        conn = pymysql.connect(host='127.0.0.1',
                               unix_socket='/tmp/mysql.sock',
                               user='root',
                               passwd=None,
                               db='mysql',
                               charset='utf8mb4')
        cur = conn.cursor()
        cur.execute("USE dailydata")
    except:
        sys.exit()

    starttime = datetime.now()  # 開始時刻の取得

# IDが1からの連番で欠番がないという前提。
    lines = cur.execute("select id from hatenabookmark;")  # 結果の行数をループ変数へ代入。
    for line in range(150, 300):
        # for line in range(lines):
        print(line + 1)
        getlink(line + 1)

    endProcess(starttime)
