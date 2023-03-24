import cv2
import numpy as np
import time

def get_coor(image, template, value):
        """
        image 游戏图片 灰度图片
        template 模板图片 灰度图片(不要传入三通道图片！)
        value 模板匹配阈值 越低检测到的东西越多，但是越可能错检
        """
        if len(image.shape) > 2 and image.shape[2] == 3:
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = image
        h, w = template.shape[0:2]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        left_top = max_loc  # 左上角
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if len(loc[0]) > 0:
            # 找到目标图片返回找到的模板相对于图片的坐标 否则返回None
            return (left_top, right_bottom)

