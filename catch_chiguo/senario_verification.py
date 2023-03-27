import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2 as cv
import os
import random

from match_template_func import get_coor
from keymouse import move_and_click_in_game, move_close_to

model = None
IMG_HEIGHT = 100
IMG_WIDTH = 100

popup_path = './popup'
model_path = './model/mhxy.h5'
template_popup_list = []


def load_popup_template():
    template_popup_list.clear()
    popup_pics = os.listdir(popup_path)
    for i in range(len(popup_pics)):
        popup_pic = popup_pics[i]
        template_popup = cv.imread(os.path.join(popup_path, popup_pic), 0)
        template_popup_list.append(template_popup)


def model_load():
    global model
    model = keras.models.load_model(model_path)
    model.summary()


def preprocess_image(image):  # 输入numpy图像
    image = tf.convert_to_tensor(image, dtype=tf.float32)
    image = tf.image.resize(image, [IMG_WIDTH, IMG_HEIGHT])
    image /= 255.0  # normalize to [0,1] range
    return image


def model_predict(image1, image2, image3, image4):
    global model
    image1 = preprocess_image(image1)
    image2 = preprocess_image(image2)
    image3 = preprocess_image(image3)
    image4 = preprocess_image(image4)
    imgs = [image1, image2, image3, image4]
    imgs =  tf.convert_to_tensor(imgs)
    predictions = model.predict(imgs)
    predictions = [row[0] for row in predictions]
    print(predictions)
    min_index = predictions.index(min(predictions))
    print(f' 预测结果为 第 > {min_index + 1} < 张图片')
    return min_index


def detect_verification_point(image):
    result = None
    for i in range(len(template_popup_list)):
        template = template_popup_list[i]
        result = get_coor(image, template, 0.8)
        if result is not None:
            break
    if result is not None:
        left_top, right_bottom = result
        window_left = left_top[0] - 85
        window_top = left_top[1] - 8
        x1 = window_left
        x2 = window_left + 90
        x3 = x2 + 90
        x4 = x3 + 90
        x5 = x4 + 90
        image1 = image[window_top + 40: window_top + 167, x1:x2 + 1]
        image2 = image[window_top + 40: window_top + 167, x2:x3 + 1]
        image3 = image[window_top + 40: window_top + 167, x3:x4 + 1]
        image4 = image[window_top + 40: window_top + 167, x4:x5 + 1]
        min_index = model_predict(image1, image2, image3, image4)
        if min_index == 0:
            return x1 + 45, window_top + 100
        elif min_index == 1:
            return x2 + 45, window_top + 100
        elif min_index == 2:
            return x3 + 45, window_top + 100
        elif min_index == 3:
            return x4 + 45, window_top + 100
        else:
            return None


def auto_do_verification(image):
    detect_result = detect_verification_point(image)
    if detect_result is not None:
        click_x, click_y = detect_result
        move_close_to(click_x+random.randint(-5, 5), click_y+random.randint(-5, 5))
        move_and_click_in_game(click_x+random.randint(-5, 5), click_y+random.randint(-5, 5))
        return True
    return False


if __name__ == "__main__":
    model_load()
    load_popup_template()
    picture = cv.imread('./senario_verification_catch/3.png')
    result1 = detect_verification_point(picture)
    if result1 is not None:
        result_x, result_y = result1
        cv.rectangle(picture, np.array([result_x, result_y]).astype(np.int32), np.array([result_x+3, result_y+3]).astype(np.int32), (0, 0, 255), 2)
        cv.imshow("result", picture)
        cv.waitKey()
        cv.destroyAllWindows()
    