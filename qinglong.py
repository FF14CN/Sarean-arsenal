# 用于青龙面板的任务
# 青龙面板需要满足以下条件：
# docker镜像必须使用【whyour/qinglong:debian】，否则依赖无法安装。
# 请安装【requirement.txt】内的Python依赖
# 请安装【zbar-tools】linux依赖
# 请确保已经填写好【config.ini】配置文件，此任务将不会引导您填写配置文件。
import configparser

from Utility.sqMall import sqMallDoSign as sqMallSign
from Utility.risingStones.dailyTask import daily_task as lets_go

taskConfig = configparser.RawConfigParser()
taskConfig.read('config.ini', encoding='utf-8')
if taskConfig.get('Modules', 'sqMallTask') == 'True':
    sqMallSign.main()

if taskConfig.get('Modules', 'risingStonesTask') == 'True':
    noc_config = configparser.RawConfigParser()
    noc_config.read('config.ini', encoding='utf-8')
    if noc_config.get('Notification', 'noc-enable') == 'True':
        import Utility.Notifications.push as pusher
        msg = lets_go()
        pusher.push('石之家任务结果', msg)
    else:
        import Utility.Notifications.push as pusher
        msg = lets_go()
        pusher.push('石之家任务结果', msg)