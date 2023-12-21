# 推送组件

**本组件仅为以下服务商提供调用方法，不存在任何利益关系。**  
**若与服务商产生经济纠纷请与服务商协商解决。**

目前已支持：
- [X] [Bark (仅供iOS)](https://bark.day.app/#/)
- [X] [PushDeer (多平台)](https://www.pushdeer.com/)
- [X] [ServerChan (多平台)](https://sct.ftqq.com/)
- [X] SMTP邮件 (多平台)


# 使用方法

## 用户教程
请在项目 `config.ini` 文件内填写好以下内容：
```ini
[Notification]
;若要启用消息通知，请将noc-enable设置为True,并根据说明正确配置push-key
noc-enable = False
;通知服务商可选：bark、pushdeer serverchan smtp
push-method = bark
;推送密钥或目标地址
push-key = xxxxx

;SMTP 发件服务器配置
;目前仅支持SSL 465端口发送
; TODO: 支持非SSL
smtp-host = ""
smtp-port = 465
smtp-username = ""
smtp-password = ""
smtp-ssl = True
```

### 获取push-key
#### Bark
[![1703144086065.webp](https://infrasimage-r2.cf.cdn.infras.host/2023/12/21/6583ea8deed28.webp)](https://infrasimage-r2.cf.cdn.infras.host/2023/12/21/6583ea8deed28.webp)

#### PushDeer
1. 通过apple账号（或微信账号·仅Android版支持）登录
2. 切换到「设备」标签页，点击右上角的加号，注册当前设备
3. 切换到「Key」标签页，点击右上角的加号，创建一个Key
4. 将Key填入配置文件

#### ServerChan
[![1703144461590.webp](https://infrasimage-r2.cf.cdn.infras.host/2023/12/21/6583ec04d0242.webp)](https://infrasimage-r2.cf.cdn.infras.host/2023/12/21/6583ec04d0242.webp)

#### SMTP邮件
请自行Google/百度：“QQ邮箱SMTP发件教程” “XX邮箱SMTP教程”

## 调用教程
此章节内容仅供开发者使用，普通用户无需关注此部分内容。

导入`push.sh`：
```python
import Utility.Notifications.push as pusher
pusher.push('title标题', 'content内容')
```