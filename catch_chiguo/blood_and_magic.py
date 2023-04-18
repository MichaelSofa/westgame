import cv2 as cv
import numpy as np
import pydirectinput

from shot_screen_func import shot

person_blood_thresh = 0.3
pet_blood_thresh = 0.3
person_magic_thresh = 0.5
pet_magic_thresh = 0.3

person_restore_key = "f5"
pet_restore_key = "f6"


def def detect_blood_magic(image):
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
    blood_magic_result = detect_blood_magic(image)
    if blood_magic_result is not None:
        person_blood_state, pet_blood_state, person_magic_state, pet_magic_state = blood_magic_result
        if person_blood_state < person_blood_thresh or person_magic_state < person_magic_thresh:
            pydirectinput.press(person_restore_key)
        if pet_blood_state < pet_blood_thresh or pet_magic_state < pet_magic_thresh:
            pydirectinput.press(pet_restore_key)
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