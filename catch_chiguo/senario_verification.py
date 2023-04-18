import torch
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2 as cv
import os
import random

from model_v3 import mobilenet_v3_large
from match_template_func import get_coor
from keymouse import move_and_click_in_game, move_close_to, do_mouse_action
from shot_screen_func import shot

model = None

popup_path = './popup'
model_path = './model/MobileNetV3.pth'
template_popup_list = []
device = torch.device("cpu")
global_pic_number = 0

data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

def load_popup_template():
    template_popup_list.clear()
    popup_pics = os.listdir(popup_path)
    for i in range(len(popup_pics)):
        popup_pic = popup_pics[i]
        template_popup = cv.imread(os.path.join(popup_path, popup_pic), 0)
        template_popup_list.append(template_popup)


def model_load():
    global model
    # create model
    model = mobilenet_v3_large(num_classes=2).to(device)
    # load model weights
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()


def jiance(np_img):
    global model
    img = Image.fromarray(np_img) 
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()
    confidence1 = predict[0].numpy()
    confidence2 = predict[1].numpy()
    return confidence1/confidence2
    
    
def detect_verification_point(image):
    result = None
    for image1 in template_popup_list:
        result = get_coor(image, image1, 0.8)
        if result is not None:
            break
    if result is not None:
        left_top, right_bottom = result 
        src = image[left_top[1]-10:left_top[1]+160,left_top[0]-282:left_top[0]+78]
        width = 90
        max_confidence = 0
        max_id = 0
        for i in range(4):
            src_person = src[0:170, width*i:width*(i+1)]
            confidence = jiance(src_person)
            print("confidence: ", confidence)
            if confidence > max_confidence:
                max_confidence = confidence
                max_id = i
                
        x_avg = int((left_top[0]-282) + width*(2*max_id+1)/2)
        y_avg = int((left_top[1]-10) + 170/2)
        return x_avg, y_avg


def auto_do_verification():
    result = shot()
    if result is not None:
        image, left, top, right, bottom = result
        detect_result = detect_verification_point(image)
        if detect_result is not None:
            click_x, click_y = detect_result
            for try_i in range(10):
                return_flag = do_mouse_action(click_x+random.randint(-5, 5), click_y+random.randint(-5, 5))
                if return_flag:
                    break
            return True
    return False


if __name__ == "__main__":
    model_load()
    load_popup_template()
    images = os.listdir(r"E:\workspace\menghuanxiyou_outsourcing\scene_verification\xumi")
    for image in images:
        image_path = os.path.join(r"E:\workspace\menghuanxiyou_outsourcing\scene_verification\xumi", image)
        pic = cv.imread(image_path)
        result = detect_verification_point(pic)
        if result is not None:
            x_avg, y_avg = result
            cv.circle(pic, (x_avg, y_avg), 2, (0, 0, 255), 2)
            cv.imshow("show", pic)
            cv.waitKey()
        else:
            print("ERROR: SEARCH FAILED!!")
    '''
    picture = cv.imread('./senario_verification_catch/3.png')
    result1 = detect_verification_point(picture)
    if result1 is not None:
        result_x, result_y = result1
        cv.rectangle(picture, np.array([result_x, result_y]).astype(np.int32), np.array([result_x+3, result_y+3]).astype(np.int32), (0, 0, 255), 2)
        cv.imshow("result", picture)
        cv.waitKey()
        cv.destroyAllWindows()
    '''