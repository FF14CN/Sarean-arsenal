# 用于直接执行任务的脚本
import configparser

from Utility.sqMall import sqMallDoSign as sqMallSign
from Utility.risingStones.dailytask import daily_task as lets_go

taskConfig = configparser.RawConfigParser()
taskConfig.read('config.ini', encoding='utf-8')
if taskConfig.get('Modules', 'sqMallTask') == 'True':
    sqMallSign.main()

if taskConfig.get('Modules', 'risingStonesTask') == 'True':
    print(lets_go())