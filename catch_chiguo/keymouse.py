# -*- coding: utf-8 -*-
# 说明：加入了一定程度的随机算法，但是仅仅是随机算法，没有模拟人类鼠标轨迹。存在被封的风险。
# 说明：必须调用管理员权限运行程序

import cv2 as cv
import numpy as np
import os
#import pyautogui
import pydirectinput
import random
import time
from shot_screen_func import shot

#pyautogui.PAUSE = random.random()/3
#pyautogui.FAILSAFE = False           # 启用自动防故障功能
pydirectinput.PAUSE = random.random()/3
pydirectinput.FAILSAFE = False           # 启用自动防故障功能

## 鼠标形状偏移
mouse_move_shape = (8,8)

template = cv.imread("cursor.png")

'''
def find_mouse_in_desktop(img, template):
    h, w = template.shape[0:2]
    threshold = 0.85
    res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    left_top = max_loc  # 左上角
    right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    if len(loc[0]) > 0:
        # 找到目标图片返回图片当前坐标
        return (left_top, right_bottom)
'''

def find_mouse_in_game(img, template):
    # h, w = template.shape[0:2]
    threshold = 0.85
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    left_top = max_loc  # 左上角
    # right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    if len(loc[0]) > 0:  # 返回鼠标的尖端点相对于图像的坐标
        return left_top[0]-mouse_move_shape[0], left_top[1] - mouse_move_shape[1]


"""
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
"""
    
def move_and_click_in_game(x, y):  # 加入随机算法而不是直接直线移动
    step = 10
    result = shot()
    if result is not None:
        img, left, top, right, bottom = result
    else:
        print("not find game picture! 1")
        return False
    mouse_result = find_mouse_in_game(img, template)
    if mouse_result is None:
        print("not find mouse! 1")
        return False
    else:
        x_dist = x - mouse_result[0]
        y_dist = y - mouse_result[1]
        # print("initial x_dist, y_dist: {} {}".format(x_dist, y_dist))
        for i in range(1, step+1):  # 制造移动轨迹的随机性
            random_number1 = random.random()
            random_number2 = random.random()
            random_number_x = 0.5*random_number1
            random_number_y = min(0.5, max(0, random_number_x + (random_number2-0.5)*0.2))
            #this_move_x = int(x_dist*0.5*random.random())
            #this_move_y = int(y_dist*0.5*random.random())
            this_move_x = int(x_dist*random_number_x)
            this_move_y = int(y_dist*random_number_y)
            pydirectinput.moveRel(this_move_x, this_move_y, duration=random.random()/step) #, relative=True)
            x_dist = x_dist - this_move_x
            y_dist = y_dist - this_move_y
            # print("x_dist, y_dist: {} {}".format(x_dist, y_dist))
        
        # 开始点击
        result = shot()
        if result is None:
            print("not find game picture! 2")
            return False
        img, left, top, right, bottom = result
        mouse_result = find_mouse_in_game(img, template)
        if mouse_result is None:
            print("not find the mouse! 2")
            return False
        else:
            time.sleep(random.random()/3)
            # move_rel_and_click(x-mouse_result[0], y-mouse_result[1])
            pydirectinput.moveRel(x-mouse_result[0], y-mouse_result[1], duration=random.random()/3) #, relative=True)
            time.sleep(random.random()/5)
            pydirectinput.click()
            return True

def move_close_to(x, y):  # 加入随机算法的将鼠标移动靠近目标
    step = 10
    result = shot()
    if result is not None:
        img, left, top, right, bottom = result
    else:
        print("not find game picture! 1")
        return False
    x_mouse, y_mouse = pydirectinput.position()
    x_mouse = x_mouse - left
    y_mouse = y_mouse - top
    x_dist = x - x_mouse
    y_dist = y - y_mouse
    # print("initial x_dist, y_dist: {} {}".format(x_dist, y_dist))
    for i in range(1, step+1):  # 制造移动轨迹的随机性
        random_number1 = random.random()
        random_number2 = random.random()
        random_number_x = 0.5*random_number1
        random_number_y = min(0.5, max(0, random_number_x + (random_number2-0.5)*0.2))
        #this_move_x = int(x_dist*0.5*random.random())
        #this_move_y = int(y_dist*0.5*random.random())
        this_move_x = int(x_dist*random_number_x)
        this_move_y = int(y_dist*random_number_y)
        pydirectinput.moveRel(this_move_x, this_move_y, duration=random.random()/step) #, relative=True)
        x_dist = x_dist - this_move_x
        y_dist = y_dist - this_move_y
        # x_test, y_test = pydirectinput.position()
        # print("x_dist, y_dist: {} {}".format(x_dist, y_dist))
        # print("x_test, y_test: {} {}".format(x_test, y_test))
        
    return True


if __name__ == '__main__' : 
    '''
    time.sleep(2)
    move_rel_and_click(111, 44)
    time.sleep(1)
    move_to_and_click(640, 640)
    time.sleep(1)
    '''
    '''
    # template = cv.imread("cursor.png")
    picture = cv.imread("7.png")
    t1 = time.time()
    result = find_mouse_in_game(picture, template)
    t2 = time.time()
    print("spend time: ", t2 - t1)
    if result is not None:
        print(result)
        cv.rectangle(picture, result, (result[0]+10, result[1]+10), (0, 0, 255), 1)
        cv.imshow('show', picture)
        cv.waitKey()
        cv.destroyAllWindows()
    
    time.sleep(2)
    print(pydirectinput.position())
    '''
    # excute_flag = move_and_click_in_game(1600, 300)
    excute_flag = move_close_to(200, 200)
    print("excute_flag: ", excute_flag)
        
    
