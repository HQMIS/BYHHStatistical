#-*-coding:utf-8-*-

# script: BYHHStatistical.py
# author: huangqimin@baidu.com

# note: 
# 1、This Python Script use Library requests:
#    see http://docs.python-requests.org/en/v1.0.0/
# 2、BYHH的所有页面Url均显示为http://byhh.net/main.html:
#    想要找到实际地址，可以利用Chrome的F12（审查元素）
# 3、 未找到可以一次 请求某个版面所有帖子的Url，每次只能请求20个:
#    而且BYHH有防爬虫系统，虽然请求间隔之间随机sleep一段时间，也没法请求道所有的，最后还是被判为爬虫，后续研究

import requests
import random
import time

class BYHH:
    def __init__(self):
        pass

    def getCount(self, url):
        r = requests.get(url)
        count =  r.text.split("><a href=bbsqry?userid=")[-2].split(">")[-4].split("<")[0]
        userList = [i.split(">")[0] for i in r.text.split("><a href=bbsqry?userid=")[1:]]
        return count,  userList
        
    def spider(self):
        print "Sorry, You are Attested As A Spider!"

if __name__ == '__main__':
    board = raw_input("Board Name Input: ")
    
    stat = {}
    sleeptime = 15
    firstPostNum = "1"
    count = "1"

    byhh = BYHH()

    ## Board Url
    url = "http://byhh.net/cgi-bin/bbsdoc?board="+board
    try:
        count, userList = byhh.getCount(url)
        print board+"Post Number: "+count

        while int(firstPostNum) < int(count):
            try:
                ## Post List Url
                url = "http://byhh.net/cgi-bin/bbsdoc?board="+board+"&start="+firstPostNum
                lastPostNum, userList = byhh.getCount(url)
                print lastPostNum

                firstPostNum = str(int(lastPostNum) + 1)
                for _id in userList:
                    try:
                        stat[_id] = stat[_id] + 1
                    except:
                        stat[_id] = 1

                userstat = sorted(stat.items(), key=lambda d: d[1], reverse=True)
                print userstat

                # BYHH会检测，是否为机器登录
                # 看到的是如果sleeptime时间为一个数，则被判为机器登录
                # 所以这里生成随机数来处理
                sleeptime = 15 + random.randint(0, 15)
                time.sleep(sleeptime)
            except:
                firstPostNum = count
                byhh.spider()
    except:
        byhh.spider()
