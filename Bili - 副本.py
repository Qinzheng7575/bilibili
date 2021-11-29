import requests
import json
import datetime
import matplotlib.pyplot as plt
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
        self.Cookie = open('bilibili_spy/Cookie.txt', 'r', encoding='utf-8').read()
        self.User_Agent=open('bilibili_spy/User-Agent.txt', 'r', encoding='utf-8').read()
        self.header = {
        "Cookie": self.Cookie,
        "User-Agent":self.User_Agent,
        }
        self.count_1=0
        self.count_2=0
        self.count_3=0
        self.count_4=0
        self.count_5=0
        self.count_6=0





    def Get_video(self,count,n):
        url_temp=self.URL_video_1+str(n)+self.URL_video_2
        #pn=page number
        # data = requests.get(self.URL_video, headers=self.header)
        data = requests.get(url_temp, headers=self.header)
        if data.status_code == 200:
            videos = data.json()['data']['list']['vlist']
            temp=0
            for i in videos:
                if temp < count:
                    temp += 1
                    self.new_inc+=i["play"]
                    # print( "{}。{} \n播放量：{} 评论：{}，弹幕：{}".format( temp,i['title'],i['play'],i['comment'],i['video_review']))
                    if i['play']<1000:
                        self.count_1+=1
                    elif i['play']>1000 and i['play']<2000:
                        self.count_2+=1
                    elif i['play']>2000 and i['play']<3000:
                        self.count_3+=1
                    elif i['play']>3000 and i['play']<5000:
                        self.count_4+=1
                    elif i['play']>5000 and i['play']<10000:
                        self.count_5+=1
                    elif i['play']>10000:
                        self.count_6+=1
        else:
            print("search接口请求出错")

if __name__ == "__main__":
    B = Bili_Vdou()


    for i in range(8):
        B.Get_video(30,i+1)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    waters = ('<1k', '1k~2k', '2k~3k', '3k~5k', '5k~1w','>1w')
    buy_number = [B.count_1, B.count_2, B.count_3, B.count_4, B.count_5,B.count_6]
    
    plt.bar(waters, buy_number)
    plt.title('去年播放量分档统计')
    
    plt.show()