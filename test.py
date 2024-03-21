from DrissionPage import ChromiumOptions,ChromiumPage
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
co = ChromiumOptions()
co.headless(True)
co.no_imgs(True).mute(True)

page = ChromiumPage(co)
page.get("https://www.baidu.com")
title = page.ele('tag:title').text
print(title)
page.quit()
