import requests
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
import os
import datetime

# 현재 시간
# current = datetime.datetime.now()
# print(current)
# current_time = current.replace(microsecond=0)
# print(current_time)

# 파일 위치에 엑셀파일 생성.
wb = openpyxl.Workbook() #workbook 생성
path = os.getcwd()
new_filename = path+'/result.xlsx'
wb.save(new_filename)

# 리스트 생성
# url_list = []
url_list = ['https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180?rcode=CYT6453',
'https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-1-000-mg-30-Fish-Gelatin-Softgels/82845?rcode=CYT6453',
'https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-30-Billion-CFU-60-Veggie-Capsules/64009?rec=iherbtest-home']
stock_list = []
time_list = []
# 먼저 3 개의 url
# https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180?rcode=CYT6453
# https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-1-000-mg-30-Fish-Gelatin-Softgels/82845?rcode=CYT6453
# https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-30-Billion-CFU-60-Veggie-Capsules/64009?rec=iherbtest-home

# url 입력받기
# for i in range (3):
#     input_url = input("url 입력")
#     url_list.append(input_url)

#재고 o
#stock-status > strong
#stock-status
# url = 'https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-5-Billion-CFU-10-Veggie-Capsules/64008' 

#재고x
#stock-status > div.text-danger.stock-status-text
#stock-status
# url1 = 'https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180'

# 재고유무 확인
for url in url_list:
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select_one('#stock-status')
        text = title.get_text()
        val = "품절" in text
        if val:
            stock_list.append("재고 X")
        else:
            stock_list.append("재고 O")
        
        current = datetime.datetime.now()
        current_time = current.replace(microsecond=0)
        time_list.append(current_time)
    
    else:
        print(response.status_code)

print(stock_list)
print(time_list)

dataframe = pd.DataFrame({
    'Time':time_list, 'url': url_list,'stock':stock_list
})

dataframe