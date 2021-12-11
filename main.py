from operator import setitem
import random           
import sys
import time
import requests
import urllib3
from urllib.parse import urlencode
import json
import datetime

"""乐健体育模拟跑步分析"""
"""author:sake"""
class LegymPost:
    def __init__(self) -> None: 
        #账号密码输入         
        if (len(sys.argv) == 0):
            print("账号密码不能为空")
            exit(-1)
        self.userName = sys.argv[1] 
        self.password = sys.argv[2]
        self.distance = sys.argv[3]
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        #登录验证
        self.headers = {
                        "user-agent": "Mozilla/5.0 (Linux; Android 11; LE2123 Build/RQ3A.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/36.07843)",
                        "Content-Type": "application/json"}          #请求头部
        self.login_url = ("https://cpes.legym.cn/authorization/user/manage/login")
        self.login_data = {
            "entrance":"1",
            "password":self.password,
            "userName":self.userName }             #登录数据包
        try:    
            self.login_response = requests.post(self.login_url, headers = self.headers, data = json.dumps(self.login_data), verify = False)   #开始登录验证
        except Exception as e:
            print(e)

        #获取response里的关键数据
        self.message: dict = self.login_response.json()["message"]
        self.data: dict = self.login_response.json()["data"]
        self.token: str = self.data.get("accessToken", None)
        self.schoolId: str = self.data.get("schoolId", None)
        self.headers.update({"authorization": "Bearer "+self.token,"Organization": self.schoolId})

        # 获取userid，活动签到用
        fitness_url = 'https://cpes.legym.cn/fitness/fitness/app/info'
        data = {"year":0}
        r = requests.post(fitness_url,headers=self.headers,data=json.dumps(data))
        self.userId:str = r.json()['data']['userId']
        

    #检查登录状态
    def check_login_status(self) -> str:        
        
        if self.message != None:
            print(self.message)
            return 0                #返回错误信息的message
        if self.login_response.status_code != 200:
            print("网络连接失败")
            return 0                #状态码不为200
        
    #获取semesterId
    def semesterId(self):
        url = "https://cpes.legym.cn/education/semester/getCurrent" 
        current_response = requests.get(url, headers = self.headers, verify = False)
        data: dict = current_response.json()["data"]
        self.semesterId: str = data.get("id", None)
        return self.semesterId

    #获取limitation
    def limitation(self):
        url = "https://cpes.legym.cn/running/app/getRunningLimit"
        data ={"semesterId": (LegymPost().semesterId())}
        with open("limit.json","w",encoding='gbk',errors='ignore') as f:
                json.dump(data,f)
        self.limit_data = json.load(open('limit.json',encoding='gbk',errors='ignore'))
        limit_response = requests.post(url,headers = self.headers, data = json.dumps(self.limit_data), verify = False)
        data: dict = limit_response.json()["data"]
        self.limitation: str = data.get("limitationsGoalsSexInfoId", None)
        return self.limitation

    def getActivityList(self) -> list:
        """获取课外活动列表
        ---
        每周三次打卡的锻炼活动

        :return `list`: 课外活动列表
        """
        url = 'https://cpes.legym.cn/education/app/activity/getActivityList'
        data = {"name":"","campus":"","page":1,"size":10,"state":"","topicId":"","week":""}
        r = requests.post(url=url, headers=self.headers, data=json.dumps(data),verify=False)
        # print(r.json())
        activityList:list = r.json()['data']['items']
        return activityList


    def activityDetail(self, activityId:str) -> dict:
        """活动详情
        ---
        获取课外活动的详情，暂时可能没用
        
        :param `activityId` : 活动id
        
        :return `dict` : 活动详情信息
        """
        url = f'https://cpes.legym.cn//education/app/activity/getStudentActivityDetail?activityId={activityId}'
        r = requests.get(url, headers=self.headers,verify=False)
        detail = r.json()['data']

    
    def signUpActivity(self, activityId:str) -> str:
        """活动报名
        ---
        活动报名，可以报名未开始的活动，服务端不验证报名是否开始
        
        :param `activityId` : 活动id
        
        :return `str` : 响应数据
        """
        url = 'https://cpes.legym.cn/education/app/activity/signUp'
        data = {"activityId":activityId}
        r = requests.post(url, headers=self.headers, data=json.dumps(data))
        response = r.text

        return response
    
    def signInActivity(self, activityId:str) -> str:
        """活动签到
        ---
        进行活动的签到，活动签到不需要位置信息，位置信息仅在客户端验证
        
        :param `activityId` : 活动id
        
        :return `str` : response body
        """
        url = 'https://cpes.legym.cn/education/activity/app/attainability/sign'
        data = {
            "activityId": activityId,
            "times": "1",
            "pageType": "activity",
            "userId": self.userId,
            "activityType": 0,
            "attainabilityType": 2
        }
        r = requests.put(url=url, headers=self.headers, data=json.dumps(data))

        return r.text

    def signInSimple(self, activityId:str) -> None:
        """签到详情界面
        ---
        只是用来更逼真地模拟签到流程
        
        :param `activityId` : 活动id
        
        :return `None` : 无返回值
        """
        url = 'https://cpes.legym.cn/education/activity/simple/attainability/get'
        data = {"simpleActivityId":activityId,"times":"1"}
        r = requests.post(url, headers=self.headers, data=json.dumps(data))

        return 0
        

    #发送跑步数据
    def run_route(self) -> None:
        random_time= random.randint(20,30)
        self.headers.update({"user-agent": "okhttp/4.2.2"})
        distance =float(self.distance)
        endtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starttime = (datetime.datetime.now()-datetime.timedelta(minutes=random_time)).strftime("%Y-%m-%d %H:%M:%S")
        data ={
                "scoringType": 1,
                "semesterId": LegymPost().semesterId(),
                "signPoint": [],
                "startTime": starttime,
                "totalMileage": distance,
                "totalPart": 0.0,
                "type": "自由跑",
                "uneffectiveReason": "",
                "avePace": random_time * 60/ distance * 1000 + random.randint(0,1) / 10,
                "calorie": int(distance * random.uniform(70.0,75.0)),
                "effectiveMileage": distance,
                "effectivePart": 1,
                "endTime": endtime,
                "gpsMileage": distance,
                "limitationsGoalsSexInfoId":LegymPost().limitation(),
                "paceNumber": distance * (random.randint(50,150)),
                "paceRange": random.randint(5,10),
                "routineLine": [{ "latitude": 30.756303201239845, "longitude": 103.93206457325871 },
                                { "latitude": 30.756346614671184, "longitude": 103.93206545656531 }, 
                                { "latitude": 30.756359404607583, "longitude": 103.93407893568614 }, 
                                { "latitude": 30.753229499261558, "longitude": 103.93407611144278 }]
                }
        with open("run.json","w",encoding='gbk',errors='ignore') as f:
                json.dump(data,f)
        self.run_data = json.load(open('run.json',encoding='gbk',errors='ignore'))
        url = ("https://cpes.legym.cn/running/app/uploadRunningDetails")
        response = requests.post(url, headers = self.headers, data = json.dumps(self.run_data), verify = False)       #开始跑步发包
        print(response.text)
        return 0  

if __name__ == "__main__":
    print(time.strftime("%F %H:%M:%S").center(60))
    LegymPost().__init__()
    LegymPost().check_login_status()
    LegymPost().run_route()
    