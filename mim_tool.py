import pyautogui
import cv2
import pytesseract
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import asyncio
import threading

import mimmim_sys
'''
MOUSE FUNCTION
'''


'''
TELEGRAM FUNCTION
'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def call_teleBot(sending_message,api_key, user_id):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(send_msg(message=sending_message,api_key=api_key, user_id=user_id)) #봇 실행하는 코드


async def send_msg(message,api_key, user_id): #실행시킬 함수명 임의지정
    bot = Bot(token=api_key)
    await bot.send_message( user_id,message)


'''
IMAGE FUNCTION
'''
def check_success(check_msg):
    img_text=extract_text()
    
    if check_msg in img_text:
        return True
    else:
        return False

def extract_text():
    pyautogui.screenshot("test.jpg")

    img=cv2.imread('test.jpg')

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    text=pytesseract.image_to_string(gray,lang="kor+eng")
    
    return text

'''
DISPLAY FUNCTION
'''

def show_prog_state(show_label,count_var,prog_type):
    if count_var==0 or count_var==1:
        show_label.setText(prog_type)
    elif count_var==2 or count_var==3:
        show_label.setText(prog_type+".")
    elif count_var==4 or count_var==5:
        show_label.setText(prog_type+"..")
    elif count_var==6 or count_var==7:
        show_label.setText(prog_type+"...")
