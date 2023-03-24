import cv2  as cv
import numpy as np
import os



file_path ="./catch"
file_path1 ="./run"

# 参数设置
CONFIDENCE = 0.5  # 过滤弱检测的最小概率
THRESHOLD = 0.4  # 非最大值抑制阈值
boxThreshold = 0.5
classThreshold = 0.5
nmsThreshold = 0.45
nmsScoreThreshold = boxThreshold * classThreshold

senpen_labels = ['chiguo']
netAnchors = [[10, 13, 16, 30, 33, 23], [30, 61, 62, 45, 59, 119 ], [116, 90, 156, 198, 373, 326]]
netStride = [8.0, 16.0, 32.0, 64.0]
netWidth = 416
netHeight = 416

COLORS = np.random.randint(0, 255, size=(len(senpen_labels), 3), dtype="uint8")

net = cv.dnn.readNet('chiguo.onnx')
net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
#net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)

# net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
# net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


def predict(net, img, labels, COLORS):
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
    
    net_width = 5 + len(senpen_labels)
    # 筛选置信度
    for stride in range(len(layerOutputs)):  # 对每个stride
        grid_x = int(netWidth / netStride[stride])
        grid_y = int(netHeight / netStride[stride])
        for anchor in range(3):  # 对每个anchor框
            anchor_w = netAnchors[stride][anchor * 2];
            anchor_h = netAnchors[stride][anchor * 2 + 1];
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
    
    # 非最大值抑制
    idxs = cv.dnn.NMSBoxes(boxes, confidences, nmsScoreThreshold, nmsThreshold)  # boxes中，保留的box的索引index存入idxs
    
    if len(idxs) > 0:
        for i in idxs.flatten():  # indxs是二维的，第0维是输出层，所以这里把它展平成1维
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            color = [int(c) for c in COLORS[classIDs[i]]]
            cv.rectangle(img, (x, y), (x+w, y+h), color, 2)
            text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
            cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # 字体风格、大小、颜色、粗细
    
    return img,w


def get_coor(image, template, value):
        """
        image 游戏图片 灰度图片
        template 模板图片 灰度图片(不要传入三通道图片！)
        value 模板匹配阈值 越低检测到的东西越多，但是越可能错检
        """
        if len(image.shape) > 2 and image.shape[2] == 3:
            img_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else:
            img_gray = image
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        left_top = max_loc  # 左上角
        right_bottom = (left_top[0] + w, left_top[1] + h)  # 右下角
        if len(loc[0]) > 0:
            # 找到目标图片返回图片当前坐标
            return (left_top, right_bottom)
        else:
            return ((0,0),(0,0))

def file_find(image,path):
    path_list = os.listdir(path)
    print(path_list)
    for filename in path_list:
        print(filename)
        f = os.path.join(path,filename)
        template =cv.imread(f,0)
        (left_top,right_bottom)=get_coor(image,template,0.9)
        cv.rectangle(image, np.array(left_top).astype(np.int32), np.array(right_bottom).astype(np.int32), (0, 0, 255), 2)
        cv.imshow('show', image)
        cv.waitKey(0)
        if(left_top,right_bottom)!=((0,0),(0,0)):
            
            print(left_top)
            print(right_bottom)
            return (left_top, right_bottom)
        else:
            print("not this image")
            print("--------------------------------")
            continue
        

def main(video_path):
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        print('open failed!!')
        return
    video_fps = int(cap.get(cv.CAP_PROP_FPS))
    cv.namedWindow('show', cv.WINDOW_NORMAL)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame.size == 0:
            break
        frame,flag = predict(net, frame, senpen_labels, COLORS)
        cv.imshow('show', frame)
        cv.waitKey(0)
        print(flag)
        if flag != 0:
            print("找到了chiguo")
            (x,y)=file_find(frame,file_path)
            print(x)
            print(y)
            return 
        else:
            print("没找到chiguo")
            (x,y)=file_find(frame,file_path1)
            print(x)
            print(y)
            return 
    
    
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    video_path = './video/test6.mp4'
    
    main(video_path)
    # image = cv.imread('back.png')
    # file_find(image,file_path)

