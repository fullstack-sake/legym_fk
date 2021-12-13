# 乐健体育模拟跑步与活动签到
## 项目介绍

- 本项目仅适用于**乐健体育**
- 对代码改进有任何好的建议，欢迎提`Issues`，或者直接`PR`，感谢:handshake::heart:!!
- 如果对您有帮助，请顺手点个`Star`吧
- **Author**:smiley::  [**sake**](https://github.com/fullstack-sake)

------

## 模拟跑步与活动签到原理

先用`frida`配合此项目仓库的`sake.js`来**hook**证书验证，干掉**乐健体育**的`ssl pinning`，然后进行`packetcapture`。通过分析`packet`，向相应站点`get`或`post`不同的`json`进行`forward packet`，就可以实现**无乐健体育式模拟跑步与活动签到**。


### 站点1：Login
 **为用户提供登录服务**

采用`post`方法，`body`如下：

```python
body = {"entrance":"1","password":"password","userName":"18888888888"}
```

返还的`response`可以获取到很多关键数据：`accessToken`，`organizationId`

### 站点2：getCurrent

采用`get`方法，这里返还的`response`我们只需要`semesterId`


### 站点3：getRunningLimit

`body`要提供`getCurrent`获取的`semesterId`，这里返还的`response`我们只需要`limitationsGoalsSexInfoId`

### 站点4：uploadRunningDetails

**上传跑步数据**

`headers`中需提供`Authorization`，采用了`Bearer<token>`，可以通过获取登录的`response`的`accesstoken`拼接为`Bearer accesstoken`

采用`post`方法，`body`结构为

```python
data ={
       "scoringType": 1,
       "semesterId": semesterId,
       "signPoint": [],
       "startTime": starttime,
       "totalMileage": distance,
       "totalPart": 0.0,
       "type": 跑步类型,
       "uneffectiveReason": "",
       "avePace": random_time / distance * 1000 + random.randint(0,1) / 10,
       "calorie": int(distance * random.uniform(70.0,75.0)),
       "effectiveMileage": distance,
       "effectivePart": 1,
       "endTime": endtime,
       "gpsMileage": distance,
       "limitationsGoalsSexInfoId":limitationsGoalsSexInfoId,
       "paceNumber": distance * (random.randint(50,150)),
       "paceRange": random.randint(5,10),
       "routineLine": [跑步路线]
        }
```

### 站点5：getActivityList

**获取课外活动列表**

采用`post`方法，这里返还的`response`我们只需要`ActivityId`

### 站点6：signUpActivity

**活动报名**

可以报名未开始的活动，服务端不验证报名是否开始。

采用`post`方法，要提供`getActivityList`获取的`ActivityId`

### 站点7：signInActivity

**活动签到**

进行活动的签到，活动签到不需要位置信息，位置信息仅在客户端验证

采用`post`方法，要提供`getActivityList`获取的`ActivityId`


------

## 使用方法

### 如果部署了python环境：

直接将**main.py**文件 **raw** 到本地，然后在终端/命令提示符下输入`python main.py 账号 密码 里程 参加活动的关键词`

 ![a1](https://raw.githubusercontent.com/NightFrost42/legym_fk/main/images/a1.png)



### 如果未部署python环境：

1. 将本仓库`Fork`到自己的仓库里；
 ![1](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/1.png)


2. 点击`Settings`→`Secrets`→`New repository secret`。
 ![2](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/2.png)


3. 添加三个`repository secret`：

- 在`Name`中填入`username`，在`Value`中填入你的账号，点击`Add secret`；
- 回到刚刚的界面，点击`New repository secret`，在`Name`中填入`password`，在`Value`中填入你的密码，再点击`Add secret`；
- 再回到刚刚的界面，点击`New repository secret`，在`Name`中填入`distance`，在`Value`中填入你想要跑的里程，再点击`Add secret`。
- 继续回到刚刚的页面，点击`New repository secret`，在`Name`中填入`TargetActivities`， 在`Value`中填入你需要参加活动的关键字（可以汉字）, 再点击`Add secret`。
 ![3](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/3.png)
  ![4](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/4.png)
  ![5](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/5.png)
  ![6](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/6.png)


4. 完成后，进入`Actions`界面。工作流默认会自动开启。你也可以手动执行工作流，以防止自动数据上传失效。
 ![7](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/7.png)




## 免责声明

- 本项目仅供学习参考之用，请勿用于违法用途，本项目及其作者不承担相应责任。

- 作者不需要使用乐健体育APP，纯属为爱码代码。

- 项目可能失效，随缘更新，欢迎大佬们PR。

- 如造成作者及其代码提供者损害，作者有权关闭此项目仓库。
