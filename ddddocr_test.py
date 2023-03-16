import os
import cv2 as cv
import numpy as np

import ddddocr

cut_dir = './text_pics/cut'
cut_pictures = os.listdir(cut_dir)

det = ddddocr.DdddOcr(det=True)
ocr = ddddocr.DdddOcr(beta=True)

result = []
for cut_picture in cut_pictures:
    image = cv.imread(os.path.join(cut_dir, cut_picture))
    data = cv.imencode('.jpg', image)[1].tobytes()
    poses = det.detection(data)
    #res1 = ocr.classification(data)
    #print("direct result: ", res1)
    little_pic_list = []
    for box in poses:
        x1, y1, x2, y2 = box
        little_pic = image[y1:y2, x1:x2, :]
        little_pic_list.append(little_pic)
    
    for box in poses:
        x1, y1, x2, y2 = box
        im = cv.rectangle(image, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
    cv.imwrite(os.path.join('./text_pics/result', cut_picture[0:-4] + '_cut.png'), im)
    
    pic_result = []
    for little_pic in little_pic_list:
        data = cv.imencode('.jpg', little_pic)[1].tobytes()
        res = ocr.classification(data)
        pic_result.append(res)
        
    result.append(pic_result)
    
for pic_result in result:
    for char_result in pic_result:
        print(char_result, end=' ')
    print('')
    
        

