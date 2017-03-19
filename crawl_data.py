# -*-coding:utf-8 -*-
import sys
import codecs
import threading
import time
import urllib2
import json
import csv
import random
import wx
from wx.lib.pubsub import pub
import math
reload(sys)
sys.setdefaultencoding("utf-8")


class CrawlData(threading.Thread):
    def __init__(self, current_thread_num, thread_type):
        threading.Thread.__init__(self)
        self.current_thread_num = current_thread_num
        self.thread_type = thread_type

    def run(self):
        if self.thread_type == 'pub':
            self.crawl_pub_data()
        elif self.thread_type == 'pri':
            self.crawl_pri_data()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'}

    def crawl_pub_data(self):
        page = self.current_thread_num - 1
        try:
            rand = random.random()
            url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/fund?size=100&page=' + str(page) + '&rand=' + str(rand)
            req = urllib2.Request(url, '{}', self.headers)
            response = urllib2.urlopen(req, timeout=10)
            json_data = json.loads(response.read(), encoding='utf-8')
            found_list = json_data['content']
            element_num = len(json_data['content'])

            total_elements = json_data['totalElements']
            pages = math.ceil(total_elements / 100.0)
            data = []

            for i in range(element_num):
                try:
                    row_values = []
                    if found_list[i].has_key('fundNo'):
                        fund_no = str(found_list[i]['fundNo'])
                        row_values.append(fund_no)
                    if found_list[i].has_key('fundName'):
                        fund_name = str(found_list[i]['fundName'])
                        row_values.append(fund_name)
                except Exception,e:
                    continue
                data.append(row_values)

            wx.CallAfter(pub.sendMessage, 'new.pub.thread', data=data, finish_thread_num=self.current_thread_num, pages=int(pages))
        except Exception, e:
            wx.CallAfter(pub.sendMessage, 'craw.error', msg=str(e), finish_thread_num=self.current_thread_num - 1)
            wx.CallAfter(pub.sendMessage, 'new.pub.thread', data='', finish_thread_num=self.current_thread_num - 1, pages=-1)

    def crawl_pri_data(self):
        page = self.current_thread_num - 1
        try:
            rand = random.random()
            url = 'http://gs.amac.org.cn/amac-infodisc/api/fund/account?size=100&page=' + str(page) + '&rand=' + str(
                rand)
            req = urllib2.Request(url, '{}', self.headers)
            response = urllib2.urlopen(req, timeout=10)
            json_data = json.loads(response.read(), encoding='utf-8')
            found_list = json_data['content']
            element_num = len(json_data['content'])
            total_elements = json_data['totalElements']
            pages = math.ceil(total_elements / 100.0)
            data = []

            for i in range(element_num):
                try:
                    row_values = []
                    if found_list[i].has_key('registerCode'):
                        fund_no = str(found_list[i]['registerCode'])
                        row_values.append(fund_no)
                    if found_list[i].has_key('name'):
                        fund_name = str(found_list[i]['name'])
                        row_values.append(fund_name)
                except Exception,e:
                    continue
                data.append(row_values)

            wx.CallAfter(pub.sendMessage, 'new.pri.thread', data=data, finish_thread_num=self.current_thread_num, pages=int(pages))
        except Exception, e:
            wx.CallAfter(pub.sendMessage, 'craw.error', msg=str(e), finish_thread_num=self.current_thread_num - 1)
            wx.CallAfter(pub.sendMessage, 'new.pri.thread', data='', finish_thread_num=self.current_thread_num - 1, pages=-1)

