from selenium import webdriver
from django.shortcuts import render
from crawler.parser_geneerator import Setting
from selenium.webdriver.chrome.options import Options


def setting_post(request):
    return_text = {}
    if request.method == 'POST':
        url = request.POST['url']
        tags = request.POST['tags']
        tags_map = request.POST['map']
        table = request.POST['table']
        html = request.POST['html']
        return_text['URL'] = url
        return_text['html'] = html
        if url is not '' and html is '':
          #  driver = webdriver.Chrome(
          #      executable_path=r'/Users/qq/PycharmProjects/parseltongue/chromedriver/chromedriver')
            chrome_options = Options()
            chrome_options.binary_location = '/app/.apt/usr/bin/google-chrome'
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(executable_path='/app/.apt/usr/bin/google-chrome', chrome_options=chrome_options)
            driver.get(url)
            html = driver.page_source
            driver.close()
        if html is not '':
            setting = Setting(html)
            if tags is not '':
                setting.set_tag(str(tags).split(','))
            if tags_map is not '':
                setting.set_tag_map(tags_map)
            if table is not '':
                setting.set_table(table)
            return_text['json'] = setting.to_json()
    return render(request, "setting.html", return_text)