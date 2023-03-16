import win32gui
import shutil
import io
import sys
import os
import time
from skimage.metrics import structural_similarity
import cv2 as cv
from PIL import Image
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import numpy as np
from matplotlib import pyplot as plt

# 全局变量
hwnd_title = dict()


def qimage2numpy(qimage, dtype='array'):
    """Convert QImage to numpy.ndarray.  The dtype defaults to uint8
    for QImage.Format_Indexed8 or `bgra_dtype` (i.e. a record array)
    for 32bit color images.  You can pass a different dtype to use, or
    'array' to get a 3D uint8 array for color images."""
    result_shape = (qimage.height(), qimage.width())
    temp_shape = (qimage.height(),
                  qimage.bytesPerLine() * 8 // qimage.depth())
    if qimage.format() in (QtGui.QImage.Format_ARGB32_Premultiplied,
                           QtGui.QImage.Format_ARGB32,
                           QtGui.QImage.Format_RGB32):
        if dtype == 'rec':
            dtype = QtGui.bgra_dtype
        elif dtype == 'array':
            dtype = np.uint8
            result_shape += (4,)
            temp_shape += (4,)
    elif qimage.format() == QtGui.QImage.Format_Indexed8:
        dtype = np.uint8
    else:
        raise ValueError("qimage2numpy only supports 32bit and 8bit images")
        # FIXME: raise error if alignment does not match
    size = qimage.size()
    # buf = qimage.bits().asstring(qimage.numBytes())
    buf = qimage.bits().asstring(size.width() * size.height() * qimage.depth() // 8)
    print(dtype)
    print(temp_shape)
    result = np.frombuffer(buf, dtype).reshape(temp_shape)
    
    if result_shape != temp_shape:
        result = result[:, :result_shape[1]]
    if qimage.format() == QtGui.QImage.Format_RGB32 and dtype == np.uint8:
        result = result[..., :3]
    # result = result[:,:,::-1]
    return result


def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
        




def shot():
    hwnd_title.clear()
    win32gui.EnumWindows(get_all_hwnd, 0)
    mhxy_title = ''
    for h,t in hwnd_title.items():
        # print(h)
        # print(t)
        if t.startswith('梦幻西游 ONLINE'):
            mhxy_title = t
            # print(mhxy_title)
            hwnd = win32gui.FindWindow(None, mhxy_title)
            app = QApplication(sys.argv)
            #desktop_id = app.desktop().winId()
            screen = QApplication.primaryScreen()
            #img_desk = screen.grabWindow(desktop_id).toImage()
            img_sc = screen.grabWindow(hwnd).toImage()
            #img_desk.save('./image_desk.png')
            # img_sc.save('./image_screen.png')
            print(type(img_sc))
            image_numpy = qimage2numpy(img_sc)

    if mhxy_title == '':
        print('mhxy not start')
        return None
    return image_numpy



if __name__ == "__main__":
    cv.namedWindow('show', cv.WINDOW_NORMAL)
    while True:
        np_image = shot()
        if np_image is not None:
            cv.imshow("show", np_image)
            key = cv.waitKey(1)
            if key & 0xFF == 27 or key & 0xFF == ord('Q') or key & 0xFF == ord('q'):
                break
    
    cv.destroyAllWindows()
            