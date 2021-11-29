import requests
import json
import datetime
import time
from threading import Thread

class Decorator:
    def __init__(self):
        pass

    @staticmethod
    def timer(func):#计时器
        def wrapper(*args,**kw):
            start=time.time()
            #真正执行的是这行。
            func(*args,**kw)
            last=time.time()-start
            print("\n----本次统计总共花费时间%.3f----"%last)
        return wrapper

class Bili_Vdou:
    def __init__(self):
        self.follow_7day = 0
        self.total_fans = 0
        self.inc_7day = 0
        self.new_inc=0
        
        self.URL_follow = 'https://member.bilibili.com/x/web/index/stat'
        self.URL_inc='https://member.bilibili.com/x/web/data/pandect?tmid=238190151&type=1'
        self.URL_video='https://api.bilibili.com/x/space/arc/search?mid=238190151&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
        self.URL_video_1='https://api.bilibili.com/x/space/arc/search?mid=238190151&ps=30&tid=0&pn='
        self.URL_video_2='&keyword=&order=pubdate&jsonp=jsonp'
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[0:10]
        self.date="".join( list(filter(str.isdigit,self.time)))#str
        self.Cookie = open('bilibili_spy/bilibili/Cookie.txt', 'r', encoding='utf-8').read()
        self.User_Agent=open('bilibili_spy/bilibili/User-Agent.txt', 'r', encoding='utf-8').read()

        self.header = {
        "Cookie": self.Cookie,
        "User-Agent":self.User_Agent,
        }
   
    # @Decorator.timer
    def Get_7day_fans(self):
        data = requests.get(self.URL_follow, headers=self.header)
        if data.status_code == 200:

            follow_all = data.json()['data']['fan_recent_thirty']['follow']
            for i in follow_all:

                if str(int(self.date)-7)<=i:
                # if '20201025'<=i:
                    self.follow_7day += follow_all[i]
                    # print(i, ":", follow_all[i])
        else:
            print("sta接口请求出错")
        print("七日总关注人数：",self.follow_7day)

    def Get_total_fans(self):
        data = requests.get(self.URL_follow, headers=self.header)

        if data.status_code == 200:
            # print(data.json())
            self.total_fans = data.json()['data']['total_fans']
        else:
            print("sta接口请求出错")
        print("目前总粉丝：", self.total_fans)

    def Get_7day_inc(self):
        data = requests.get(self.URL_inc, headers=self.header)
        if data.status_code == 200:

            inc = data.json()['data']
            temp=0
            for i in inc:
                if temp < 7:
                    self.inc_7day+=i['total_inc']
                    # print(i['total_inc'])
                    temp+=1
        else:
            print("pandect接口请求出错")
        print("七日新增播放量：",self.inc_7day)

    def Get_video(self,count):
        url_temp=self.URL_video
        # data = requests.get(self.URL_video, headers=self.header)
        data = requests.get(url_temp, headers=self.header)
        if data.status_code == 200:
            videos = data.json()['data']['list']['vlist']
            temp=0
            for i in videos:
                if temp < count:
                    temp += 1
                    self.new_inc+=i["play"]
                    print( "{}。{} \n播放量：{} 评论：{}，弹幕：{}".format( temp,i['title'],i['play'],i['comment'],i['video_review']))
        else:
            print("search接口请求出错")
        print("\n本周发布视频播放量：",self.new_inc)


if __name__ =='__main__':
    days=6
    B = Bili_Vdou()

    @Decorator.timer
    def do(analysis_days):
        print("{} B站运营统计".format(B.time))
        thread_lists=[]
        thread_lists.extend([Thread(target=B.Get_total_fans,args=()),
                                Thread(target=B.Get_7day_fans,args=()),
                                Thread(target=B.Get_video,args=(analysis_days,)),
                                Thread(target=B.Get_7day_inc,args=())
                                ])
        for thread in thread_lists:
            thread.start() 
            thread.join()          
        # B.Get_total_fans()     
        # B.Get_7day_fans()     
        # B.Get_video(6)
        # B.Get_7day_inc()
    do(days)



