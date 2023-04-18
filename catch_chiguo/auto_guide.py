import cv2 as cv
import numpy as np
import pydirectinput
import random
from match_template_func import get_coor
from keymouse import do_mouse_action
from shot_screen_func import shot
import time

red_dot_path = './auto_guide_template/red_dot.png'
xumi_path = './auto_guide_template/xumi.png'

template_red_rot = None
template_xumi = None

goal_point1 = [96, 87]  # 与须弥东界左上角点的相对距离
goal_point2 = [32, 346]  # 与须弥东界左上角点的相对距离
goal_index = 0  # 0表示上方的点 1表示下方的点


def calc_dist(pt1, pt2):
    return abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


def load_guide_template():
    global template_xumi
    global template_red_rot
    template_xumi = cv.imread(xumi_path, 0)
    template_red_rot = cv.imread(red_dot_path, 0)


def auto_guide():
    global goal_index
    result = shot()
    if result is None:
        return
    image, left, top, right, bottom = result
    result_xumi = get_coor(image, template_xumi, 0.8)
    if result_xumi is None:
        pydirectinput.press('tab')
    else:
        left_top, right_bottom = result_xumi
        real_goal_pt1 = (left_top[0] + goal_point1[0], left_top[1] + goal_point1[1])
        real_goal_pt2 = (left_top[0] + goal_point2[0], left_top[1] + goal_point2[1])
        result_red_pot = get_coor(image, template_red_rot, 0.8)
        if result_red_pot is not None:
            red_left_top, red_right_bottom = result_red_pot
            if goal_index == 0:
                dist = calc_dist(red_left_top, real_goal_pt1)
                if dist < 50:
                    goal_index = 1
            elif goal_index == 1:
                dist = calc_dist(red_left_top, real_goal_pt2)
                if dist < 50:
                    goal_index = 0

            if goal_index == 0:
                time.sleep(random.random()*2)
                do_mouse_action(real_goal_pt1[0]+random.randint(-6, 6), real_goal_pt1[1]+random.randint(-6, 6))
                
            elif goal_index == 1:
                time.sleep(random.random()*2)
                do_mouse_action(real_goal_pt2[0]+random.randint(-6, 6), real_goal_pt2[1]+random.randint(-6, 6))


