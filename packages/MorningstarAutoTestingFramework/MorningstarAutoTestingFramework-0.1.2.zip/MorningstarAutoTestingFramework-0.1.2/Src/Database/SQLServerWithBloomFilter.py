# -*- coding: utf-8 -*-
from pybloom import ScalableBloomFilter
import pyodbc

cnxn = pyodbc.connect('driver={SQL Server};server=192.168.0.2;database=pic;uid=yyb;pwd=sz123')
cursor = cnxn.cursor()
row = cursor.execute("select top 5 * from admin").fetchall()
# fetchall返回的是列表 fetchone返回的是类
cnxn.close()  # 关闭连接
sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
for a in row:
    sbf.add('dddd')
    print 'ddd' in sbf


