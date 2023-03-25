import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2 as cv

model = None
IMG_HEIGHT = 100
IMG_WIDTH = 100

def model_load(model_path):
    global model
    model = keras.models.load_model(model_path)
    model.summary()
    

def model_predict(image1, image2, image3, image4):
    global model
    imgs = [image1, image2, image3, image4]
    imgs =  tf.convert_to_tensor(imgs)
    predictions = model.predict(imgs)
    predictions = [row[0] for row in predictions]
    print(predictions)
    min_index = predictions.index(min(predictions))
    print(f' 预测结果为 第 > {min_index + 1} < 张图片')
    return min_index
    
    
def preprocess_image(image):  # 输入numpy图像
  image = tf.convert_to_tensor(image, dtype=tf.float32)
  image = tf.image.resize(image, [IMG_WIDTH, IMG_HEIGHT])
  image /= 255.0  # normalize to [0,1] range
  return image
  

if __name__ == "__main__":
    model_load('./model/mhxy.h5')
    image1 = cv.imread('./1.png')
    image2 = cv.imread('./2.png')
    image3 = cv.imread('./3.png')
    image4 = cv.imread('./4.png')
    image1 = preprocess_image(image1)
    image2 = preprocess_image(image2)
    image3 = preprocess_image(image3)
    image4 = preprocess_image(image4)
    model_predict(image1, image2, image3, image4)
    