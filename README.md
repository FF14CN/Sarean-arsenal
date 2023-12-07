# FF14 AutoSignRemake

## 使用说明

1. 下载 [Releases](https://github.com/KuLiPoi/FF14AutoSign/releases) 中已打包好的最新版文件
2. 进入项目根目录
3. 安装依赖库 ```pip -r requirements.txt```
4. 运行本项目 ```python .\main.py```

## 注意事项

一般情况下无需修改根目录下的设置文件

如果出现报错请开启 ```DebugMode```并将```LogsLevel```调整至 ```High```并心中默念「给我日志给我日志」然后再次执行程序将程序根目录出现的新东西发送到issue.

**没有logs文件无异于闭眼开车，没有日志或合理错误说明的Issue将被直接关闭！**

## TodoList

- [ ] 支持消息推送
  - [X] 已支持：Bark、Pushdeer、Severchan
  - [ ] 计划中：
- [ ] 支持账号密码和一键登录
- [ ] 支持青龙面板

## 感谢

[@renchangjiu](https://github.com/renchangjiu/FF14AutoSignIn) **提供的核心思路**

## License

[With AFL - 3.0](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE)  
[Pineapple LICENSE](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE.txt) 
