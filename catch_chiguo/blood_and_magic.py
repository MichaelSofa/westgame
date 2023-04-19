import cv2 as cv
import numpy as np
import pydirectinput
import random
import time

from shot_screen_func import shot
from match_template_func import get_coor
from keymouse import do_mouse_action

person_blood_thresh = 0.3
pet_blood_thresh = 0.3
person_magic_thresh = 0.5
pet_magic_thresh = 0.3

person_restore_key = "f6"
pet_restore_key = "f5"

template_panda = cv.imread("./blood_magic_template/panda.png", 0)
template_change = cv.imread("./blood_magic_template/change.png", 0)
template_xiuxi = cv.imread("./blood_magic_template/xiuxi.png", 0)
template_xiuxi2 = cv.imread("./blood_magic_template/xiuxi2.png", 0)
template_xiuxi3 = cv.imread("./blood_magic_template/xiuxi3.png", 0)




def detect_blood_magic(image):
    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    varify_blood_flag = (image_hsv[66, -13, 1] == 255)
    varify_magic_flag = (image_hsv[78, -13, 1] == 255)
    #print("varify_magic_flag: ", image_hsv[78, -13, 1])
    #print("varify_blood_flag: ", image_hsv[66, -13, 1])
    if varify_blood_flag and varify_magic_flag:
        person_blood_s = image_hsv[66, -59:-14, 1]
        pet_blood_s = image_hsv[66, -179:-134, 1]
        person_magic_s = image_hsv[78, -59:-14, 1]
        pet_magic_s = image_hsv[78, -179:-134, 1]
        # print(person_blood_s)
        # print(pet_blood_s)
        # print(person_magic_s)
        # print(pet_magic_s)
        person_blood_state = np.sum(person_blood_s >= 150 )/45
        pet_blood_state = np.sum(pet_blood_s >= 150 )/45
        person_magic_state = np.sum(person_magic_s >= 150 )/45
        pet_magic_state = np.sum(pet_magic_s >= 150 )/45
        return person_blood_state, pet_blood_state, person_magic_state, pet_magic_state
    
    
def do_auto_restore_blood_magic():
    result = shot()
    if result is None:
        return
    image, left, top, right, bottom = result
    pet_result = get_coor(image, template_panda, 0.9)
    if pet_result is not None:
        pet_flag = False
    else:
        pet_flag = True
    blood_magic_result = detect_blood_magic(image)
    if blood_magic_result is not None:
        person_blood_state, pet_blood_state, person_magic_state, pet_magic_state = blood_magic_result
        if person_blood_state < person_blood_thresh or person_magic_state < person_magic_thresh:
        # if True:
            pydirectinput.press(person_restore_key)
            time.sleep(0.5+random.random()/5)
            result = shot()
            if result is not None:
                image, left, top, right, bottom = result
                change_result = get_coor(image, template_change, 0.9)
                if change_result is not None:
                    (left_top, right_bottom) = change_result
                    center_x = int((left_top[0] + right_bottom[0])/2)
                    center_y = int((left_top[1] + right_bottom[1])/2)
                    for try_i in range(10):
                        return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y)
                        # return_flag = do_mouse_action(center_x, center_y)
                        if return_flag:
                            break
            time.sleep(0.5+random.random()/5)
            result = shot()
            if result is not None:
                image, left, top, right, bottom = result
                xiuxi_result = get_coor(image, template_xiuxi, 0.9)
                if xiuxi_result is not None:
                    (left_top, right_bottom) = xiuxi_result
                    # time.sleep(0.5+random.random())
                    center_x = int((left_top[0] + right_bottom[0])/2)
                    center_y = int((left_top[1] + right_bottom[1])/2)
                    for try_i in range(10):
                        return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y)
                        # return_flag = do_mouse_action(center_x, center_y)
                        if return_flag:
                            break
            
        if pet_flag:
            if pet_blood_state < pet_blood_thresh or pet_magic_state < pet_magic_thresh:
                pydirectinput.press(pet_restore_key)
                time.sleep(0.5+random.random()/5)
                result = shot()
                if result is not None:
                    image, left, top, right, bottom = result
                    change_result = get_coor(image, template_change, 0.9)
                    if change_result is not None:
                        (left_top, right_bottom) = change_result
                        center_x = int((left_top[0] + right_bottom[0])/2)
                        center_y = int((left_top[1] + right_bottom[1])/2)
                        for try_i in range(10):
                            return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y+random.randint(-1, 1))
                            if return_flag:
                                break
                                
                time.sleep(0.5+random.random()/5)
                result = shot()
                if result is not None:
                    image, left, top, right, bottom = result
                    xiuxi_result = get_coor(image, template_xiuxi3, 0.9)
                    if xiuxi_result is not None:
                        (left_top, right_bottom) = xiuxi_result
                        center_x = int((left_top[0] + right_bottom[0])/2)
                        center_y = int((left_top[1] + right_bottom[1])/2)
                        for try_i in range(10):
                            return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y+random.randint(-1, 1))
                            if return_flag:
                                break
    else:
        print("not in game main scene!")

if __name__ == "__main__":
    image = cv.imread("cut.png")
    blood_magic_result = detect_blood_magic(image)
    if blood_magic_result is not None:
        person_blood_state, pet_blood_state, person_magic_state, pet_magic_state = blood_magic_result
        print(person_blood_state, pet_blood_state, person_magic_state, pet_magic_state)
    
    '''
    while True:
        time.sleep(10)
        do_auto_restore_blood_magic()
    '''