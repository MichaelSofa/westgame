import cv2 as cv
import numpy as np
import os
import time
import random
from match_template_func import get_coor
from keymouse import do_mouse_action, do_press_alt_key
import pydirectinput
from shot_screen_func import shot

catch_path = "./catch"
run_path = "./run"
template_catch_list = []
template_run_list = []

# 参数设置
CONFIDENCE = 0.5  # 过滤弱检测的最小概率
THRESHOLD = 0.4  # 非最大值抑制阈值
boxThreshold = 0.5
classThreshold = 0.5
nmsThreshold = 0.45
nmsScoreThreshold = boxThreshold * classThreshold

net_path = "./model/chiguo.onnx"
yolo_labels = ['chiguo']
netAnchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119 ], [116, 90, 156, 198, 373, 326]]
netStride = [8.0, 16.0, 32.0, 64.0]
netWidth = 416
netHeight = 416

# COLORS = np.random.randint(0, 255, size=(len(yolo_labels), 3), dtype="uint8")
net = None


def load_catch_and_run_template():
    template_catch_list.clear()
    catch_pics = os.listdir(catch_path)
    for i in range(len(catch_pics)):
        catch_pic = catch_pics[i]
        template_catch = cv.imread(os.path.join(catch_path, catch_pic), 0)
        template_catch_list.append(template_catch)
    template_run_list.clear()
    run_pics = os.listdir(run_path)
    for i in range(len(run_pics)):
        run_pic = run_pics[i]
        template_run = cv.imread(os.path.join(run_path, run_pic), 0)
        template_run_list.append(template_run)


def net_load():
    global net
    net = cv.dnn.readNet(net_path)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
    # net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
    # net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    # net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


def predict(net, img, labels):
    (H, W) = img.shape[:2]
    blobImg = cv.dnn.blobFromImage(img, 1.0/255.0, (netWidth, netHeight), None, True, False)
    net.setInput(blobImg)  # # 调用setInput函数将图片送入输入层
    outInfo = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(outInfo)
    
    ratio_h = H / netHeight
    ratio_w = W / netWidth
    
    boxes = []  # 所有边界框
    confidences = []  # 所有置信度
    classIDs = []  # 所有分类ID
    centers = []  # 所有中心
    
    net_width = 5 + len(yolo_labels)
    # 筛选置信度
    for stride in range(len(layerOutputs)):  # 对每个stride
        grid_x = int(netWidth / netStride[stride])
        grid_y = int(netHeight / netStride[stride])
        for anchor in range(3):  # 对每个anchor框
            anchor_w = netAnchors[stride][anchor * 2]
            anchor_h = netAnchors[stride][anchor * 2 + 1]
            out = layerOutputs[stride][0][anchor]
            out = 1.0 / (1.0 + np.exp(-out))  # 整体sigmoid
            for i in range(grid_y):
                for j in range(grid_x):
                    box_score = out[i,j,4]
                    if (box_score >= boxThreshold):
                        scores = out[i,j,5:]
                        classID = np.argmax(scores)
                        max_class_score = scores[classID]
                        if (max_class_score >= classThreshold):
                            x = (out[i,j,0] * 2 - 0.5 + j) * netStride[stride] * ratio_w
                            y = (out[i,j,1] * 2 - 0.5 + i) * netStride[stride] * ratio_h
                            w = (out[i,j,2] * 2) ** 2 * anchor_w * ratio_w
                            h = (out[i,j,3] * 2) ** 2 * anchor_h * ratio_h
                            left = int(x - 0.5 * w + 0.5)
                            top = int(y - 0.5 * h + 0.5)
                            classIDs.append(classID)
                            confidences.append(max_class_score * box_score)
                            boxes.append([left, top, int(w), int(h)])
                            centers.append([left + int(w/2), top + int(h/2)])
    
    # 非最大值抑制
    idxs = cv.dnn.NMSBoxes(boxes, confidences, nmsScoreThreshold, nmsThreshold)  # boxes中，保留的box的索引index存入idxs
    out_boxes = []  # 所有边界框
    out_confidences = []  # 所有置信度
    out_classIDs = []  # 所有分类ID
    out_centers = []  # 所有中心

    if len(idxs) > 0:
        for i in idxs.flatten():
            out_boxes.append(boxes[i])
            out_confidences.append(confidences[i])
            out_classIDs.append(classIDs[i])
            out_centers.append(centers[i])
    #     for i in idxs.flatten():  # indxs是二维的，第0维是输出层，所以这里把它展平成1维
    #         (x, y) = (boxes[i][0], boxes[i][1])
    #         (w, h) = (boxes[i][2], boxes[i][3])
    #         color = [int(c) for c in COLORS[classIDs[i]]]
    #         cv.rectangle(img, (x, y), (x+w, y+h), color, 2)
    #         text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
    #         cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # 字体风格、大小、颜色、粗细
    return out_boxes, out_confidences, out_classIDs, out_centers


