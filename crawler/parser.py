from django.shortcuts import render
from selenium import webdriver
from crawler.parser_geneerator import JsonToGetText
import os;
from selenium.webdriver.chrome.options import Options as ChromeOptions


def parser_post(request):
    return_text = {}
    if request.method == 'POST':
        url = request.POST['url']
        html = request.POST['html']
        json = request.POST['json']
        return_text['URL'] = url
        return_text['html'] = html
        if url is not '' and html is '':
            #driver = webdriver.Chrome(
            #    executable_path=r'/Users/qq/PycharmProjects/parseltongue/chromedriver/chromedriver')
            chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
            opts = ChromeOptions()
            opts.binary_location = chrome_bin
            driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=opts)
            driver.get(url)
            html = driver.page_source
            driver.close()
        if html is not '' and json is not '':
            get_html = JsonToGetText(html, json)
            return_text['tag'] = get_html.get_tag_text()
            return_text['table'] = get_html.get_table_text()
    return render(request, "crawler.html", return_text)