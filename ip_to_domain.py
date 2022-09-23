import re

import requests


def read_msg(ip_test):
    ip_to_web_url = "http://ip.yqie.com/iptodomain.aspx?ip=49.234.227.88"
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