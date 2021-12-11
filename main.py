import random           
import sys
import time
import requests
import urllib3
import json
import datetime

"""乐健体育模拟跑步分析"""
"""author:sake"""
class LegymPost:
    def __init__(self) -> None: 
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        #账号密码输入         
        if (len(sys.argv) == 0):
            print("账号密码不能为空")
            exit(-1)
        self.userName = sys.argv[1] 
        self.password = sys.argv[2]
        self.distance = sys.argv[3]
        
        self.headers = {
                        "user-agent": "Mozilla/5.0 (Linux; Android 11; LE2123 Build/RQ3A.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/36.07843)",
                        "Content-Type": "application/json"}          #请求头部
        self.login_url = ("https://cpes.legym.cn/authorization/user/manage/login")
        self.login_data = {
                        "entrance":"1",
                        "password":self.password,
                        "userName":self.userName }             #登录数据包
        try:    
            self.login_response = requests.post(self.login_url, headers = self.headers, data = json.dumps(self.login_data), verify = False)   #登录验证并检查状态
            self.message: dict = self.login_response.json()["message"]
            if self.message != None:
                print(self.message)                  #返回错误信息的message
            if self.login_response.status_code != 200:
                print("网络连接失败")             #状态码不为200               
        except Exception as e:
            print(e)

        #获取response里的关键数据       
        self.data: dict = self.login_response.json()["data"]
        self.token: str = self.data.get("accessToken", None)
        self.schoolId: str = self.data.get("schoolId", None)
        self.headers.update({"authorization": "Bearer "+self.token,"Organization": self.schoolId})

        # 获取userid，活动签到用
        fitness_url = 'https://cpes.legym.cn/fitness/fitness/app/info'
        data = {"year":0}
        r = requests.post(fitness_url,headers=self.headers,data=json.dumps(data))
        self.userId:str = r.json()['data']['userId']


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

    #获取课外活动列表    
    def getActivityList(self) -> list:
        url = 'https://cpes.legym.cn/education/app/activity/getActivityList'
        data = {"name":"","campus":"","page":1,"size":10,"state":"","topicId":"","week":""}
        r = requests.post(url=url, headers=self.headers, data=json.dumps(data),verify=False)
        activityList:list = r.json()['data']['items']
        lst = [item[key] for item in activityList for key in item]
        return lst

    #活动报名
    def signUpActivity(self, activityId:str) -> str:
        url = 'https://cpes.legym.cn/education/app/activity/signUp'
        data = {"activityId":activityId}
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response.text
    
    #活动签到
    def signInActivity(self, activityId:str) -> str:
        url = 'https://cpes.legym.cn/education/activity/app/attainability/sign'
        data = {
            "activityId": activityId,
            "times": "1",
            "pageType": "activity",
            "userId": self.userId,
            "activityType": 0,
            "attainabilityType": 1
        }
        r = requests.put(url=url, headers=self.headers, data=json.dumps(data))
        return r.text
    
    #活动批量报名签到
    def Activity(self):
        lst = app.getActivityList()
        for i in range(0,int(len(lst)/20)):
            print(app.signUpActivity(lst[20*i]))
            print(app.signInActivity(lst[20*i]))   

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
                "avePace": random_time *60 / distance * 1000 + random.randint(0,1) / 10,
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
    app=LegymPost()
    app.__init__()          #登录
    app.Activity()          #签到
    app.run_route()         #跑步
    