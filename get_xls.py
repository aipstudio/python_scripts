#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlrd

def main():
    rb = xlrd.open_workbook('c:/tmp/Новый.xls',formatting_info=True)
    sheet = rb.sheet_by_index(0)
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        print(int(row[1]))
        #for c_el in row:
        #    print (c_el)

if __name__ == '__main__':
    main()