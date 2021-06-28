import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime #날짜
import time # 일정시간 반복
import openpyxl

# 텍스트 파일 생성 or 불러와서 urls 리스트에 추가
# urls 리스트 생성
urls = []
try:
    with open('url.txt', 'r') as file:
        for line in file:
            urls.append(line.strip('\n'))
    
except:
    f = open("url.txt", 'w', encoding="UTF8")
    f.close()
    print("생성된 url.txt 파일에 하나의 url을 입력하고 엔터를 반복한 후 다시 실행해주세요")

# 열너비 조절

# def AutoFitColumnSize(worksheet, columns=None, margin=2):
#     for i, column_cells in enumerate(worksheet.columns):
#         is_ok = False
#         if columns == None:
#             is_ok = True
#         elif isinstance(columns, list) and i in columns:
#             is_ok = True
            
#         if is_ok:
#             length = max(len(str(cell.value)) for cell in column_cells)
#             worksheet.column_dimensions[column_cells[0].column_letter].width = length + margin

#     return worksheet

# 리스트 생성

# url_list = []
# 먼저 3 개의 url
# https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180?rcode=CYT6453
# https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-1-000-mg-30-Fish-Gelatin-Softgels/82845?rcode=CYT6453
# https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-30-Billion-CFU-60-Veggie-Capsules/64009?rec=iherbtest-home
# ================================
# url_list = ['https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-Triglyceride-Form-1000-mg-90-Fish-Gelatin-Softgels/85180?rcode=CYT6453',
# 'https://kr.iherb.com/pr/California-Gold-Nutrition-Omega-800-Pharmaceutical-Grade-Fish-Oil-80-EPA-DHA-1-000-mg-30-Fish-Gelatin-Softgels/82845?rcode=CYT6453',
# 'https://kr.iherb.com/pr/California-Gold-Nutrition-LactoBif-Probiotics-30-Billion-CFU-60-Veggie-Capsules/64009?rec=iherbtest-home']

#=============================================
# stock_list = []
# time_list = []
# name_list = []

# # 재고유무 확인

# while True:
#     for url in urls:
#         response = requests.get(url)

#         if response.status_code == 200 :
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')
#             title = soup.select_one('#stock-status')
#             text = title.get_text()
#             val = "품절" in text
#             if val:
#                 stock_list.append("재고 X")
#             else:
#                 stock_list.append("재고 O")
            
            
#             current = datetime.datetime.now()
#             current_time = current.strftime('%Y-%m-%d %H:%M') #current.replace(microsecond=0)
#             time_list.append(str(current_time))
#             name = soup.select_one('#name')
#             name_text = name.get_text()
#             name_list.append(name_text)

#         else:
#             print(response.status_code)
#             print("비정상적인 접근")

#     dataframe = pd.DataFrame({
#         'Time':time_list, 'name': name_list,'stock':stock_list
#     })

#     print(dataframe)

#     dataframe.to_excel('stocklist.xlsx')

#     time.sleep(60)
#============================== NEW
# Excel 구조잡기

#첫리스트에 어떤 값이 올지 모름
for i in range(len(urls)):
    response = requests.get(urls[i])
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.select_one('#name')
        name_text = name.get_text()
        print(name_text)
        wb = openpyxl.Workbook()
        ws = wb.active
        # sheet이름에 특수문자 불가.
        if "\/*[]:?" in name_text:
            pass #지워주기
        if i == 0 :
            ws.append(["날짜/시간", "재고"])
            ws.title = name_text
        else:
            new_sheet = wb.create_sheet(name_text)
            new_sheet.append(["날짜/시간", "재고"])
    else:
        print("excel 구조 형성에서의 response status_code 오류")

wb.save("newstock.xlsx")
# 재고유무 확인

# while True:
#     for url in urls:
#         response = requests.get(url)

#         if response.status_code == 200 :
#             html = response.text
#             soup = BeautifulSoup(html, 'html.parser')

#             name = soup.select_one('#name')
#             name_text = name.get_text()
#             #name_list.append(name_text)
#             title = soup.select_one('#stock-status')
#             text = title.get_text()
#             val = "품절" in text
#             if val:
#                 print()
#                 #stock_list.append("재고 X")
#             else:
#                 #stock_list.append("재고 O")
            
            
#             current = datetime.datetime.now()
#             current_time = current.strftime('%Y-%m-%d %H:%M') #current.replace(microsecond=0)
#             #time_list.append(str(current_time))


#         else:
#             print(response.status_code)
#             print("비정상적인 접근")

#     time.sleep(60)