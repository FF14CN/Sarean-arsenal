import Daoyu


def main():
    if Daoyu.initialize():
        phone_number, device_id, manuid = Daoyu.config_handler()[1], Daoyu.config_handler()[7], Daoyu.config_handler()[
            8]
        guid, scene = Daoyu.get_guid(device_id, manuid)
        main_key, show_username = Daoyu.get_main_key(manuid, device_id, guid, phone_number, scene)
        account_id_list = Daoyu.get_account_id_list(manuid, device_id, main_key, show_username)
        temp_account_sessionid = Daoyu.get_temp_sessionid(main_key)
        if account_id_list is not None:
            Daoyu.logger_stream.info(f'已经发现你的账户存在{len(account_id_list)}个账号，将为你依次执行...')
            for account_id in account_id_list:
                flowid = Daoyu.get_flowid(account_id, manuid)
                if Daoyu.make_confirm(account_id["accountId"], flowid, device_id, manuid, guid, show_username):
                    sub_account_key = Daoyu.get_sub_account_key(flowid, manuid, device_id)
                    sub_account_session = Daoyu.get_sub_account_session(sub_account_key, temp_account_sessionid)
                    if Daoyu.do_sign(sub_account_session):
                        Daoyu.logger_stream.info(
                            f'账号{account_id["displayName"]}签到成功，当前积分余额{Daoyu.get_balance(sub_account_session)}')
                    else:
                        Daoyu.logger_stream.info(f'账号{account_id["displayName"]}签到失败)')
                else:
                    Daoyu.logger_stream.info(f'账号{account_id["displayName"]}与服务器握手失败')

        else:
            Daoyu.logger_stream.info('没有发现你的账户，请检查logs文件')


if __name__ == '__main__':
    main()
