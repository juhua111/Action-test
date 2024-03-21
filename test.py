from DrissionPage import ChromiumPage,ChromiumOptions
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class PremiumProduct:
    def __init__(self,href):
        #商品链接
        self.href = href
        #商品价格
        self.price = 0
        #商品名称
        self.name = ""
        #商品sku
        self.sku = ""
        #商品标题
        self.title = ""
        #商品库存
        self.stock=0
        #商品周销
        self.sale=0
        #商品周gmv
        self.gmv=0
        #商品好评
        self.starts=0
        #商品评论数
        self.comments=0
def run():
    co = ChromiumOptions()
    co.headless(False)
    co.no_imgs(True)
    co.set_user_data_path(r"appdata")
    page = ChromiumPage(co)
    premium = PremiumProduct('https://www.ozon.ru/product/igrushka-disney-mandalorets-grogu-child-baby-yoda-301451890/?campaignId=346')
    tab = page.new_tab(premium.href)
    comments = page.wait.ele_loaded('xpath://*[@id="layoutPage"]/div[1]/div[6]/div/div[1]/div[3]/div[4]/div/div[1]/div[1]/div/div[1]/div/button/span/div/span[2]',timeout=20)
    print(tab.html)

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        run()