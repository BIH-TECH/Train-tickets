import requests
import re
from pprint import pprint 


def main():
    url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042"
    r = requests.get(url, verify = False)
    patter = u"([\u4e00-\u9fa5]+)\|([A-Z]+)"
    result = re.findall(patter, r.text) 
    result = dict(result)
   # pprint(dict(result), indent = 4)     
    print(result.keys())
    print(result.values())




if __name__ == "__main__":
    main()

