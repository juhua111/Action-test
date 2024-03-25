from DrissionPage import ChromiumOptions,SessionPage,WebPage

page = WebPage()
page.get("https://www.ozon.ru/product/d-aromatizator-avtomobilnyy-cologne-1415420851/?oos_search=false")
print(page.html)
with open("test2.html", "w", encoding="utf-8") as f:
    f.write(page.html)