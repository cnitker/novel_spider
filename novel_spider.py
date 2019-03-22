# -*- coding: utf-8 -*-
import re

# 笔趣阁小说采集脚本
# author LR
# 使用之前请自行安装 requests,BeautifulSoup

from bs4 import BeautifulSoup
import requests


class novel_download(object):
    novel_page_urls = []
    novel_name = ''
    novel_nums = 1

    novel_server = 'https://www.biquge5.com/'
    novel_server_url = 'https://www.biquge5.com/1_1293/'

    # 自定义开始抓取页
    custom_first_url = ""


    def get_novel_urls(self):
        #    headers = {'Referer': 'https://www.biquge5.com/1_1293/',
        #               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        res = requests.get(self.novel_server_url)
        res.encoding = 'gbk'

        soup = BeautifulSoup(res.text, 'html.parser')
        novel_name = soup.find('h1')

        self.novel_name = novel_name.string

        ul = soup.find('ul', class_="_chapter")
        a_href = BeautifulSoup(str(ul).replace('\n', ''), 'html.parser')
        frist_url = a_href.find('a').get('href')

        if not self.custom_first_url:
            frist_url = self.custom_first_url

        self.novel_page_urls.append(frist_url)
        self.get_novel_content_next_link(frist_url)

    def get_novel_content_next_link(self, page_url):
        headers = {'Referer': 'https://www.biquge5.com/1_1293/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

        res = requests.get(page_url)
        res.encoding = 'gbk'
        content = res.text

        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('h1').string

        nextlink = soup.find('a', string=re.compile('下一页'))

        if nextlink is None:
            nextlink = soup.find('a', string=re.compile('下一章'))

        if nextlink.get('href') == 'https://www.biquge5.com/shuku/0/weekvisit-0-1.html':
            return "列表数据采集完成共", self.novel_nums, " 条"

        full_link = self.novel_server_url + nextlink.get('href')
        self.novel_page_urls.append(full_link)
        self.novel_nums += 1
        print("第{", int(self.novel_nums), "个}" + title.center(20, '-') + "连接  {url}入列成功".format(url=full_link))

        self.get_novel_content_next_link(full_link)

    def get_novel_content(self, target):
        headers = {'Referer': 'http://www.xbiquge.la/25/25786/',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        req = requests.get(target, headers=headers)
        req.encoding = 'gbk'
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')

        title = bf.find('h1')
        # return title.string

        content = bf.find('div', id='content')

        content = str(content).replace('<br/>', '\n')
        content = content.replace('<script>s1();</script>', '')
        content = content.replace('&lt;', '')
        content = BeautifulSoup(content, 'html.parser')
        content = content.get_text()
        return title.string + "\n\n" + content.replace('\xa0', '')

    def write(self, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(text)
            f.write('\n\n')


if __name__ == '__main__':
    dl = novel_download()
    dl.get_novel_urls()
    # dl.get_novel_content_next_link('https://www.biquge5.com/1_1293/13961997.html')

    print("小说[{name}]下载中...".format(name=dl.novel_name))

    for i in range(dl.novel_nums):
        print(dl.novel_page_urls[i])
        dl.write('./{name}.txt.'.format(name=dl.novel_name), dl.get_novel_content(dl.novel_page_urls[i]))
        print("已下载:{:.2f}%".format(float((i+1) / dl.novel_nums) * 100) + '\r')

    print("小说[{name}]下载中完成".format(name=dl.novel_name))
