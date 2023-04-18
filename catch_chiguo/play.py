import cv2 as cv
import numpy as np
import os
import sys
import time
import random
import pydirectinput
import keyboard
from keymouse import do_mouse_action
from shot_screen_func import shot
from match_template_func import get_coor
from senario_verification import auto_do_verification, model_load, load_popup_template
from check_battle_flag import BattleClass
from catch_chiguo import load_catch_and_run_template, net_load, process_one_battle_frame
from auto_guide import auto_guide, load_guide_template
from multi_window import to_primary_window, switch_window
from blood_and_magic import do_auto_restore_blood_magic

loop_flag = True
fight_flag = True


def change_loop_action(x):
    global loop_flag, fight_flag
    a = keyboard.KeyboardEvent('down', 28, 'm')
    b = keyboard.KeyboardEvent('down', 28, 'f')
    if x.event_type == 'down' and x.name == a.name:
        print("loop flag changed")
        loop_flag = not loop_flag
    elif x.event_type == 'down' and x.name == b.name:
        print("fight flag changed")
        fight_flag = not fight_flag


def main():
    # 预加载各种模板
    load_popup_template()
    load_catch_and_run_template()
    model_load()
    net_load()
    battle_class = BattleClass()
    battle_class.init_bar_vector()
    load_guide_template()
    keyboard.hook(change_loop_action)
    # 进入死循环
    while True:
        # 是否循环的判断
        if not loop_flag:
            continue
        # 截取一帧游戏图像
        result = shot()
        if result is None:
            print("mhxy game is not running!")
            continue
        game_frame, left, top, right, bottom = result
        # 开始前加入一次随机移动
        pydirectinput.moveRel(random.randint(-30, 30), random.randint(-30, 30))
        # 判断是否处于战斗状态
        battle_flag = battle_class.detect_if_battle(game_frame)
        if battle_flag:  # 处于战斗状态
            need_check = True
            result = auto_do_verification()
            if result:  # 处于场景验证状态
                continue
            # 非场景验证状态
            process_one_battle_frame(fight_flag)  # 抓宝宝或逃跑/抓宝宝或战斗
            switch_window()  # 切换多开窗口功能

        else:  # 处于非战斗状态加血加蓝或进行自动寻路
            if need_check:
                do_auto_restore_blood_magic()  # 每个窗口的人物和宝宝分别检查和实现加血加蓝
                need_check = False
            else:
                to_primary_window()  # 确保处于第一个窗口，如果不在就点击到第一个窗口
                auto_guide()  # 进行自动点击小地图


if __name__ == "__main__":
    main()
