# 乐健体育自动化

> 作者：[sake](https://github.com/fullstack-sake), [MrCai](https://github.com/MrCaiDev)
>
> legym 模块本体：[MrCaiDev/legym](https://github.com/MrCaiDev/legym)

## 项目介绍

乐健体育 app 的**每日自动活动签到与跑步数据上传**。

- 实现原理见：[模拟跑步与活动签到原理](https://github.com/MrCaiDev/legym-automation/blob/main/doc/theory.md)
- 对代码改进有任何好的建议，欢迎提 Issues，或者直接 PR，感谢:handshake::heart:！
- 如果对您有帮助，请顺手点个 Star 吧！

## 部署教程

### 本地私有化部署

    git clone https://github.com/fullstack-sake/legym-automation.git
    pip install -i https://test.pypi.org/simple legym==0.4
    python main.py 你的账号#你的密码#要上传的跑步里程#要报名的活动名称

### GitHub Action 自动化部署

1. Fork 本仓库；

![1](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/1.png)

1. 点击 Settings → Secrets → New repository secret。

![2](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/2.png)

1. 添加 secret 的方法：在 Name 栏中填入 secret 名称，在 Value 栏中填入 secret 值。本项目需要 4 个 secret：

|   Name   |      Value       |
| :------: | :--------------: |
| username |     你的账号     |
| password |     你的密码     |
| distance | 要上传的跑步里程 |
| activity | 要报名的活动名称 |

![3](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/3.png)
![4](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/4.png)
![5](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/5.png)
![6](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/6.png)
![10](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/10.png)

4. 完成后，进入 Actions 界面。被 Fork 的仓库工作流默认不启用，需要将其手动开启（仅首次需要）。你也可以手动执行工作流，并检查 build 过程是否按预期进行。

![7](https://raw.githubusercontent.com/fullstack-sake/legym_fk/main/images/7.png)

## 免责声明

- 本项目仅供学习参考之用，请勿用于商业或违法用途；使用该代码的责任由部署者自行承担。
- 项目可能失效，随缘更新，欢迎大佬们 PR。
- 如造成作者及其代码提供者损害，作者有权关闭此项目仓库。
