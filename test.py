import datetime
from DrissionPage import ChromiumPage,ChromiumOptions,WebPage
from DrissionPage._pages.chromium_tab import ChromiumTab
from DrissionPage.common import make_session_ele
import sys
import json
import requests
import re
from concurrent.futures import ThreadPoolExecutor
import threading
import time
lock = threading.Lock()
from threading import Thread

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class PremiumProduct:
    def __init__(self,href):
        #商品名
        self.name = ''
        #店铺名
        self.shop_name = ''
        #商品链接
        self.href = href
        #商品价格
        self.price = 0
        #商品sku
        self.sku = ""
        #商品标题
        self.title = ""
        #商品周销
        self.sale=0
        #商品搜索排名
        self.search=0
        #商品提问
        self.questions=0
        #商品评论
        self.comments=0

        self.page=ChromiumPage()

    def console(self):
        print(f'商品评价数{self.comments}')
        print(f'商品提问{self.questions}')
        print(f'商品标题{self.title}')
        print(f'商品三日销{self.sale}')
        print(f'商品价格{self.price}')
        print(f'商品sku{self.sku}')
        print(f'商品链接{self.href}')

    def search_premium_product(self,page:ChromiumTab,index=0):
        page.wait.ele_loaded('@data-widget:Score')
        pagehtml=make_session_ele(page.html)
        try:
            body = pagehtml.s_ele('t:body')
            self.comments=body('@data-widget:Score').text
            #self.comments=re.search(r'(\d+)',self.comments).group(1)

            self.questions=body('@data-widget=webQuestionCount').text
            #self.questions=re.search(r'(\d+)',self.questions).group(1)
            
            self.title=body('@data-widget=webProductHeading').text

            self.sku = str(re.search(r'.*-(\d+)\/.*',self.href).group(1))

            self.price=body('@data-widget=webPrice').eles('t:span')[0].text

            self.price=re.search(r'(\d+)',self.price.replace(" ","")).group(1)
            
            self.get_premium_stock_sale_gmv()
        except Exception as e: 
            print("商品信息获取失败 "+str(e))
            index+=1
            if index>10:
                print("商品信息获取失败 超过10次")
                with open("error.txt","a",encoding="utf-8") as f:
                    f.write(self.href+"\n")
                page.close()
            else:
                self.search_premium_product(page=page,index=index)
        

    def get_premium_stock_sale_gmv(self):
        with lock:
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "none",
                'cookie':'_ga=GA1.1.982804541.1704363782; _ym_uid=1681391849463919981; _ym_d=1704363784; mindboxDeviceUUID=2a856983-78a1-4c74-94f6-884073bdbc67; directCrm-session=%7B%22deviceGuid%22%3A%222a856983-78a1-4c74-94f6-884073bdbc67%22%7D; _ym_visorc=b; _cmg_cssteig2a=1710228320; _comagic_ideig2a=7998454747.11711166377.1710228319; _ym_isad=1; carrotquest_device_guid=590f66a7-1449-492f-a9e5-af98a1f1d6c8; carrotquest_realtime_services_transport=wss; tmr_lvid=cffdb69e379a7ce80425d3bfd941af10; tmr_lvidTS=1681391853000; carrotquest_closed_part_id=1661953803395533597; userlogin=a%3A2%3A%7Bs%3A3%3A%22lgn%22%3Bs%3A24%3A%22newworldnorth%40yandex.com%22%3Bs%3A3%3A%22pwd%22%3Bs%3A32%3A%22f104d9c9086b387b61ac0c44e68b3931%22%3B%7D; carrotquest_uid=1648369995933026451; carrotquest_auth_token=user.1648369995933026451.57576-5a5343ec7aac68d788dabb2569.e6d60cb30da5a8cc0085a3d7d8dfbb037a646c49608cfea6; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3MTAyMzE5ODAsImlhdCI6MTcxMDIyODM4MCwianRpIjoiYTk5NzMyMDc0NGFmNDZjNTgyZDYwYjhhMmNjYzUzYjAiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTcxMDIyODM4MCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjU3NTc2LiR1c2VyX2lkOjE2NjE5NTM3MTA5Njk4NTAwNTEiLCJ1c2VyLiRhcHBfaWQ6NTc1NzYuJHVzZXJfaWQ6MTY0ODI0MDgyMTQ2MTMyMjczMyIsInVzZXIuJGFwcF9pZDo1NzU3Ni4kdXNlcl9pZDoxNjQ4MzY5OTk1OTMzMDI2NDUxIiwidXNlci4kYXBwX2lkOjU3NTc2LiR1c2VyX2lkOjE2NDgzNjk1NjI3MzY5MjEzMTgiXSwiYXBwX2lkIjo1NzU3NiwidXNlcl9pZCI6MTY0ODM2OTk5NTkzMzAyNjQ1MX0.v0Z4ovUAIjwJ_RFIpOYXTvV1iyLYYGfSrG1WKGWjITo; _ga_8S8Y1X62NG=GS1.1.1710228316.2.1.1710228406.30.0.0; carrotquest_session=c3bsw85obm728t84s6ee8vojekgagus0; carrotquest_session_started=1'
            } 
            data = {"Sku":[self.sku],"Place":"ozon"}
            url = "https://plugin.mpstats.io/pluginapi"
            res = requests.post(url=url,headers=headers,data=json.dumps(data))
            data = res.json()
            print(data)
            items = data['items'][self.sku]
            self.sale=items['OrdersNewArray'][-3:]
            self.shop_name=items['Seller']
            time.sleep(1)
    
    def set_sheet_premium(self):
        with lock:
            import http.client
            conn = http.client.HTTPSConnection("www.kdocs.cn")

            payload = {"Context":{"argv":{
                'name':self.name,
                'sku':self.sku,
                'title':self.title,
                'shop_name':self.shop_name,
                'comments':self.comments,
                'questions':self.questions,
                'price':self.price,
                'day1':self.sale[0]['day'],
                'sale1':self.sale[0]['cnt'],
                'day2':self.sale[1]['day'],
                'sale2':self.sale[1]['cnt'],
                'day3':self.sale[2]['day'],
                'sale3':self.sale[2]['cnt'],
                'href':self.href,
                'time':datetime.date.today().strftime("%Y-%m-%d")
            }}}

            AirScript_Token = "9NejrdQLV6UC2cJ98p1eJ"
            Script_Url = "/api/v3/ide/file/cjSwBTF9A0nF/script/V2-1xGlmoAeRttMEVy3ISCjL3/sync_task"

            headers = {
                'Content-Type': "application/json",
                'AirScript-Token': AirScript_Token
            }

            conn.request("POST", Script_Url, json.dumps(payload), headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            with open("log.json","w",encoding="utf-8") as f:
                f.write(data)
            conn.close()

    def run(self):

        page=self.page.new_tab(self.href)
        if page('t:title')=="Just a moment...":
            page.wait(30)
        self.search_premium_product(page)
        self.set_sheet_premium()
        self.console()
        page.close()

def read_config():
    with open("config.json","r",encoding="utf-8") as f:
        config = json.load(f)
    return dict(config)

def read_err():
    with open("error.txt","r",encoding="utf-8") as f:
        hrefs = f.readlines()
    hrefs = [i.strip() for i in hrefs]
    return hrefs



def main():
    last_run_timestamp_str = sys.argv[1]
    last_run_timestamp = int(last_run_timestamp_str)
    current_timestamp = int(time.time())

    if current_timestamp - last_run_timestamp >= 259200:  # 3天时间差（以秒为单位）
        # 执行核心业务逻辑
        print("It's been at least 3 days since the last run.")
        config = read_config()
        hrefdict=[]
        for i in config.keys():
            for href in config[i]:
                hrefdict.append({'href':href,'name':i})
        
        # config = read_err()
        # hrefdict=[]
        # for href in config:
        #     hrefdict.append({'href':href,'name':'error'})


        co = ChromiumOptions()
        co.headless(False)
        co.no_imgs(True)
        co.no_js(True)
        co.set_user_data_path(r"userdata")
        page = ChromiumPage(co)

        with ThreadPoolExecutor(max_workers=5) as executor:
            for i in hrefdict:
                prem = PremiumProduct(i['href'])
                prem.name = i['name']
                prem.page = page
                executor.submit(prem.run)

        page.quit()
        # 更新LAST_RUN_TIMESTAMP
        # 这里由于GitHub Actions限制，我们不能直接在脚本中更新Secrets
        # 可以选择调用GitHub REST API来更新（需要一个PAT）
        # 或者让脚本输出新的timestamp，然后在后续Action步骤中更新
        new_timestamp = current_timestamp
        print(f"New timestamp for updating secret: {new_timestamp}")

        # 示例更新GitHub Secrets的API调用（需要PAT）
        token = "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"
        headers = {'Authorization': f'token {token}'}
        url = f'https://api.github.com/repos/{"juhua111"}/{"Action-test"}/actions/secrets/LAST_RUN_TIMESTAMP'
        data = {'value': str(new_timestamp)}
        response = requests.put(url, headers=headers, json=data)
        print(response.status_code, response.json())

    else:
        print("Not running because it hasn't been 3 days since the last run.")


if __name__ == '__main__':
    main()