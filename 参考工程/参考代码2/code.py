import os
import cv2 as cv

class BattleClass:
    def __init__(self):
        self.skip_number = 0;  # 战斗状态下没有达到判定条件跳过的帧数
        self.skip_number_thresh = 10;  # 跳过的帧数大于这个阈值就变为非战斗状态
        self.remain_number = 0;  # 非战斗状态下达到判定条件保持的帧数
        self.remain_number_thresh = 3;  # 保持的帧数大于这个阈值就变为战斗状态
        self.condition_flag = False;  # 状态指示，现在是战斗状态为True，非战斗状态为False
        self.bar_vector = list()
    
    def init_bar_vector(self, bar_dir):
        # 初始化条状图加载
        if len(self.bar_vector) == 5:
            return True
        self.bar_vector.clear()
        if not os.path.exists(bar_dir):
            return False
        bar1 = cv.imread(os.path.join(bar_dir, "bar1.png"))
        if bar1 is None:
            return False
        bar2 = cv.imread(os.path.join(bar_dir, "bar2.png"))
        if bar2 is None:
            return False
        bar3 = cv.imread(os.path.join(bar_dir, "bar3.png"))
        if bar3 is None:
            return False
        bar4 = cv.imread(os.path.join(bar_dir, "bar4.png"))
        if bar4 is None:
            return False
        bar5 = cv.imread(os.path.join(bar_dir, "bar5.png"))
        if bar5 is None:
            return False
        self.bar_vector.append(bar1)
        self.bar_vector.append(bar2)
        self.bar_vector.append(bar3)
        self.bar_vector.append(bar4)
        self.bar_vector.append(bar5)
        return True
        
    def detect_if_battle(self, cv_pic):
        # 检测是否处于战斗状态
        if cv_pic is None:
            print("empty image")
            return False
        
        col_num = cv_pic.shape[1]
        row_num = cv_pic.shape[0]
        if col_num < 21 or row_num < 442:
            print("col_num: {}".format(col_num))
            print("row_num: {}".format(row_num))
            print("image too small!")
            return False

        test_pic_little = cv_pic[177:441+1,col_num-20:col_num-6,:]
        hsv_pic = cv.cvtColor(test_pic_little, cv.COLOR_BGR2HSV)

        detect_flag = False
        h_bins = 60
        s_bins = 64
        histSize = [h_bins, s_bins]
        #h_ranges = [0, 180]
        #s_ranges = [0, 256]
        #ranges = [h_ranges, s_ranges]
        ranges = [0, 180, 0, 256]
        channels = [0, 1]
        hist_pic = cv.calcHist(hsv_pic, channels, None, histSize, ranges, True, False)
        hist_pic = cv.normalize(hist_pic, hist_pic, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)  # 归一化

        if len(self.bar_vector)<5:
            print("please init the bar vector first!")
            return False

        for i in range(5):
            hsv_bar = cv.cvtColor(self.bar_vector[i], cv.COLOR_BGR2HSV)
            hist_bar = cv.calcHist(hsv_bar, channels, None, histSize, ranges, True, False)
            hist_bar = cv.normalize(hist_bar, hist_bar, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
            result = cv.compareHist(hist_bar, hist_pic, cv.HISTCMP_CORREL)
            if result>0.75:
                detect_flag = True
                break

        if detect_flag:
            if self.condition_flag == False:
                self.remain_number += 1
                if self.remain_number >= self.remain_number_thresh:
                    self.condition_flag = True
                    self.skip_number = 0
            else:
                self.skip_number = 0
        else:
            if self.condition_flag == False:
                self.remain_number = 0
            else:
                self.skip_number += 1
                if self.skip_number >= self.skip_number_thresh:
                    self.condition_flag = False
                    self.remain_number = 0
        return self.condition_flag