def find_button(image, template_list):
    for template in template_list:
        result = get_coor(image, template, 0.8)
        if result is not None:
            (left_top, right_bottom) = result
            return left_top, right_bottom
        

def process_one_battle_frame(fight_flag=False):
    result = shot()
    if result is None:
        return
    image, left, top, right, bottom = result
    out_boxes, out_confidences, out_classIDs, out_centers = predict(net, image, yolo_labels)
    if len(out_centers) > 0:
        result = find_button(image, template_catch_list)  # 人物抓宝宝
        if result is not None:
            '''
            left_top, right_bottom = result
            center_x = int((left_top[0] + right_bottom[0])/2)
            center_y = int((left_top[1] + right_bottom[1])/2)
            do_mouse_action(center_x+random.randint(-3, 3), center_y+random.randint(-3, 3))
            '''
            do_press_alt_key('g')
            for try_i in range(10):
                return_flag = do_mouse_action(out_centers[0][0]+random.randint(-5, 5), out_centers[0][1]+random.randint(-5, 5))
                if return_flag:
                    break

        result = shot()  # 重新采图 宠物防御
        if result is not None:
            image, left, top, right, bottom = result
            result = find_buttom(image, template_run_list)
            if result is not None:
                do_press_alt_key('d')
        
    else:
        if not fight_flag:  # escape
            result = find_button(image, template_run_list)  # 人物逃跑
            if result is not None:
                left_top, right_bottom = result
                center_x = int((left_top[0] + right_bottom[0])/2)
                center_y = int((left_top[1] + right_bottom[1])/2)
                for try_i in range(10):
                    return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y+random.randint(-3, 3))
                    if return_flag:
                        break
                        
            result = shot()  # 重新采图 宠物逃跑
            if result is not None:
                image, left, top, right, bottom = result
                result = find_button(image, template_run_list)  
                if result is not None:
                    left_top, right_bottom = result
                    center_x = int((left_top[0] + right_bottom[0])/2)
                    center_y = int((left_top[1] + right_bottom[1])/2)
                    for try_i in range(10):
                        return_flag = do_mouse_action(center_x+random.randint(-3, 3), center_y+random.randint(-3, 3))
                        if return_flag:
                            break
                
        else:  # fight
            result = find_button(image, template_run_list)  # 识别逃跑按钮
            if result is not None:
                do_press_alt_key('q') # 人物自动施法
            # 重新采图 宠物施法
            result = shot()  # 重新采图 宠物攻击
            if result is not None:
                image, left, top, right, bottom = result
                result = find_button(image, template_run_list)  
                if result is not None:
                    do_press_alt_key('q')  # 宠物自动施法


if __name__ == "__main__":
    '''
    video_path = './video/test6.mp4'
    cap = cv.VideoCapture(video_path)
    ret, frame = cap.read()
    while ret:
        process_one_battle_frame(frame)
    '''
    net_load()
    COLORS = np.random.randint(0, 255, size=(len(yolo_labels), 3), dtype="uint8")
    picture_path = r"C:\Users\HP\Desktop\aaa.jpg"
    A = cv.imread(picture_path)
    out_boxes, out_confidences, out_classIDs, out_centers = predict(net, A, yolo_labels)
    for i in range(len(out_boxes)):
        (x, y) = (out_boxes[i][0], out_boxes[i][1])
        (w, h) = (out_boxes[i][2], out_boxes[i][3])
        color = [int(c) for c in COLORS[out_classIDs[i]]]
        cv.rectangle(A, (x, y), (x+w, y+h), color, 2)
        text = "{}: {:.4f}".format(yolo_labels[out_classIDs[i]], out_confidences[i])
        cv.putText(A, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # 字体风格、大小、颜色、粗细
    cv.imshow("show", A)
    cv.waitKey()
    cv.closeAllWindows()

