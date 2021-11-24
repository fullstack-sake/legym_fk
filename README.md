## 注意：这是一个待修复的项目



# 乐健体育模拟跑步的分析
## 项目介绍

- 本项目仅适用于**乐健体育**
- 工作流将自动在每日的**10:00**左右自动上传跑步数据（才跑1.8公里的菜鸡，后续加入更多里程）
- 对代码改进有任何好的建议，欢迎提`Issues`，或者直接`PR`
- 如果对您有帮助，请顺手点个`Star`吧

------

## 模拟跑步原理

目前发现有6个站点；向它们`get`或`post`不同的字典字符串json，就可以相当于完成相应工作。


### 站点1：Login
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

### 站点2：getTotalRunning

**获取`totalMileage`**，不清楚有什么用

### 站点3：getCurrent

**获取跑步任务开始期和结束期**

并注意到返回了`organizationId`，不清楚有什么用

------

### 站点4：getRunningRange

`headers`中需提供`Authorization`和`Organization`，而`organization`可以通过`getCurrent`获取

采用`post`方法，`body`如下
```python
{ 	"latitude": 纬度, 
 	"longitude": 经度, 
 ..."scoringType": 跑步模式, ... }
```

------

### 站点5：getRunningLimit

`body`要提供`semesterId`

------

### 站点6：uploadRunningDetails

`headers`中需提供`Authorization`，采用了`Bearer<token>`，可以通过登录的`response`的`accesstoken`获取

采用`post`方法，`body`结构为

```python
{ "avePace": 配速, "calorie": 卡路里, "effectiveMileage": 有效里程, "effectivePart": 1, "endTime": 提交时间, ... "paceNumber": 998, "paceRange": 0, "routineLine": [{ "latitude": 纬度, "longitude": 经度 },...], "scoringType": 1, "semesterId": "402881ea7c39c5d5017c39d1ffd306a0", "signPoint": [], "startTime": 开始时间, "totalMileage": 总里程, "totalPart": 0.0, "type": 跑步模式, "uneffectiveReason": "" }
```

------

## 使用方法

部署Action自动跑步数据上传

1. 将本仓库`Fork`到自己的仓库里；

 ![1](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/1.png)

2. 点击`Settings`→`Secrets`→`New repository secret`。

 ![2](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/2.png)

3. 在`Name`中填入`username`，在`Value`中填入你的账号，再点击`Add secret`；再回到刚刚的界面，点击`New repository secret`，在`Name`中填入`password`，在`Value`中填入你的密码，再点击`Add secret`。

 ![3](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/3.png)

 ![4](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/4.png)

 ![5](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/5.png)
4. 完成后，进入`Actions`界面。工作流默认会自动开启。你也可以手动执行工作流，以防止自动数据上传失效。
 ![6](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/6.png)

 


## 免责声明

- 本项目仅供学习参考之用，请勿用于违法用途，本项目及其作者不承担相应责任。

- 作者不需要使用乐健体育APP，纯属为爱码代码。

- 项目可能失效，随缘更新，欢迎大佬们PR。

- 如造成作者及其代码提供者损害，作者有权关闭此项目仓库。