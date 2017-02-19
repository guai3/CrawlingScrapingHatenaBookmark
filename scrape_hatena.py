#!/usr/bin/env python
# coding: UTF-8
# はてなブックマークの人気エントリーを日付ごとに取得してMysqlに格納する
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date as ddate
from datetime import datetime as datetime
from datetime import timedelta as timedelta

import pymysql
import re
import sys
import os.path

# ブックマークエントリーの内容を格納する。
class Bookmark():
    count = 0

    def __init__(self, dateurl):
        Bookmark.count += 1
        self.dateurl = dateurl
        self._date_ = self.dateurl[-8:]
        self.date = ddate(int(self._date_[:4]),
                          int(self._date_[4:6]),
                          int(self._date_[6:8]))

    def setUrl(self, url):
        self.url = url

    def setTitle(self, title):
        self.title = title

    def setHatebu(self, hatebu):
        self.hatebu = int(hatebu)

    def setCategory(self, category):
        self.category = category

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setDomain(self, domain):
        self.domain = domain

    def setHatenaurl(self, hatenaurl):
        self.hatenaurl = hatenaurl

# Mysqlに接続する
class connectMysql():

    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    unix_socket='/tmp/mysql.sock',
                                    user='root',
                                    passwd=None,
                                    db='mysql',
                                    charset='utf8mb4')

        self.cur = self.conn.cursor()
        self.cur.execute("USE dailydata")

# 該当日のURLのホットエントリーをパースしてMysqlにINSERTする関数
def getHotentry(day):

    bookmarkurl = "http://b.hatena.ne.jp"

    try:
        dateurl = "http://b.hatena.ne.jp/hotentry/" + day
        html = urlopen(dateurl).read()
        bsObj = BeautifulSoup(html, "html.parser")

    except HTTPError as e:
        print(str(e))

    except URLError as e:
        print(str(e))

    # データが含まれているタグを定義
    blist = bsObj.findAll("a", class_="entry-link")
    blist2 = bsObj.findAll("a", {"data-track-click-target": "entry"})
    blist3 = bsObj.findAll("li", class_="category")
    blist4 = bsObj.findAll("li", class_="date")
    blist5 = bsObj.findAll("li", class_="domain")
    hatenaurls = bsObj.findAll("ul", class_="users")

    bukuma = []
    j = 0

    for i in range(len(blist)):
        a = Bookmark(dateurl)
        bukuma.append(a)
        bukuma[i].setTitle(blist[i].get("title"))
        bukuma[i].setUrl(blist[i].get("href"))
        try:
            if blist2[i + j].span is None:
                j += 1
        except:
            print(dateurl)
            print("該当の日付のデータが存在しないので､プログラムを終了します")
            sys.exit()

        bukuma[i].setHatebu(
            re.search(r"[0-9]+", str(blist2[i + j].span)).group())
        bukuma[i].setCategory(
            re.search(r"\">.{1,10}</", str(blist3[i])).group()[2:-2])

        bukuma[i].setTimestamp(blist4[i].string)
        bukuma[i].setDomain(blist5[i].span.string)

        print(bukuma[i].title)

        try:
            bukuma[i].setHatenaurl(
                bookmarkurl + hatenaurls[i].li.strong.a.get("href"))
        except AttributeError:
            try:
                bukuma[i].setHatenaurl(
                    bookmarkurl + hatenaurls[i].li.em.a.get("href"))
            except AttributeError:
                try:
                    bukuma[i].setHatenaurl(
                        bookmarkurl + hatenaurls[i].li.a.get("href"))
                except:
                    bukuma[i].setHatenaurl("")

    try:
        for i in range(len(bukuma)):
            print(bukuma[i].title)
            try:
                cur.cur.execute("INSERT INTO hatenabookmark \
                         (bookmarkdate, \
                         timestamp, \
                         url, \
                         domain, \
                         title, \
                         hatebu, \
                         category,\
                         htnurl)VALUES\
                          (%s,%s,%s,%s,%s,%s,%s,%s)",
                                (bukuma[i].date,
                                 bukuma[i].timestamp,
                                 bukuma[i].url,
                                 bukuma[i].domain,
                                 bukuma[i].title,
                                 bukuma[i].hatebu,
                                 bukuma[i].category,
                                 bukuma[i].hatenaurl))
            except:
                pass  # エラー処理を書こう！

        cur.cur.connection.commit()

    finally:
        print("レコード数: " + str(Bookmark.count))
        print(day)

