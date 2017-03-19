#-*- encoding:UTF-8 -*-
import wx
import wx.grid
import os
import csv
fields = ['stock_name', 'vitality_rate', 'net_volumn', 'total_volumn', 30, 50, 70, 100, 200, 300, 500, 1000, 2000, 5000, 10000, 'Inf']
class TestTable(wx.grid.PyGridTableBase):#定义网格表
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = []
        self.colLabels = fields
        self.data_dir = ''

    def GetNumberRows(self):
        return 50
    def GetNumberCols(self):
        return len(fields)
    def IsEmptyCell(self, row, col):
        return True

    def GetValue(self, row, col):#为网格提供数据
        # value = self.data[row][fields[col]]
        # if value is not None:
        #     return value
        # else:
        #     return ''
        return ''
    def SetValue(self, row, col, value):#给表赋值
        pass


    def set_data_dir(self, data_dir):
        self.data_dir = data_dir

    def process_data(self):
        result_list = []
        for file_name in os.listdir(self.data_dir):
            result_dict = get_result_dict(self.data_dir, file_name)
            result_list.append(result_dict)

        result_list.sort(key=lambda x:x['vitality_rate'], reverse=True)
        save_result('./result.csv', result_list)


def save_result(file_path, result_list):
    with open(file_path, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file, fields)
        csv_writer.writerow(fields)
        for record in result_list:
            row_values = []
            for field in fields:
                if record.has_key(field):
                    row_values.append(record[field])
                else:
                    row_values.append('')
            csv_writer.writerow(row_values)


def get_region_value(volumn, fields):
    if volumn > 10000:
        return 'Inf'
    for key in fields:
        if isinstance(key, int) and volumn <= key:
            return key


def get_result_dict(file_dir, filename):
    path = os.path.join(file_dir, filename)
    stock_name = filename.split('.')[0]
    if stock_name[0] == '0':
        stock_name = 'u' + stock_name
    volume_dic = {'stock_name': stock_name}

    first_line = True
    total_volumn = 0
    net_volumn = 0

    csv_file = file(path, 'rb')
    reader = csv.reader(csv_file)

    for line in reader:
        if first_line:
            first_line = False
            continue
        tran_volume = (int)(line[3])
        tran_volume_type = get_region_value(tran_volume, fields)
        tran_type = line[6]
        total_volumn += tran_volume
        if tran_type == 'S':
            tran_volume = -tran_volume
        net_volumn += tran_volume
        if volume_dic.has_key(tran_volume_type):
            volume_dic[tran_volume_type] += tran_volume
        else:
            volume_dic[tran_volume_type] = tran_volume
    print total_volumn

    # 计算活跃度
    abs_net_volumn = 0
    for value in volume_dic.values():
        if isinstance(value, int):
            abs_net_volumn += abs(value)
            print abs(value)
    print abs_net_volumn
    vitality_rate = float(abs_net_volumn) / total_volumn
    volume_dic['vitality_rate'] = vitality_rate
    print vitality_rate
    # 添加总量和净额
    volume_dic['total_volumn'] = total_volumn
    volume_dic['net_volumn'] = net_volumn
    return volume_dic

if __name__ == '__main__':
    # pass
    volume_dic = {'stock_name': r'u000001'}
    csv_file = file('D://2017-01-10//000001.csv', 'rb')
    reader = csv.reader(csv_file)
    first_line = True
    total_volumn = 0
    net_volumn = 0
    for line in reader:
        if first_line:
            first_line = False
            continue
        tran_volume = (int)(line[3])
        tran_volume_type = get_region_value(tran_volume, fields)
        tran_type = line[6]
        total_volumn += tran_volume
        if tran_type == 'S':
            tran_volume = -tran_volume
        net_volumn += tran_volume
        if volume_dic.has_key(tran_volume_type):
            volume_dic[tran_volume_type] += tran_volume
        else:
            volume_dic[tran_volume_type] = tran_volume
    print total_volumn

    #计算活跃度
    abs_net_volumn = 0
    for value in volume_dic.values():
        if isinstance(value, int):
            abs_net_volumn += abs(value)
            print abs(value)
    print abs_net_volumn
    vitality_rate = float(abs_net_volumn) / total_volumn
    volume_dic['vitality_rate'] = vitality_rate
    print vitality_rate
    #添加总量和净额
    volume_dic['total_volumn'] = total_volumn
    volume_dic['net_volumn'] = net_volumn
    print volume_dic

    with open('d:/c.csv','wb') as csvfile:
        print volume_dic

        writer = csv.writer(csvfile, fields)
        writer.writerow(fields)
        row_values = []
        for field in fields:
            row_values.append(volume_dic[field])
        writer.writerow(row_values)










