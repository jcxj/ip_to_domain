import argparse
import configparser

import pandas as pd

import fofa_client
import colorama
import xlsxwriter
from prettytable import PrettyTable
import os
import time
import re
import requests
import codecs
import mmh3

#获取用户信息
def get_userinfo():
    user_info = client.get_userinfo()
    email = user_info["email"]  # 查询用户邮箱
    username = user_info["username"]  # 查询用户名
    fcoin = user_info["fcoin"]  # 查询F币剩余数量
    isvip = user_info["isvip"]  # 查询用户是否为VIP
    vip_level = user_info["vip_level"]  # 查询用户VIP等级
    print(colorama.Fore.RED + "======个人信息=======")
    print(colorama.Fore.GREEN + "[+] 邮箱：{}".format(email))
    print(colorama.Fore.GREEN + "[+] 用户名：{}".format(username))
    print(colorama.Fore.GREEN + "[+] VIP等级：{}".format(vip_level))

#进行单语句查询
def get_search(query_str):
    start_page = 1
    end_page = 2
    fields = config.get("fields", "fields")  # 获取查询参数
    print(colorama.Fore.RED + "======查询内容=======")
    print(colorama.Fore.GREEN + "[+] 查询语句：{}".format(query_str))
    print(colorama.Fore.GREEN + "[+] 查询参数：{}".format(fields))
    print(colorama.Fore.GREEN + "[+] 查询页数：{}-{}".format(start_page, end_page))
    print("时间会比较久")
    database = []
    for page in range(start_page, end_page):  # 从第1页查到第n页
        try:
            data = client.get_data(query_str, page=page, fields=fields)  # 查询第page页数据
        except Exception as e:
            fields = "Error"
            data = {"results": ["{}".format(e)]}
        for i in range(0,1):
            data["results"][i] = data["results"][i] + read_msg(data["results"][i][0])
        database = database + data["results"]
        time.sleep(0.1)
    set_database = []
    for data in database:
        if data not in set_database:
            set_database.append(data)
    return set_database, fields
#输出到excel
def out_file_excel(filename, database):
    print(colorama.Fore.RED + "======文档输出=======")
    field = config.get("fields", "fields").split(",")
    column_lib = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
                  13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W',
                  24: 'X', 25: 'Y', 26: 'Z'}
    workbook = xlsxwriter.Workbook(filename) ##创建xlsx文件
    worksheet = workbook.add_worksheet() #在文件中添加一个sheet1
    worksheet.set_column('A:{}'.format(column_lib[len(field)]), 30)#写几个列,如A:D,就是设置A到D单元格,这些单元格宽度为30
    #设置样式
    title_format = workbook.add_format(
        {'font_size': 14, 'border': 1, 'bold': True, 'font_color': 'white', 'bg_color': '#4BACC6',
             'align': 'center',
             'valign': 'center', 'text_wrap': True})
    content_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
    i = 1
    row = 1
    col = 0
    #第一行表头也就是ip,host等
    for column in field:
            worksheet.write('{}1'.format(column_lib[i]), column, title_format)#1控制在第一行
            i += 1
        #第一个for控制行，第二个for控制列
    for item in database:
        for n in range(len(field)):
            worksheet.write(row, col + n, item[n], content_format)
        row = row + 1
    workbook.close()
    print(colorama.Fore.GREEN + "[+] 文档输出成功！文件名为：{}".format(filename))
#非fofa接口查询域名
def read_msg(ip_test):
    ip_to_web_url = "http://ip.yqie.com/iptodomain.aspx?ip="
    try:
        res = requests.get(url=ip_to_web_url+ip_test)
        res.encoding = res.apparent_encoding
        html = res.text
        result_url = re.findall(r'<td width="90%" class="blue t_l" style="text-align: center">www\..*\.com</td>', html,
                                 re.M | re.I)
        result_url = result_url[0].strip()
        result_url = re.findall(r'www.*.com', result_url, re.M | re.I)
        return [result_url,"https://icp.chinaz.com/{}".format(result_url[0])]
    except:
        #没有域名的ip会自动跳过
        return ["None","None"]
        pass
#命令行传参
#1.添加一个解析器对象
parser = argparse.ArgumentParser(
        description="fofa采集工具")
#给这个解释器对象传参，参数名为 query,bat_query........;传参方法为 -q -bq........
#那个help是输入--help时返回的
parser.add_argument('-q', '--query', help='Fofa查询语句')
parser.add_argument('-o', '--outfile', default="fofa.xlsx", help='保存文件名,默认为fofa.xlsx')
args = parser.parse_args()#print(args.query)
#获取query的值,目的是给fofa客户端传参
query_str = args.query
filename = args.outfile
# bat_query_file = args.bat_query

# is_scan = args.nuclie
# update = args.update
# ico = args.icon_query

if query_str:
        #初始化参数
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read('user_msg.ini', encoding="utf-8")
        # 生成一个fofa客户端实例
        client = fofa_client.Client()
        # 获取账号信息
        get_userinfo()
        database, fields = get_search(query_str)
        out_file_excel(filename, database)
else:
        print("语法错误,请输入python/python3 fofa.py --help进行查询")



