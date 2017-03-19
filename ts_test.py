#-*- coding:utf-8 -*-
import pandas as td
import tushare as ts
import urllib2
def get_all_stock():
    df = ts.get_today_all()
    print df.values


def get_10_sh(stock_id):
    try:
        url = 'http://www.yidiancangwei.com/gudong/sdlt_' + stock_id + '.html'
        response = urllib2.urlopen(url, timeout=10)
        result = str(response.read())
        for i in range(11):
            result, shareholds = get_sh_str(result)
            if shareholds == None:
                break
            else:
                print shareholds

    except Exception,e:
        pass

def get_sh_str(html_data):
    try:
        start = str(html_data).index('Val=')
        html_data = html_data[start + 4:]
        end = str(html_data).index('"')
        sh = html_data[:end]
        return html_data, sh
    except Exception,e:
        return None,None


def get_all_stock_id():
    stock_info=ts.get_stock_basics()
    for i in stock_info.index:
        get_10_sh(i)
if __name__ == '__main__':
    get_all_stock_id()