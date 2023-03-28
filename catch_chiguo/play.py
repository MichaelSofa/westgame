import cv2 as cv
import numpy as np
import os
import sys
import time
import random
import pydirectinput
import keyboard
from keymouse import move_and_click_in_game, move_close_to
from shot_screen_func import shot
from match_template_func import get_coor
from senario_verification import auto_do_verification, model_load, load_popup_template
from check_battle_flag import BattleClass
from catch_chiguo import load_catch_and_run_template, net_load, process_one_battle_frame
from auto_guide import auto_guide, load_guide_template

loop_flag = True


def change_loop_action(x):
    global loop_flag
    a = keyboard.KeyboardEvent('down', 28, 'm')
    if x.event_type == 'down' and x.name == a.name:
        print("loop flag changed")
        loop_flag = not loop_flag


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
        # move_close_to(random.randint(left+10, right-10), random.randint(top+10, bottom-10))
        pydirectinput.moveRel(random.randint(-20, 20), random.randint(-20, 20), duration=random.random())
        # 判断是否处于战斗状态
        battle_flag = battle_class.detect_if_battle(game_frame)
        if battle_flag:  # 处于战斗状态
            result = auto_do_verification(game_frame)
            if result:  # 处于场景验证状态
                continue
            # 非场景验证状态
            process_one_battle_frame(game_frame)  # 抓宝宝或逃跑

        else:  # 处于非战斗状态(进行自动寻路)
            auto_guide(game_frame)


if __name__ == "__main__":
    main()
