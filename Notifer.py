#coding:UTF-8
import os
import requests
import EnviromentVar as envi
def output(strings: str,how=envi.OUTPUT_MODE):
    if(how=='print'):
        print(strings)
    elif(how=='LINEnotify'):
        print(strings)
        url='https://notify-api.line.me/api/notify'
        token=envi.LINENOTIFY_TOKEN
        headders={'Authorization':'Bearer '+token}
        message=strings
        payload={'message':message}
        res=requests.post(url,data=payload,headers=headders)
        print(f'LINENotify:{res}')
