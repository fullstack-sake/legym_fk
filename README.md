## 注意：这是一个还未完工的项目



# 乐健体育模拟跑步的分析

## 原理

该功能目前发现有6个站点；向它们`get`或`post`不同的字典字符串，就可以相当于完成手动点击的任何操作；

---

## 站点1：Login

**为用户提供登录服务**

`headers`中需要提供`content-type`和`connection`。

```python
headers = {	
    		"content-type":"application/json",
            "connection":"Keep-Alive"}
```

采用`post`方法，`body`如下：

```python
body = {"entrance":"1","password":"password","userName":"18888888888"}
```

------

## 站点2：getTotalRunning

**获取`totalMileage`**

------

## 站点3：getCurrent

**获取跑步任务开始期和结束期**

并注意到返回了`organizationId`

------

## 站点4：getRunningRange

`headers`中需提供`Authorization`和`Organization`，而`organization`可以通过`getCurrent`获取

采用`post`方法，`body`如下
```python
{ 	"latitude": 纬度, 
 	"longitude": 经度, 
 ..."scoringType": 跑步模式, ... }
```

------

## 站点5：getRunningLimit

`body`要提供`semesterId`，现阶段还未搞到

------

## 站点6：uploadRunningDetails

`headers`中需提供`Authorization`，采用了`Bearer<token>`，并未找到有效方法获取，只能通过抓包

采用`post`方法，`body`结构为

```python
{ "avePace": 配速, "calorie": 卡路里, "effectiveMileage": 有效里程, "effectivePart": 1, "endTime": 提交时间, ... "paceNumber": 998, "paceRange": 0, "routineLine": [{ "latitude": 纬度, "longitude": 经度 },...], "scoringType": 1, "semesterId": "402881ea7c39c5d5017c39d1ffd306a0", "signPoint": [], "startTime": 开始时间, "totalMileage": 总里程, "totalPart": 0.0, "type": 跑步模式, "uneffectiveReason": "" }
```

