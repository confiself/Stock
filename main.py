#! /usr/python/bin
# -*-coding:utf-8 -*-
import wx
import os
from crawl_data import CrawlData
import threading
from wx.lib.pubsub import pub
import sys
import csv
import codecs
import time
reload(sys)
sys.setdefaultencoding("utf-8")
class RefactorExample(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'股票分析器', size=(640, 480))
        self.text_list = wx.TextCtrl(self, -1,  style=wx.TE_MULTILINE)
        self.createMenuBar()
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -1, -1])
        pub.subscribe(self.OnNewPubThread, 'new.pub.thread')
        pub.subscribe(self.OnNewPriThread, 'new.pri.thread')
        pub.subscribe(self.OnCrawError, 'craw.error')
        self.craw_pri_thread_index = 0
        self.craw_pub_thread_index = 0
        self.pub_total_pages = 0
        self.pri_total_pages = 0
        if os.path.exists('./log.txt'):
            os.remove('./log.txt')

    def menuData(self): #菜单数据
        return ((u'&文件',
                (u'&导入目录', '', self.on_load_data),
                (u'&退出', '', self.on_close_window)),
                (u'&处理',
                (u'&策略一', '', self.on_process),
                 (u'爬公募数据', '', self.OnCrawPubData),
                 (u'爬私募数据', '', self.OnCrawPriData)))

    #创建菜单
    def createMenuBar(self):
        self.menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1:]
            self.menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(self.menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachLabel, eachStatus, eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem = menu.Append(-1, eachLabel, eachStatus)
            self.Bind(wx.EVT_MENU, eachHandler, menuItem)
        return menu

    wildcard = 'excel files (*.xls)|*.xls|All files (*.*)|*.*'

    def on_load_data(self, event):
        dlg = wx.DirDialog(self, u'打开文件夹')
        if dlg.ShowModal() == wx.ID_OK:
            data_dir = dlg.GetPath()
            self.table.set_data_dir(data_dir)
        dlg.Destroy()

    def on_save_data(self, event):
        dlg = wx.FileDialog(self, u'另存为',os.getcwd(),
                            style=wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            print filename
        dlg.Destroy()

    def on_process(self, event):
        self.table.process_data()
        box = wx.MessageDialog(self, u'处理完毕！',
                         caption=u'提示',
                    style = wx.OK|wx.CANCEL,
                    pos = wx.DefaultPosition)
        box.ShowModal()
        box.Destroy()

    def on_close_window(self, event):
            self.Destroy()

    def on_craw_data(self, event):
        self.statusbar.SetStatusText(u'爬取数据中...', 0)
        pub.sendMessage('new.pub.thread', data='', finish_thread_num=0, pages=1)
        # self.OnNewPriThread(self.craw_pri_thread_index)

    def OnCrawPubData(self,event):
        self.statusbar.SetStatusText(u'爬取公募数据中...', 0)
        file_path = './pub_fund.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
        pub.sendMessage('new.pub.thread', data='', finish_thread_num=0, pages=1)

    def OnCrawPriData(self, event):
        self.statusbar.SetStatusText(u'爬取私募数据中...', 0)
        file_path = './pri_fund.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
        pub.sendMessage('new.pri.thread', data='', finish_thread_num=0, pages=1)

    def OnNewPubThread(self, data, finish_thread_num, pages):
        if pages > self.pub_total_pages:
            self.pub_total_pages = pages
        if finish_thread_num > self.pub_total_pages: #finish
            self.text_list.AppendText(u'公募数据抓取完毕！' + '\r')
            self.statusbar.SetStatusText(u'公募数据抓取完毕！', 0)
            return
        print finish_thread_num
        with open('./pub_fund.csv', 'ab+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.write(codecs.BOM_UTF8)
            if finish_thread_num == 0:
                csv_writer.writerow(['fundNo', 'fundName'])
            else:
                if isinstance(data, list):
                    csv_writer.writerows(data)

        #new thread
        self.text_list.AppendText(u'抓取公募数据中...' + str(finish_thread_num) + '/' + str(self.pub_total_pages) + '\r')
        for i in range(1):
            self.craw_pub_thread_index = finish_thread_num + 1
            craw_data = CrawlData(self.craw_pub_thread_index, thread_type='pub')
            craw_data.start()

    def OnNewPriThread(self, data, finish_thread_num, pages):
        if pages > self.pri_total_pages:
            self.pri_total_pages = pages
        if finish_thread_num > self.pri_total_pages:
            self.text_list.AppendText(u'私募数据抓取完毕！' + '\r')
            self.statusbar.SetStatusText(u'私募数据抓取完毕！', 0)
            return
        print finish_thread_num
        with open('./pri_fund.csv', 'ab+') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.write(codecs.BOM_UTF8)
            if finish_thread_num == 0:
                csv_writer.writerow(['registerCode', 'name'])
            else:
                if isinstance(data, list):
                    csv_writer.writerows(data)

        #new thread
        self.text_list.AppendText(u'抓取私募数据中...' + str(finish_thread_num) + '/' + str(self.pri_total_pages) + '\r')
        for i in range(1):
            self.craw_pri_thread_index = finish_thread_num + 1
            craw_data = CrawlData(self.craw_pri_thread_index, thread_type='pri')
            craw_data.start()



    def OnCrawError(self, msg, finish_thread_num):
        self.text_list.AppendText(u'抓取数据页 '+ str(finish_thread_num) + u' 出错,重新抓取中...'+'\r')
        with open('./log.txt', 'a+') as log_file:
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            log_file.write(current_time + '----' + str(finish_thread_num) + ':' + msg + '\r')

if __name__ == '__main__':
    app = wx.App()
    frame = RefactorExample(parent=None, id=-1)
    frame.Show()
    app.MainLoop()