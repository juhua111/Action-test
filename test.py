from DrissionPage import ChromiumPage,ChromiumOptions,WebPage
from DrissionPage._pages.chromium_tab import ChromiumTab
import sys
import json
import requests
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class PremiumProduct:
    def __init__(self,href):
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

    def console(self):
        print(f'商品评价数{self.comments}')
        print(f'商品提问{self.questions}')
        print(f'商品标题{self.title}')
        print(f'商品三日销{self.sale}')
        print(f'商品价格{self.price}')
        print(f'商品sku{self.sku}')
        print(f'商品链接{self.href}')

    def search_premium_product(self,tab:ChromiumTab,index=0):
        try:
            layoutPage = tab.s_ele('x://*[@id="layoutPage"]')
            self.comments=layoutPage('x:/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[1]/a/div').text
            self.questions=layoutPage('x:/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[2]/div[2]/a/div').text
            self.title=layoutPage('x:/div[1]/div[4]/div[3]/div[1]/div[1]/div[2]/div/div[1]/h1').text
            self.sku=layoutPage('x:/div[1]/div[4]/div[2]/div/div/div/div[2]/div[1]/button/div').text
            self.price=layoutPage('@data-widget=webPrice').eles('t:span')[3].text
        except Exception as e: 
            print("商品信息获取失败 "+str(e))
            self.search_premium_product(tab,index=index)
        
        self.get_premium_stock_sale_gmv()

    def get_premium_stock_sale_gmv(self):
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

        
def run():
    co = ChromiumOptions()
    co.headless(False)
    co.no_imgs(True)
    page = ChromiumPage(co)
    premium = PremiumProduct('https://www.ozon.ru/product/nabor-figurok-skibidi-tualet-unitaz-skibidisty-kameramen-spikermen-1212924339/?advert=r4GQG1gACtcW3pIcu0kywgPbnpDWlYapVLBW4SYJvc1s0kcV9udSUt5NiLTVPimQRM6siXRvj2omLt4mcIyMVcbD6SHQFt_uYGCF5UcqU3PjxNmTAvdj7Kd272tRmvyIexCcHam_z6ZCmGO9yACmnpv1itmAMHhXxM34yWI3r4FUU_CE-kV6SJBV0-ohaY8L55d9P3IxtoPArA&avtc=1&avte=2&avts=1711071471')
    tab = page.new_tab(premium.href)
    tab.wait(10)
    premium.search_premium_product(tab)
    premium.console()

    tab.close()
    page.quit()



if __name__ == '__main__':
    run()