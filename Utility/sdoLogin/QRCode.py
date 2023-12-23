import requests, time, qrcode, json, os, configparser
from pyzbar.pyzbar import decode
from PIL import Image
from datetime import datetime

header = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

timestamp = lambda: int(round(time.time() * 1000))

skey = None
ticket_cookie = None
ticket = None
authCookie = None
params_cookie = None
cookie_combine = None

deBug = 'False'
initialization = 'False'
cookieSaved = 'False'


def json_handel(self):
    return self.replace('\\', '').replace('"{', "{").replace('}"', "}").replace('codeKeyLogin_JSONPMethod(',
                                                                                "").replace(')', '')


def get_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


# 处理QrCode
def qrcode_get(appId,areaId):
    global skey, barcode_url
    # 获取二维码缓存到本地
    qrcode_url = "https://w.cas.sdo.com/authen/getcodekey.jsonp?&appId=" + str(appId) + "&areaId=" + str(areaId) + "/getcodekey.png"
    res = requests.get(qrcode_url, headers=header, verify=False)
    skey_cookie = res.cookies
    with open(f"{get_path()}/temp/qrcode.png", 'wb') as f:
        f.write(res.content)
        f.close()

    # 使用pyzbar解析缓存的二维码图片
    barcodes = decode(Image.open(f"{get_path()}/temp/qrcode.png"))
    for barcode in barcodes:
        barcode_url = barcode.data.decode("utf-8")

    # 使用qrcode生成二维码到终端
    qr = qrcode.QRCode()
    qr.add_data(barcode_url)
    qr.print_ascii(invert=True)

    # 将二维码携带的skey传递给登录阶段
    if barcode_url is not None:
        skey = skey_cookie
        print(f'[{get_current_time()}]获取登录二维码成功,请尽快使用叨鱼扫描')
    else:
        print(f'[{get_current_time()}]获取登录验证码失败,请反馈给开发者')


# 进行登录
def qrcode_check(appId, areaId, serviceUrl):
    show_qrcode = False
    global skey
    global ticket_cookie
    global ticket

    # 检查skey
    if skey is not None:

        url = ("https://w.cas.sdo.com/authen/codeKeyLogin.jsonp?callback=codeKeyLogin_JSONPMethod&appId="
               + str(appId)
               + "&areaId="
               + str(areaId)
               + "&code=300&serviceUrl="
               + serviceUrl
               + f"&productId=2&productVersion=3.1.0&authenSource=2&_={timestamp}")

        # 进入二维码扫描判断
        while True:

            res = requests.get(url, headers=header, timeout=30, cookies=skey)
            s = requests.session()
            s.keep_alive = False

            # 替换Json中无效字符
            response = json_handel(res.text)
            obj = json.loads(response)
            return_code = obj["return_code"]

            # 是否已经展示二维码
            if not show_qrcode:
                show_qrcode = True
                print(f'[{get_current_time()}]' + '请速速打开叨鱼APP扫描二维码,不然我就哭给你看!')

            # 判断是否扫码 并将携带ticket的cookie传递
            if return_code != -10515805:
                ticket_cookie = res.cookies
                ticket = obj["data"]["ticket"]
                print(
                    f'[{get_current_time()}]' + f'侦测到你拿起了手机,现在请放下手机并耐心等待.[你问我怎么知道你拿起了手机?]')
                return ticket
    else:
        print(f'[{get_current_time()}]' + '扫码失败,请检查网络连接或者尝试拍打一下电脑.')


def login(appId, areaId, serviceUrl):
    """
    :param appId: 应用ID
    :param areaId: 区域ID
    :param serviceUrl: 服务地址
    :return: 盛趣登录的Cookie，格式：json
    """
    qrcode_get(appId, areaId)
    ticket_cookie = qrcode_check(appId, areaId, serviceUrl)
    return ticket_cookie
