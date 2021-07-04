from bs4 import BeautifulSoup#pip로 설치필요
import time
import datetime
import requests #pip로 설치필요
#pandas 관련 모듈
import pandas as pd#pip로 설치필요
import numpy as np#pip로 설치필요

#시스템 및 복사 모듈
import os
import shutil

from tendo import singleton #프로그램 중복 실행 방지 모듈 #pip로 설치 요
me = singleton.SingleInstance()#프로그램 중복 실행 방지 


def stock_check(url): #iherb의 stock check
    response = requests.get(url, headers=None)
    #print(response.headers)#웹사이트의 헤더 정보를 표시한다.
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("h1",{"itemprop":"name", "id":"name"}).get_text()
    stock_status=soup.find("div",{"id":"stock-status"}).contents[1].get_text(strip=True).replace("\n","").replace("  ","") #첫번째 있는 것이 실제 품절/재고 있음이 있는 태그
    now=datetime.datetime.now()
    nowstr=now.strftime('%m/%d %H:%M')
    return [title, stock_status, nowstr] #0:title, 1:stock_status, 2:nowstr

def save_to_csv(save_dir, save_name): #적절한 방법으로 csv로 저장
    save_file=save_dir+save_name+".csv"
    #-------원 데이터를 csv로 저장---------
    if os.path.isfile(save_file): 
        ddf=pd.read_csv(save_file, encoding="utf-8-sig", nrows=1)
        if str(ddf.columns) == str(df_stocks.columns):
            df_stocks.to_csv(save_file, mode='a', header=False, encoding="utf-8-sig", index=False)#a는 원본에 데이터를 추가해서 저장하겠다는 뜻
        else:
            df_stocks.to_csv(save_file, mode='a', header=True, encoding="utf-8-sig", index=False)
    else: #동일한 파일이 없다면
        df_stocks.to_csv(save_file, mode='a', header=True, encoding="utf-8-sig", index=False)#utf-8-sig인코딩을 사용하면 한글도 깨지지 않음
    #-------원 데이터 보호를 위해 복사본으로 저장---------
    #shutil.copy(source, destination) 으로 사용
    destination = "./" + "[재고여부확인]iherb" + ".csv"


    try:#원래는 원사본에 저장
        shutil.copy(save_file, destination)
    except Exception as e: #만약 사용자가 파일을 열어보고 있거나 오류가 발생하면
        print(e)

#===========================================================================================================================================================
urls = ['https://kr.iherb.com/pr/California-sGold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180?rcode=CYT6453',
        'https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-1-000-mg-30-Fish-Gelatin-Softgels/82845?rcode=CYT6453',
        'https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-30-Billion-CFU-60-Veggie-Capsules/64009?rec=iherbtest-home']

stocks_dic = {'time':[]}
for i in range(len(urls)):
    title = stock_check(urls[i])[0]
    stocks_dic[title]=[]

flag=True

save_dir="./dontouch/"
save_name = "original"

if not os.path.isdir(save_dir[:-1]):
    os.mkdir("./"+save_dir)

try:
    f=open("./dontouch/process_option.txt","r")
    flag = f.readline()
except:
    f=open("./dontouch/process_option.txt","w")
    f.write("True")
f.close()

print("go to mainloop")

#mainloop
while True:
    f = open("./dontouch/process_option.txt","r")
    flag = f.readline()# 첫번째 줄 읽기
    f.close()
    print("read!")
    print("flag :",flag)
    if flag == "False":
        break
    for i in range(len(urls)): #재고 확인
        title, stock_status, nowstr = stock_check(urls[i]) #list로 return되어도 각각 변수 순서대로 들어감
        print("[{}의 재고 확인]".format(title))
        print(nowstr,">>>", stock_status)
        if i == 0:
            stocks_dic['time'].append(nowstr)
        stocks_dic[title].append(stock_status)
    df_stocks= pd.DataFrame(stocks_dic)
    save_to_csv(save_dir, save_name)#csv로 저장
    time.sleep(60)
exit()