# 終了処理を行う
# 実行時間の表示、ログ吐き出し、データベースのクローズ


def endProcess(begin, term, starttime):
    # ターミナルに実行結果を表示
    elapsedtime = datetime.now() - starttime
    today = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    strElapsedtime = "経過時間: " + str(elapsedtime)[:10]
    strBookmarkcount = "総レコード数: " + str(Bookmark.count)

    print("")
    print(strBookmarkcount)
    print(strElapsedtime)

    # ログファイルに書き込み
    if os.path.isfile("getdailydatalog.txt"):
        f = open("getdailydatalog.txt", "a")
    else:
        f = open("getdailydatalog.txt", "w")
    f.write(today + u"\n")
    f.write(str(__file__) + u"\n")
    f.write(u"開始日 " + begin + u"\n")
    f.write(u"期間 " + str(term) + u"日間\n")
    f.write(strBookmarkcount + u"\n")
    f.write(strElapsedtime + u"\n")
    f.write("\n\n")
    f.close()

    cur.cur.close()
    cur.conn.close()
    print(u"\n処理が終了しました。")
    sys.exit()

if __name__ == '__main__':

    # データ取得開始日と期間を設定
    # コマンドライン引数で日付と日数を指定する。
    param = sys.argv
    if len(param) == 3:  # 引数が２つ入力された場合、日付からの期間のデータを取得
        begin = str(param[1])   # YYYYMMDDで日付を入力する。
        term = param[2]        # 366以下の数字を入力する。
    elif len(param) == 2:  # 引数が１つ入力された場合、その日付のデータのみ取得
        begin = str(param[1])   # YYYYMMDDで日付を入力する。
        term = "1"             # 次の処理で正規表現でチェックするので、文字列で代入
    elif len(param) == 1:  # 引数が入力されなかった場合、取得した日付の一覧を表示する
        cur = connectMysql()
        cur.cur.execute("SELECT \
                            bookmarkdate,count(*) \
                         FROM \
                            hatenabookmark \
                         GROUP BY \
                            bookmarkdate;")
        for i in cur.cur.fetchall():
            print(i[0], i[1])
        cur.cur.close()
        cur.conn.close()
        sys.exit()
    else:  # 引数が3つ以上入力された場合。終了させる。
        print("引数は二つまでしか入力出来ません。")
        sys.exit()

    # YYYYMMDD形式かをチェック
    try:
        datetime.strptime(begin, '%Y%m%d')
    except:
        print("正しい日付を入力して下さい")
        sys.exit()

    # 366以下かどうかをチェック
    try:
        re.match(r"[0-9]+", term).group()
        term = int(term)
    except:
        print("第２引数は取得したい日数を入力して下さい。")
        sys.exit()

    if term > 366:
        print("366より大きい数字は入力出来ません。")
        sys.exit()

    try:
        cur = connectMysql()
    except:
        print("データベースに正常に接続できませんでした｡プログラムを終了します｡")
        sys.exit()

    # はてなブックマークの末尾日付URLのリスト作成
    days = []
    for i in range(term):
        day = datetime.strptime(begin, '%Y%m%d') + timedelta(days=i)
        days.append(day.strftime('%Y%m%d'))

    starttime = datetime.now()  # データ取得開始時刻の取得

    # 取得した日付リストを引数にしてパースをループさせる。
    for day in days:
        getHotentry(day)

    endProcess(begin, term, starttime)
