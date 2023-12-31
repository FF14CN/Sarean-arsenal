import configparser
import importlib

'''
example:
import Utility.Notifications.push as pusher
print(pusher.push('test', 'test'))
'''

def push(title, content):
    """
    Push推送
    :param title: 通知标题
    :param content: 通知内容
    :return: 推送结果，如：{'status': 'success'} 或 {'status': 'failed', 'error': 'error message'}
    """

    push_config = configparser.ConfigParser()
    push_config.read('config.ini', encoding='UTF-8')
    # 根据配置导入对应的包
    push_module = importlib.import_module("Utility.Notifications." + push_config.get('Notification', 'push-method'))
    result = push_module.send(title, content)
    return result
