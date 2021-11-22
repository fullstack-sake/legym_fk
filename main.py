import random           
import sys
import time
import requests
import urllib3
import json
"""乐健体育模拟跑步分析"""
"""author:sake"""
class LegymPost:
    def __init__(self) -> None:                 
        if (len(sys.argv) == 0):
            print("账号密码不能为空")
            exit(-1)
        self.userName = sys.argv[1] 
        self.password = sys.argv[2]
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 11; LE2123 Build/RQ3A.211001.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/36.07843)",
            "Content-Type": "application/json",
            "Host": "cpes.legym.cn",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            }       #请求头
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.login_url = ("https://cpes.legym.cn/authorization/user/manage/login")
        self.login_data = {
            "entrance":"1",
            "password":self.password,
            "userName":self.userName
            }           #登录数据包
        self.run_url = ("https://cpes.legym.cn/running/app/uploadRunningDetails")
        
        self.run_data = json.load(open('run.json',encoding='gbk',errors='ignore'))
        self.run_data.update({"endTime": time.strftime("%F %H:%M:%S").center(60)})
    def check_user_status(self) -> None:       #检查登录状态 
        try:    
                response = requests.post(
                url = self.login_url,
                headers = self.headers,
                data = json.dumps(self.login_data),
                verify = False)       #开始登录验证
                print(response.text)
        except Exception as e:
            print(e)
            return 0
        message: dict = response.json()["message"]
        if message != None:
            print(message)
            return 0                #返回错误信息的message
        if response.status_code != 200:
            print("网络连接失败")
            return 0                #状态码不为200
        
    def run_route(self) -> None:
        try:    
                self.headers.update({"authorization": "Bearer cae0458b-93a9-4a64-b465-6b4e9b3f5820"})
                response = requests.post(
                url = self.run_url,
                headers = self.headers,
                data = json.dumps(self.run_data),
                verify = False)       #开始跑步发包
                print(response.text)
        except Exception as e:
            print(e)
            return 0


      
        return 0  
if __name__ == "__main__":
    print(time.strftime("%F %H:%M:%S").center(60))
    
    LegymPost().check_user_status()
    LegymPost().run_route()

    