import requests


def ocr_cjy(host, username, password, soft_id, codetype,img):
    """
    :param host: 超级鹰的解析APi
    :param username: 用户名
    :param password: 密码
    :param soft_id: 软件ID
    :param codetype: 验证码类型
    :return: 解析成功会返回验证码，失败会返回服务器的错误信息
    """
    ocr_params = {
        'user': username,
        'pass': password,
        'softid': soft_id,
        'codetype': codetype,
        'len_min': 6
    }
    ocr_header = {
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
    }
    files = {'userfile': ('Captcha.jpeg', img)}
    ocr_resp = requests.post(host, data=ocr_params, headers=ocr_header, files=files, verify=False)
    code_json = ocr_resp.json()
    code = code_json['pic_str']
    errmsg = code_json['err_str']
    if errmsg != 'OK':
        return ocr_resp.text
    else:
        return code
