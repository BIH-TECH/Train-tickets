# -*- coding: utf-8 -*-

'''命令行火車票查看器

Usage:
    tickets <from> <to> <date>

Example:
    tickets 北京 上海 2018-2-1
   
'''
from docopt import docopt
import stations
import requests
from prettytable import PrettyTable as pt
from colorama import Fore
               
           

def cli():

    arguments = docopt(__doc__, version='Tickets 1.0')  #實例化命令行參數
    from_station = stations.get_code(arguments.get("<from>")) #得到命令行輸入起始站的編號
    to_station = stations.get_code(arguments.get("<to>"))   #得到命令行輸入終點站編號
    date = arguments.get("<date>")   #得到輸入日期

    url = ("https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT").format(date, from_station, to_station) #將上述參數放進 url
    try:
        r = requests.get(url, verify = False, timeout = 100, headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"}, allow_redirects = False)   #請求 url
        r.raise_for_status()
    except:
        print("error!")

    raw_trains = r.json()["data"]["result"]   #將json數據改爲列表 
      
  
       #設定prettytable格式

    x = pt("車次 起始站/終點站 發車時刻/行車時間 歷時 一等座 二等坐 軟臥 硬臥 硬座 無坐".split(" "))
    x.align[""] = "|"
    x.padding_width = 1


         

        #從 json文件中解析數據

    for raw_train in raw_trains:
        data_list = raw_train.split("|")
        train_number = data_list[3]
        from_station_code = data_list[6]
        to_station_code = data_list[7]
        start_time = data_list[8]
        arrive_time = data_list[9]
        time_duration = data_list[10]
        first_seat = data_list[31] or "--"
        second_seat = data_list[30] or "--" 
        soft_bed =data_list[23] or "--"
        hard_bed =data_list[28] or "--"
        hard_seat = data_list[29] or "--"    
        no_seat = data_list[33] or "--"
        


       
        #向  prettytable 中填充數據
        
        x.add_row([Fore.BLUE + train_number + Fore.RESET,"\n".join([Fore.GREEN + stations.get_name(from_station_code) + Fore.RESET ,Fore.RED + stations.get_name(to_station_code) + Fore.RESET]),"\n".join([Fore.GREEN + start_time + Fore.RESET, Fore.RED + arrive_time + Fore.RESET]), time_duration,Fore.YELLOW + first_seat,second_seat,soft_bed,hard_bed , hard_seat,no_seat + Fore.RESET])

    print(x)

if __name__ == '__main__':

    cli()

