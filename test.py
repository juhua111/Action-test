from DrissionPage import ChromiumOptions,ChromiumPage

co = ChromiumOptions()
co.headless(True)
co.no_imgs(True).mute(True)

page = ChromiumPage(co)
page.get("https://www.baidu.com")
title = page.ele('tag:title').text
print(title.encode('utf-8').decode())
page.quit()
