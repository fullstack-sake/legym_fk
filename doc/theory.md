# 模拟跑步与活动签到原理

先用 frida 配合此项目仓库的 sake.js 来 **hook** 证书验证，干掉乐健体育的 `ssl pinning`，然后进行 packetcapture。通过分析数据报文，向相应站点 `get` 或 `post` 不同的数据进行 forward packet，就可以实现乐健体育的无头模拟。

## 站点1：Login

 **为用户提供登录服务**

采用`post`方法，`body`如下：

```python
body = {"entrance":"1","password":"password","userName":"18888888888"}
```

返还的`response`可以获取到很多关键数据：`accessToken`，`organizationId`

## 站点2：getCurrent

采用`get`方法，这里返还的`response`我们只需要`semesterId`

## 站点3：getRunningLimit

`body`要提供`getCurrent`获取的`semesterId`，这里返还的`response`我们只需要`limitationsGoalsSexInfoId`

## 站点4：uploadRunningDetails

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

## 站点5：getActivityList

**获取课外活动列表**

采用`post`方法，这里返还的`response`我们只需要`ActivityId`

## 站点6：signUpActivity

**活动报名**

可以报名未开始的活动，服务端不验证报名是否开始。

采用`post`方法，要提供`getActivityList`获取的`ActivityId`

## 站点7：signInActivity

**活动签到**

进行活动的签到，活动签到不需要位置信息，位置信息仅在客户端验证

采用`post`方法，要提供`getActivityList`获取的`ActivityId`