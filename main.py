import requests,time,qrcode,json,os,configparser
from pyzbar.pyzbar import decode
from PIL import Image
from datetime import datetime
from http.cookiejar import MozillaCookieJar



header = {'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

class Pipirapira(object):

    session = requests.session()
    
    skey = None
    ticket_cookie = None
    ticket = None
    authCookie = None
    params_cookie = None
    cookie_combine = None
    
    deBug = 'False'
    initialization = 'False'
    cookieSaved = 'False'

    def __init__(self) -> None:
        pass
    
    def jsonHandel(json_temp):
        return json_temp.replace('\\','').replace('"{',"{").replace('}"',"}").replace('codeKeyLogin_JSONPMethod(',"").replace(')','')
    
    def getPath():
        return os.path.dirname(os.path.abspath(__file__))
    
    # TimeStamp
    def timestamp():
        return int(round(time.time() * 1000))
    def getCurrentTime():
        return datetime.now().strftime("%H:%M:%S")
    
    def initialization():
        
        global deBug
        global initialization
        global cookieSaved
        
        config = configparser.ConfigParser()
        config.read(f'{Pipirapira.getPath()}/config.ini')
        
        deBug = config.get('Develop','DebugMode')
        initialization = config.get('Normal','initialization')
        cookieSaved = config.get('Normal','CookieSaved')
        
        if initialization == 'False':
            print(f'[{Pipirapira.getCurrentTime()}]尚未进行初始化,正在从云端初始化配置文件')
            try:
                r = requests.get('http://pipirapira.com/config/config.ini')
                r.raise_for_status()
                with open (f'{Pipirapira.getPath()}/config.ini','wb') as f:
                    f.write(r.content)
                    f.close
                initialization = 'True'
                print(f'[{Pipirapira.getCurrentTime()}]初始化成功,第一次使用请先扫码登录.')
                    
            except requests.exceptions as err:
                print(f'[{Pipirapira.getCurrentTime()}]初始化失败,请检查网络连接')
        else:                 
            print(f'[{Pipirapira.getCurrentTime()}]检测到初始化已经执行,正在尝试获取已保存Cookie.')
    
    # 处理QrCode    
    def qrCodeGet(self):
        global skey
        
        # 获取二维码缓存到本地
        qrcodeUrl = 'https://w.cas.sdo.com/authen/getcodekey.jsonp?&appId=6666&areaId=-1/getcodekey.png'
        res = requests.get(qrcodeUrl,headers=header,verify=False)
        skey_cookie = res.cookies
        with open(f"{Pipirapira.getPath()}/temp/qrcode.png",'wb') as f:
            f.write(res.content)
            f.close
            
        # 使用pyzbar解析缓存的二维码图片
        barcodes = decode(Image.open(f"{Pipirapira.getPath()}/temp/qrcode.png"))
        for barcode in barcodes:
            barcode_url = barcode.data.decode("utf-8")
            
        # 使用qrcode生成二维码到终端
        qr = qrcode.QRCode()
        qr.add_data(barcode_url)
        qr.print_ascii(invert=True)
        
        # 将二维码携带的skey传递给登录阶段
        if barcode_url != None:
            skey = skey_cookie
            print(f'[{Pipirapira.getCurrentTime()}]获取登录二维码成功,请尽快使用叨鱼扫描')
        else:
            print(f'[{Pipirapira.getCurrentTime()}]获取登录验证码失败,请反馈给开发者')
    
    # 进行登录 
    def qrCodeCheck(self):
        showQrCode = False
        global skey
        global ticket_cookie
        global ticket    
        
        # 检查skey
        if skey != None:
            
            url = f"https://w.cas.sdo.com/authen/codeKeyLogin.jsonp?callback=codeKeyLogin_JSONPMethod&appId=6666&areaId=-1&code=300&serviceUrl=https://qu.sdo.com/&productId=2&productVersion=3.1.0&authenSource=2&_={Pipirapira.timestamp()}"
            
            # 进入二维码扫描判断
            while True:
                
                res = requests.get(url,headers=header,timeout=30,cookies=skey)
                
                # 替换Json中无效字符
                response = Pipirapira.jsonHandel(res.text)
                # response = res.text.replace('\\','').replace('"{',"{").replace('}"',"}").replace('codeKeyLogin_JSONPMethod(',"").replace(')','')
                obj = json.loads(response)
                return_code = obj["return_code"]
                
                # 是否已经展示二维码
                if showQrCode == False:
                    showQrCode = True
                    print(f'[{Pipirapira.getCurrentTime()}]'+'请速速打开叨鱼APP扫描二维码,不然我就哭给你看!')
                      
                # 判断是否扫码 并将携带ticket的cookie传递
                if return_code != -10515805:
                    ticket_cookie = res.cookies
                    ticket = obj["data"]["ticket"]
                    print(f'[{Pipirapira.getCurrentTime()}]'+f'侦测到你拿起了手机,现在请放下手机并耐心等待.[你问我怎么知道你拿起了手机?]')
                    break
                
        else:
            print(f'[{Pipirapira.getCurrentTime()}]'+'扫码失败,请检查网络连接或者尝试拍打一下电脑.')
    
    
    # 处理已经获得的Cookie
    def cookieHandel(self):
                
        global ticket_cookie
        global ticket
        global cookie_combine
        
        print(f'[{Pipirapira.getCurrentTime()}]'+f'正在处理你的Cookies...')
        url = f'https://sqmallservice.u.sdo.com/api/us/login?ticket={ticket}&_={Pipirapira.timestamp()}'
        res = requests.get(url,headers=header,cookies=ticket_cookie)
        callback_cookie = res.cookies

        # CookieJar -> Dict
        TicketCookieJarToDict = requests.utils.dict_from_cookiejar(ticket_cookie)
        callBackCookieJarToDict = requests.utils.dict_from_cookiejar(callback_cookie)
        
        cookiecombineDict = dict(list(TicketCookieJarToDict.items()) + list(callBackCookieJarToDict.items()))
        cookie_combine = requests.utils.cookiejar_from_dict(cookiecombineDict, cookiejar=None, overwrite=True)
        print(f'[{Pipirapira.getCurrentTime()}]'+f'成功处理了你的Cookie.')
        
    def doSign(self):
        global ticket
        global cookie_combine
        
        print(f'[{Pipirapira.getCurrentTime()}]'+f'开始执行签到操作...')
        
        url = 'https://sqmallservice.u.sdo.com/api/us/integration/checkIn'  
        data_put = {'merchantId':1}
        headers_put = {
            'authority':'sqmallservice.u.sdo.com',
            'method':'PUT',
            'path':'/api/us/integration/checkIn',
            'scheme':'https',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'https://qu.sdo.com',
            'Qu-Web-Host':'qu.sdo.com',
            'Referer':'https://qu.sdo.com/',
            'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',            
            }
        
        # 发起签到请求
        
        res_Dosign = requests.put(url,headers=headers_put,cookies=cookie_combine,data=data_put)
        dosign_response = Pipirapira.jsonHandel(res_Dosign.text)
        resultMsg = json.loads(dosign_response)["resultMsg"]
        
        headers_get = {
            'authority':'sqmallservice.u.sdo.com',
            'method':'GET',
            'scheme':'https',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Origin':'https://qu.sdo.com',
            'Qu-Web-Host':'qu.sdo.com',
            'Referer':'https://qu.sdo.com/',
            'Sec-Ch-Ua':'"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'empty',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',            
            }

        # 查询总积分
        url_Balance = "https://sqmallservice.u.sdo.com/api/rs/member/integral/balance?merchantId=1"
        res_Balance = requests.get(url_Balance,headers=headers_get,cookies=cookie_combine)
        balance_response = Pipirapira.jsonHandel(res_Balance.text)
        balance = json.loads(balance_response)["data"]["balance"]


        if resultMsg == 'SUCCESS':
            acquireIntegration = json.loads(dosign_response)["data"]["acquireIntegration"]
            print(f'[{Pipirapira.getCurrentTime()}]'+ f'签到成功力,本次签到获得的积分为{acquireIntegration}' + f'总积分为{balance}.')
        elif resultMsg == '今日已签到，请勿重复签到':
            print(f'[{Pipirapira.getCurrentTime()}]'+ f'你已经签到过了,你是小猪吗?, 总积分为{balance}.')
        else:
            print(f'[{Pipirapira.getCurrentTime()}]'+ f'发生了终极大错误,重新执行一下,不行反馈给开发者.')
    
        
    def run(self):
        self.qrCodeGet()
        self.qrCodeCheck()
        self.cookieHandel()
        self.doSign()

    

if __name__ == '__main__':
    Pipirapira.initialization()
    # Pipirapira().run()
    


