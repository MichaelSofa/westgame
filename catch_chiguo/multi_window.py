import numpy as np
import cv2 as cv
import random
import time
from shot_screen_func import shot
from keymouse import do_windows_mouse_action

import numpy as np

def multi_window_detect(image):
    points = []
    this_index = None
    h,w = image.shape[0],image.shape[1]
    image_src = image[31:51,:,:]
    low = np.array([0, 0, 0])
    high = np.array([1, 1, 1])
    image_dst = cv.inRange(src=image_src, lowerb=low, upperb=high) # HSV高低阈值，提取图像部分区域
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (13,7))
    image_dilate = cv.dilate(image_dst, kernel)
    #cv.imshow("show", image_dilate)
    #cv.waitKey()
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(image_dilate,connectivity=8)  
    #retval 连通域个数，stats 外接矩形的x、y、width、height和面积 centroids：连通域的中心点
    tmp_index = 0
    this_index0 = None
    center_x = []
    for i, stat in enumerate(stats):
        if stat[2] < 200 and stat[3] > 12 and stat[2]/stat[3] > 1.5:
            centr=[int(centroids[i][0]), int(31+centroids[i][1])]
            points.append(centr)
            center_x.append(centr[0])
            pix_blue = image[50, centr[0], 0]
            if pix_blue > 200:
                this_index0 = tmp_index
            tmp_index += 1
    if this_index0 is not None:
        sorted_nums = sorted(enumerate(center_x), key=lambda x: x[1])
        idx = [i[0] for i in sorted_nums]
        this_index = idx[this_index0]
    return points, this_index

def to_primary_window():
    result = shot()
    if result is None:
        return
    image, left, top, right, bottom = result
    points, this_index = multi_window_detect(image)
    if this_index is not None and this_index != 0:
        primary_window_point = points[0]
        do_windows_mouse_action(primary_window_point[0]+random.randint(-5, 5), primary_window_point[1]+random.randint(-2, 2))
    
def switch_window():
    result = shot()
    if result is None:
        return
    image, left, top, right, bottom = result
    points, this_index = multi_window_detect(image)
    window_count = len(points)
    if window_count == 1:
        return
    if this_index is not None:
        if this_index == window_count - 1:
            new_index = 0
        else:
            new_index = this_index + 1
        new_window_point = points[new_index]
        do_windows_mouse_action(new_window_point[0]+random.randint(-5, 5), new_window_point[1]+random.randint(-2, 2))


if __name__ == "__main__":
    '''
    image = cv.imread(r"E:\workspace\menghuanxiyou_outsourcing\write_by_dongmei\duokai\7.png")
    point, this_index = multi_window_detect(image)
    for i in range (len(point)):
        print(point[i])
    print("this_index is: {}".format(this_index))
    '''
    switch_window()
    print("aaa")
    time.sleep(1)
    switch_window()
    print("aaa")
    time.sleep(1)
    switch_window()
    print("aaa")
    time.sleep(1)
    to_primary_window()

