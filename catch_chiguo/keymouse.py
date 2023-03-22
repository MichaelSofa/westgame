# -*- coding: utf-8 -*-
# 说明：这个没有模拟人类操作，只能简单实现移动和点击，使用这个绝对会被封，需要更改！！！！！
# 说明：必须调用管理员权限运行程序

import os
#import pyautogui
import pydirectinput
import random
import time

#pyautogui.PAUSE = random.random()/3
#pyautogui.FAILSAFE = False           # 启用自动防故障功能
pydirectinput.PAUSE = random.random()/3
pydirectinput.FAILSAFE = False           # 启用自动防故障功能

def move_to(x,y):
    print(f'move to - > {(x,y)}')
    #pyautogui.moveTo(x,y,duration=random.random()/2)
    pydirectinput.moveTo(x,y,duration=random.random()/2)

def move_rel(x,y):
    print(f'move rel - > {(x,y)}')
    #pyautogui.moveRel(x,y,duration=random.random()/2)
    pydirectinput.moveRel(x,y,duration=random.random()/2, relative=True)

def move_to_and_click(x, y):
    move_to(x, y)
    time.sleep(random.random()/5)
    # pyautogui.click()
    pydirectinput.click()

def move_rel_and_click(x, y):
    move_rel(x, y)
    time.sleep(random.random()/5)
    # pyautogui.click()
    pydirectinput.click()
    

if __name__ == '__main__' : 
    time.sleep(2)
    move_rel_and_click(111, 44)
    time.sleep(1)
    move_to_and_click(640, 640)
    time.sleep(1)