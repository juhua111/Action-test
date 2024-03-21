from DrissionPage import ChromiumOptions,ChromiumPage
from concurrent.futures import ThreadPoolExecutor
import time
import re

co = ChromiumOptions()
co.no_imgs(True).mute(True)
page = ChromiumPage(co)

def timetest(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()  
        print(f"函数{func.__name__}运行时间：{end_time - start_time}秒")
    return wrapper





def test_baidu(index,newpage=True,tab=None):
    if newpage:
        tab = page.new_tab(f'https://www.ozon.ru/category/sumki-na-plecho-zhenskie-17002/?page={index}')
    divs = tab.s_eles("xpath://*[@id='paginatorContent']/div/div/div")
    divs2 = tab.s_eles(".:tile-root")
    # 等待页面加载完全
    if len(divs)!= len(divs2):
        tab.wait(1.5)
        test_baidu(index,False,tab=tab)
    else:
        # 解析页面内容
        data = {}
        for div in divs2:
            sku = re.search(r'.*-(\d+)\/\?.*',div.ele('tag:a').link).group(1)
            data[sku]={
                "imghref":div.ele('tag:img').link,
                "ahref":div.ele('tag:a').link,
                "title":div.ele('.:tsBody500Medium').text,
                "sku": sku
            }
        print(data)
        tab.close()

# 多线程测试
@timetest
def main():
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(30):
            executor.submit(test_baidu, i+1)
    page.quit()
    #test_baidu(1)
if __name__ == '__main__':
    main()
