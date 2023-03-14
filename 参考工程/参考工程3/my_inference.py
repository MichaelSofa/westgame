import os
import numpy as np
import cv2 as cv
import tools.infer.utility as utility
import tools.infer.predict_rec as predict_rec
import time

os.environ["FLAGS_allocator_strategy"] = 'auto_growth'
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'



args = utility.parse_args()
print(args)
args.image_dir = r'./test_pictures/6-little.png'
# args.det_model_dir = r'./ppocr_model/det_db/'
# args.cls_model_dir = r'./ppocr_model/cls/'
args.rec_model_dir = r'./ppocr_model/rec_rcnn/'

# args.det = False
# args.rec = True
# args.cls = False
# args.use_angle_cls = False
text_recognizer = predict_rec.TextRecognizer(args)
image = cv.imread(args.image_dir)
for i in range(5):
    img = np.random.uniform(0, 255, [640, 640, 3]).astype(np.uint8)
    _, elapse = text_recognizer([img])
    print("warmup: {}".format(elapse))
rec_res, elapse = text_recognizer([image])
print("result: {}".format(rec_res))
print("spend time: {}".format(elapse))