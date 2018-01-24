# encoding: utf-8
"""
@author: lileilei
@site: 
@software: PyCharm
@file: main.py
@time: 2017/4/27 13:41
"""
from report.repPorT import report
from  report.email_send import create_report_sendemali
if __name__=="__main__":
    report(r'case')
    create_report_sendemali('18510574788@163.com', 'Mf2468101', '583469256@qq.com')
