#! coding:utf-8
# 35 671808 172608 2
# 35 917707 561497 7 7p 128g 黑
# 35 381708 961355 8 7p 128g 银
# 35 928506 481566 9
import random
import sys
import os
def generate(num):
    path = sys.path[0]
    print path
    path = sys.argv[0].split('/')
    path = '/'.join(path[:-1])
    print path
    with open(os.path.join(path, 'ios_imei.csv'), 'w') as f_w:
        for i in range(num):
            imei_list = []
            imei_list.append([x for x in range(10, 99)])
            imei_list.append([x for x in range(1)])
            imei_list.append([x for x in range(1,10)])
            imei_list.append([x for x in range(10, 99)])
            imei_list.append([x for x in range(10, 99)])
            imei_list.append([x for x in range(10, 99)])
            imei_list.append([x for x in range(1, 10)])
            imei = '35 67'
            split_index = ['','',' ','','', ' ', '']
            for j, imeis in enumerate(imei_list):
                rand = int(random.random() * 1000)
                index = rand % len(imeis)
                imei += str(imeis[index]) + split_index[j]
            f_w.writelines(imei + '\n')

if __name__ == '__main__':
    num = raw_input('请输入生成的imei数（默认1万个）：')
    if not num:
        num = '10000'
    if num and num.isdigit():
        print '目标', num, '个,正在生成...'
        generate(int(num))
        print('生成完毕！保存在ios_imei.csv中！')
    else:
        print('请重新运行软件，并输入整数.')