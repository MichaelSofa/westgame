import cv2 as cv
import numpy as np
import os
import sys
import time
from keymouse import move_and_click_in_game, move_close_to
from shot_screen_func import shot
from match_template_func import get_coor
from senario_verification import auto_do_verification, model_load, load_popup_template
from check_battle_flag import BattleClass
from catch_chiguo import load_catch_and_run_template, net_load, process_one_battle_frame
from auto_guide import auto_guide, load_guide_template


def main():
    # 预加载各种模板
    load_popup_template()
    load_catch_and_run_template()
    model_load()
    net_load()
    battle_class = BattleClass()
    battle_class.init_bar_vector()
    load_guide_template()
    # 进入死循环
    while True:
        # 截取一帧游戏图像
        result = shot()
        if result is None:
            print("mhxy game is not running!")
            continue
        game_frame, _, _, _, _ = result
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
