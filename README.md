# FF14 AutoSignRemake

## 重要说明
**本项目基于手机叨鱼运行，可能在使用过程中会涉及一些敏感参数**    
**目前仅发布于作者个人博客和Github,请注意项目来源。**  
**项目完全开源，以至于你可以完全阅读作者的每一行写的很屎的代码，但是可以确保你的账号安全**  
**没有logs无异于闭眼开车，Logs中的敏感信息已剔除，没有日志或合理错误说明的Issue将被直接关闭！**  
**请仔细阅读教程，教程中说过的再问，可能会获得一个很不好的结果（指直接关闭Issue）**
[![c4765f39e308ddf41f74890d36f54d39.webp](https://infrasimage-r2.cf.cdn.infras.host/2023/12/22/65854fa135d83.webp)](https://infrasimage-r2.cf.cdn.infras.host/2023/12/22/65854fa135d83.webp)

**程序也支持短信登录，但是会造成你其他平台的叨鱼APP掉线，我本人并不推荐，**  
**我教程中所用的方法是使用你的当前登录已经登录叨鱼的平台参数，应该对你已经登陆的设备没有影响，**  
**如果发现你的设备掉线了，请马上告诉我我！默认每日签到时间为每日21点，建议按照下面的教程配置消息推送**
## 使用教程
1. 下载 [Releases](https://github.com/KuLiPoi/FF14AutoSign/releases) 中已打包好的最新版文件
2. 进入项目根目录
3. 安装依赖库 ```pip -r requirements.txt```
4. 打开抓包软件 抓取必须的重要参数
    1. IOS端  
       1. 从Appstore下载Stream软件，免费的
       2. 打开叨鱼退出登录，退出叨鱼，打开Stream，启动抓包，打开叨鱼
    2. 安卓端  
       由于安卓阵营错综复杂每个品牌的情况各不相同，还劳烦各位自行搜索自己手机的抓包方案，  
       据我所知ROOT/非ROOT下均可抓包，可能后面会出个详细教程，看我心情。
    3. 找到```https://daoyu.sdo.com/api/userCommon/validateSmsCodeLogin```  
       ```
       *参数附带的值均为举例，你要找到你自己的*
       *我的安卓环境是MuMu模拟器，可能你的手机参数和我差别很大 无需惊恐*
       *苹果环境下应该和我的参数是差不多的，你的和我的差很多就是找错了*
       *show_username 本身就是默认隐藏中间四位的按照原样赋值即可*
       *USERSESSID 对应Config.ini中的DaoyuKey*
       在IOS下 Device_id: 8UYD77F-C2F3-98U7-098N-9I8J9876287Y
       在IOS下 device_manuid: iPhone10,5 
       在Android下 Device_id: -0b9dcd11634aa634 
       在Android下 device_manuid: 2206122SC
       通用：
       show_username: 138****1234 
       USERSESSID: DY_123U823R45FGH52123FR123F312312123VVE1234VOP098
       ```
5. 将上述参数保存到```config.ini```中，上述没提到的参数**无需改动**。
6. 如需启用消息推送，请参考[如何开启消息推送](https://github.com/KuLiPoi/FF14AutoSign/tree/main/Utility/Notifications)进行设置。
7. 运行本项目 ```python .\main.py```

## Q&A
1. 问：我找不到我的那些参数怎么办？  
答：不可能，模拟器上都能找到，除非你的手机是非智能机（？）
2. 问：作者的代码为什么看起来像大便？  
答：我现学现卖，非专业出身，你觉得你的代码水平好，那么，欢迎重构！
3. 问：我不会抓包怎么办？  
答：本项目已经成功和百度达成合作关系，今后大家有什么不懂的可以直接问百度啦！
4. 问：程序莫名其妙报了一大堆错误我看不懂怎么办啦！  
答：这是我的锅，麻烦你带着LOGS发送到ISSUE.
5. 问：你这程序会不会盗我的游戏账号？  
答：哥们儿，全是开源的东西，你看嘛，眼睛不需要就捐了。
6. 问：能否支持xx功能？
答：可以发ISSUE，觉得可行，不麻烦，后续会加上的。
7. 问：配置文件中其他参数什么意思？
答：呃，我没说的可以不用管。

## TodoList
项目开发计划与进度请移步至 [Dev Status](https://github.com/users/KuLiPoi/projects/2) 查看。

## 感谢

[@renchangjiu](https://github.com/renchangjiu/FF14AutoSignIn) **提供的核心思路**

## License

[With AFL - 3.0](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE)  
[Pineapple LICENSE](https://github.com/AmarokIce/PineappleDelight/blob/master/LICENSE.txt) 
