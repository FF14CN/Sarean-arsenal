# FF14 AutoSignRemake

## 重要说明
**本项目基于手机叨鱼运行，可能在使用过程中会涉及一些敏感参数**    
**目前仅发布于作者个人博客和Github,请注意项目来源。**  
**项目完全开源，以至于你可以完全阅读作者的每一行写的很屎的代码，但是可以确保你的账号安全**  
**没有logs无异于闭眼开车，Logs中的敏感信息已剔除，没有日志或合理错误说明的Issue将被直接关闭！**  
**请仔细阅读教程，教程中说过的再问，可能会获得一个很不好的结果（指直接关闭Issue）**
## 使用教程
1. 下载 [Releases](https://github.com/KuLiPoi/FF14AutoSign/releases) 中已打包好的最新版文件
2. 进入项目根目录
3. 安装依赖库 ```pip -r requirements.txt```
4. 打开抓包软件 抓取必须的重要参数
    1. IOS端  
       1. 从Appstore下载Stream软件，免费的
       2. 打开叨鱼退出登录，退出叨鱼，打开Stream，启动抓包，打开叨鱼
    2. 安卓端  
       由于安卓阵营错综复杂每个品牌对于ROOT非ROOT抓包的方案各不相同，还劳烦各位自行搜索自己手机的方案，
    3. 找到```https://daoyu.sdo.com/api/userCommon/validateSmsCodeLogin```  
       ```
       *参数附带的值均为举例，你要找到你自己的*
       Device_id: 8UYD77F-C2F3-98U7-098N-9I8J9876287Y / 在参数里面找
       device_manuid: iPhone10,5 / 在参数里面找
       show_username: 138****1234 / 在返回值里面找 本身就是带打码的 不必惊恐
       USERSESSID: DY_123U823R45FGH52123FR123F312312123VVE1234VOP098 / 对应设置文件的 DaoyuKey
       ```
5. 按照下面设置```config.ini```并保存。
    ```
   deviceid = 上面你找到的
   manuid = 上面你找到的
   phonenumber = 你登录叨鱼的手机号
   smsloginenable = 1
   daoyukeyinit = 0
   daoyukey = 上面你找到的
   showusername = 上面你找到的
   ```
6. 运行本项目 ```python .\main.py```

## TodoList

- [ ] 支持消息推送
  - [X] 已支持：Bark、Pushdeer、Severchan
  - [ ] 计划中：

- [ ] 支持青龙面板

## 感谢

[@renchangjiu](https://github.com/renchangjiu/FF14AutoSignIn) **提供的核心思路**

## License

[With AFL - 3.0](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE)  
[Pineapple LICENSE](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE.txt) 
