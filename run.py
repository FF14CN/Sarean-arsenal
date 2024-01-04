# 用于直接执行任务的脚本
import configparser

from Utility.sqMall import sqMallDoSign as sqMallSign
from Utility.risingStones import signIn as rs_signin
from Utility.risingStones import rs_login
from Utility.risingStones import getSignReward as getSignReward
from Utility.risingStones.rs_login import is_rs_login as rs_userInfo

taskConfig = configparser.RawConfigParser()
taskConfig.read('config.ini', encoding='utf-8')
if taskConfig.get('Modules', 'sqMallTask') == 'True':
    sqMallSign.main()

if taskConfig.get('Modules', 'risingStonesTask') == 'True':
    rs_cookies = rs_login.login()
    rs_result = rs_signin.rs_signin(rs_cookies)
    rs_reward = getSignReward.getReward(rs_cookies)
    userInfo = rs_userInfo(rs_cookies)["msg"]
    accountinfo = "当前登录账户:" + userInfo["character_name"] + "@" + userInfo["group_name"]
    print('石之家任务结果', accountinfo + '\n' + str(rs_result) + '\n' + str(rs_reward))
