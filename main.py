import Daoyu
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def work_work():
    if Daoyu.initialize():
        phone_number, device_id, manuid, daoyu_key_init, main_key, sms_enable, show_username = (
            Daoyu.config_handler()[1], Daoyu.config_handler()[7], Daoyu.config_handler()[8], Daoyu.config_handler()[9],
            Daoyu.config_handler()[10], Daoyu.config_handler()[11], Daoyu.config_handler()[12])
        if main_key == '' and show_username == '' and sms_enable == '0' and daoyu_key_init == '1':
            confirm = input("你选择了短信登录，请注意，你其他设备的叨鱼APP将掉线，请输入Y确认或N退出：")
            if confirm != 'Y':
                exit()
            guid, scene = Daoyu.get_guid(device_id, manuid)
            main_key, show_username = Daoyu.get_main_key(manuid, device_id, guid, phone_number, scene)
        elif main_key == '' and show_username == '' and sms_enable == '1':
            Daoyu.logger_stream.info('检测到你把短信登录关闭了, 而且还没有设置我要用的东西，你在搞我，爷不干了')
            exit()
        elif main_key != '' and show_username != '':
            Daoyu.logger_stream.info('读取到了你手动设置的DaoyuKey和ShowUserName')
        elif main_key != '' and show_username != '':
            Daoyu.logger_stream.info('DaoyuKey 或者 showUsername 为空 看Github上的教程 求求你辣')
            exit()
        else:
            Daoyu.logger_stream.info('ini有问题... 发个issue看看！')
            exit()
        flowid = Daoyu.get_flowid(manuid, device_id, main_key, show_username)
        account_id_list = Daoyu.get_account_id_list(flowid, device_id, manuid, main_key, show_username)
        temp_account_sessionid = Daoyu.get_temp_sessionid(main_key)
        if account_id_list is not None:
            for index, account_id in enumerate(account_id_list):
                if Daoyu.make_confirm(account_id["accountId"], flowid, device_id, manuid, main_key, show_username):
                    sub_account_key = Daoyu.get_sub_account_key(flowid, manuid, device_id, main_key, show_username)
                    sub_account_session = Daoyu.get_sub_account_session(sub_account_key, temp_account_sessionid)
                    sign_msg = Daoyu.do_sign(sub_account_session, account_id["accountId"])
                    if sign_msg == 0:
                        Daoyu.logger_stream.info(
                            f'账号{account_id["displayName"]}签到成功，当前积分余额{Daoyu.get_balance(sub_account_session)}')
                        if index + 1 < len(account_id_list):
                            flowid = Daoyu.get_flowid(manuid, device_id, main_key, show_username)
                    elif sign_msg == 1:
                        Daoyu.logger_stream.info(
                            f'账号{account_id["displayName"]}已经签到过了，当前积分余额{Daoyu.get_balance(sub_account_session)}')
                        if index + 1 < len(account_id_list):
                            flowid = Daoyu.get_flowid(manuid, device_id, main_key, show_username)
                    else:
                        Daoyu.logger_stream.info(f'账号{account_id["displayName"]}签到失败)')
                        if index + 1 < len(account_id_list):
                            flowid = Daoyu.get_flowid(manuid, device_id, main_key, show_username)
                else:
                    Daoyu.logger_stream.info(f'账号{account_id["displayName"]}与服务器握手失败')

        else:
            Daoyu.logger_stream.info('没有发现你的账户，请检查logs文件')


if __name__ == '__main__':
    # 创建一个调度器
    scheduler = BlockingScheduler()

    # 添加任务到调度器，立即执行一次，然后每天的 21 点执行一次
    scheduler.add_job(work_work, 'cron', hour=21, minute=0, second=0, next_run_time=datetime.now())

    # 启动调度器
    scheduler.start()
