from tkinter import *
import tkinter.messagebox as msgbox
from tkinter import filedialog

import os
import time
from threading import * #멀티스레드를 가능하게 해주는 모듈


root=Tk()
root.title("iherb 상품 재고 크롤링")

start_stop_frame = Frame(root)
start_stop_frame.pack(side="bottom")

def start_crawl():
    print("start!")    
    Thread(target=thread).start()

def thread():
    f = open("./dontouch/process_option.txt","w")
    f.write("True")
    f.close()
    try:
        msgbox.showinfo("알림", "크롤링을 시작합니다.")
        print("nstart")
        os.system("pythonw ./start_crawling.py")
    except Exception as e:
        msgbox.showwarning("예외발생", e)# 알림메세지 생성
    print("done!")

#시작버튼
btn_start = Button(start_stop_frame, text="start!", padx=50, pady=10, command=start_crawl)
btn_start.pack(side="left", expand=True)

def stop_crawl(): 
    print("stop!")
    Thread(target=kill_thread).start()
    msgbox.showinfo("알림", "크롤링을 중지했습니다!")# 알림메세지 생성

def kill_thread():
    f = open("./dontouch/process_option.txt","w")
    f.write("False")
    f.close()
    print("stopped!")
#멈춤버튼
btn_stop = Button(start_stop_frame, text="stop!", padx=50, pady=10, command=stop_crawl)
btn_stop.pack(side="right", expand=True)


#해당 디렉토리가 없다면 만들기
save_dir = "./dontouch"

if not os.path.isdir(save_dir): 
    os.mkdir(save_dir)

root.mainloop()
