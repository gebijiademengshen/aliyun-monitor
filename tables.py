# -*- coding: utf8 -*-
import sys
from xlsxwriter import workbook
reload(sys)
sys.setdefaultencoding('utf-8')
class WriterExcel(object):
    def __init__(self,filename,title,id,alias,disk_info):
        self.filename = filename
        self.title = title
        self.id = id
        self.alias = alias
        self.disk_info = disk_info
    def write_excel(self):
        work = workbook.Workbook(self.filename)
        worksheet = work.add_worksheet()
        format_title = work.add_format({'bold':True,'font_size':12})
        format_title.set_align('center')
        format_title.set_align('vcenter')
        format_body = work.add_format({'font_size':10})
        format_body.set_align('center')
        format_body.set_align('vcenter')
        format_color_red = work.add_format({'bold': True,'font_size':10,'bg_color':'red'})    #加粗字体并调整字体背景颜色
        format_color_red.set_align('center')
        format_color_red.set_align('vcenter')
        format_color_yellow = work.add_format({'bold': True, 'font_size': 10, 'bg_color': 'yellow'})  # 加粗字体并调整字体背景颜色
        format_color_yellow.set_align('center')
        format_color_yellow.set_align('vcenter')
        worksheet.set_row(0, 22)
        worksheet.set_column(0, 0, 27)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 3, 12)
        worksheet.set_column(3, 4, 16)
        worksheet.set_column(4, 5, 10)
        worksheet.set_column(6, 6, 12)
        worksheet.set_column(7, 9, 12)
        title = self.title
        row = 0
        col = 0
        for item in title:
            worksheet.write(row, col, item, format_title)
            col += 1
        for line in self.id:
            row += 1
            col = 0
            worksheet.write(row, col, line, format_body)
        row = 0
        for line2 in self.alias:
            row += 1
            col = 1
            worksheet.write(row, col, line2, format_body)
        row = 1
        for disk_line in self.disk_info:    #遍历每个实例的信息
            col = 1
            for key in disk_line:   #遍历单个实例的信息
                col += 1
                if type(key) is int and key >= 80 and key <85:
                    worksheet.write(row, col, key, format_color_yellow)
                elif type(key) is float and key >= 80 and key < 85:
                    worksheet.write(row, col, key, format_color_yellow)
                elif type(key) is int and key >= 85:
                    worksheet.write(row, col, key, format_color_red)
                elif type(key) is float and key >= 85:
                    worksheet.write(row, col, key, format_color_red)
                else:
                    worksheet.write(row, col, key, format_body)
            row +=1
        work.close()
class WriteExcel_Rds(object):
    def __init__(self,filename,title,id,alias,times,disk_info):
        self.filename = filename
        self.title = title
        self.id = id
        self.alias = alias
        self.times = times
        self.disk_info = disk_info
    def write_excel_rds(self):
        work = workbook.Workbook(self.filename)
        worksheet = work.add_worksheet()
        format_title = work.add_format({'bold':True,'font_size':12})
        format_title.set_align('center')
        format_title.set_align('vcenter')
        format_body = work.add_format({'font_size':10})
        format_color_red = work.add_format({'bold': True, 'font_size': 10, 'bg_color': 'red'})   #加粗字体并调整字体背景颜色
        format_color_red.set_align('center')
        format_color_red.set_align('vcenter')
        format_body.set_align('center')
        format_body.set_align('vcenter')
        format_color_yellow = work.add_format({'bold': True, 'font_size': 10, 'bg_color': 'yellow'})  # 加粗字体并调整字体背景颜色
        format_color_yellow.set_align('center')
        format_color_yellow.set_align('vcenter')
        worksheet.set_row(0, 22)
        worksheet.set_column(0, 0, 27)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 3, 20)
        worksheet.set_column(4, 3, 15)
        worksheet.set_column(6, 5, 15)
        title = self.title
        row = 0
        col = 0
        for item in title:
            worksheet.write(row, col, item, format_title)
            col += 1
        for line in self.id:
            row += 1
            col = 0
            worksheet.write(row, col, line, format_body)
        row = 0
        for line2 in self.alias:
            row += 1
            col = 1
            worksheet.write(row, col, line2, format_body)
        row = 0
        for line3 in self.times:
            row +=1
            col = 2
            worksheet.write(row, col, line3, format_body)
        row = 1
        for disk_line in self.disk_info:    #遍历每个实例的信息
            col = 2
            for key in disk_line:   #遍历单个实例的信息
                col += 1
                if type(key) is int and key >= 80 and key < 85:
                    worksheet.write(row, col, key, format_color_yellow)
                elif type(key) is float and key >= 80 and key <85:
                    worksheet.write(row, col, key, format_color_yellow)
                elif type(key) is int and key >= 85:
                    worksheet.write(row, col, key, format_color_red)
                elif type(key) is float and key >= 85:
                    worksheet.write(row, col, key, format_color_red)
                else:
                    worksheet.write(row, col, key, format_body)
            row +=1
        work.close()