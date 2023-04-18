# -*- coding: utf-8 -*-
# 说明：加入了一定程度的随机算法，但是仅仅是随机算法，没有模拟人类鼠标轨迹。存在被封的风险。
# 说明：必须调用管理员权限运行程序

import cv2 as cv
import numpy as np
import os
import pydirectinput
import random
import time
from shot_screen_func import shot
from match_template_func import get_coor


pydirectinput.PAUSE = random.random()/100
pydirectinput.FAILSAFE = False           # 启用自动防故障功能

## 鼠标形状偏移
mouse_move_shape = (8,8)

template = cv.imread("cursor.png")


def find_mouse_in_game(img, template):
    # h, w = template.shape[0:2]
    threshold = 0.8
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    left_top = max_loc  # 左上角
    # right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
    if len(loc[0]) > 0:  # 返回鼠标的尖端点相对于图像的坐标
        return left_top[0] - mouse_move_shape[0], left_top[1] - mouse_move_shape[1]


def move_and_click_in_game(x, y):  # 加入随机算法而不是直接直线移动
    step = 5
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
        for i in range(1, step+1):  # 制造移动轨迹的随机性
            random_number1 = random.random()
            random_number2 = random.random()
            random_number_x = 0.5*random_number1
            random_number_y = min(0.5, max(0, random_number_x + (random_number2-0.5)*0.2))
            this_move_x = int(x_dist*random_number_x)
            this_move_y = int(y_dist*random_number_y)
            pydirectinput.moveRel(this_move_x, this_move_y)
            x_dist = x_dist - this_move_x
            y_dist = y_dist - this_move_y
        
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
            time.sleep(random.random()/100)
            pydirectinput.moveRel(x-mouse_result[0], y-mouse_result[1])
            time.sleep(random.random()/5)
            pydirectinput.click()
            return True


def move_close_to(x, y):  # 加入随机算法的将鼠标移动靠近目标
    step = 4
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
    for i in range(1, step):  # 制造移动轨迹的随机性
        random_number1 = random.random()
        random_number2 = random.random()
        random_number_x = 0.5*random_number1
        random_number_y = min(0.5, max(0, random_number_x + (random_number2-0.5)*0.2))
        this_move_x = int(x_dist*random_number_x)
        this_move_y = int(y_dist*random_number_y)
        pydirectinput.moveRel(this_move_x, this_move_y)
        x_dist = x_dist - this_move_x
        y_dist = y_dist - this_move_y
    pydirectinput.moveRel(x_dist, y_dist)
    return True


def do_mouse_action(x, y):  # 以上两个函数的合并
    flag1 = move_close_to(x, y)
    flag2 = move_and_click_in_game(x, y)
    ret_flag = flag1 and flag2
    return ret_flag

def do_windows_mouse_action(x, y):  # 直接操控windows鼠标
    flag1 = move_close_to(x, y)
    result = shot()
    if result is not None:
        img, left, top, right, bottom = result
        x_mouse, y_mouse = pydirectinput.position()
        time.sleep(random.random()/100)
        pydirectinput.moveRel(x-x_mouse+left, y-y_mouse+top)
        time.sleep(random.random()/5)
        pydirectinput.click()
        flag2 = True
    else:
        flag2 = False
    ret_flag = flag1 and flag2
    return ret_flag

def do_press_alt_key(key_name):  # 按alt+key_name组合键
    pydirectinput.keyDown('alt')
    pydirectinput.press(key_name)
    pydirectinput.keyUp('alt')

if __name__ == '__main__' : 
    # excute_flag = move_and_click_in_game(1600, 300)
    # excute_flag = move_close_to(200, 200)
    # excute_flag = do_mouse_action(1033, 520)
    
    # excute_flag = do_mouse_action(1233, 720)
    # print("excute_flag: ", excute_flag)
    
    # time.sleep(1)
    # do_press_alt_key('a')
    # time.sleep(1)
    # pydirectinput.press("f12")
    # template_button = cv.imread(r"C:\Users\HP\Desktop\Screenshot 2023-04-16 093842.png", 0)
    # template_button = cv.imread(r"C:\Users\HP\Desktop\Screenshot 2023-04-16 093857.png", 0)
    template_button = cv.imread(r"C:\Users\HP\Desktop\Screenshot 2023-04-16 101027.png", 0)
    
    result = shot()
    if result is not None:
        img, left, top, right, bottom = result
        result2 = get_coor(img, template_button, 0.8)
        if result2 is not None:
            (left_top, right_bottom) = result2
            center_x = int((left_top[0]+right_bottom[0])/2)
            center_y = int((left_top[1]+right_bottom[1])/2)
            for i in range(10):
                return_flag = do_mouse_action(center_x, center_y)
                if return_flag:
                    break
            # do_windows_mouse_action(center_x, center_y)
            
