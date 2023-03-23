//全局变量部分
vector<cv::Mat> bar_vector;


void init_bar_vector(char* bar_dir) //初始化
{
string bar_dir_string = string(bar_dir);
if (!(bar_dir_string.back() == '/') && !(bar_dir_string.back() == '\\'))
{
	bar_dir_string = bar_dir_string + "/";
}
cv::Mat bar1 = cv::imread(bar_dir_string + "bar1.png");
cv::Mat bar2 = cv::imread(bar_dir_string + "bar2.png");
cv::Mat bar3 = cv::imread(bar_dir_string + "bar3.png");
cv::Mat bar4 = cv::imread(bar_dir_string + "bar4.png");
cv::Mat bar5 = cv::imread(bar_dir_string + "bar5.png");
bar_vector = vector<cv::Mat>();
bar_vector.push_back(bar1);
bar_vector.push_back(bar2);
bar_vector.push_back(bar3);
bar_vector.push_back(bar4);
bar_vector.push_back(bar5);
}

class BattleClass
{
public:
    BattleClass();
    bool detect_if_battle(cv::Mat cv_pic);
private:
    int skip_number;  // 战斗状态下没有达到判定条件跳过的帧数
    int skip_number_thresh;  // 跳过的帧数大于这个阈值就变为非战斗状态
    int remain_number;  // 非战斗状态下达到判定条件保持的帧数
    int remain_number_thresh;  // 保持的帧数大于这个阈值就变为战斗状态
    int condition_flag;  // 状态指示，现在是战斗状态为True，非战斗状态为False
};

BattleClass::BattleClass()
{
    skip_number = 0;  // 战斗状态下没有达到判定条件跳过的帧数
    skip_number_thresh = 10;  // 跳过的帧数大于这个阈值就变为非战斗状态
    remain_number = 0;  // 非战斗状态下达到判定条件保持的帧数
    remain_number_thresh = 3;  // 保持的帧数大于这个阈值就变为战斗状态
    condition_flag = false;  // 状态指示，现在是战斗状态为True，非战斗状态为False
}

bool BattleClass::detect_if_battle(cv::Mat cv_pic)
{
    // 条状控件检测的方法
    int col_num = cv_pic.cols;
    int row_num = cv_pic.rows;
    if (col_num < 21 || row_num < 442)
    {
        cout << "col_num: " << col_num << endl;
        cout << "row_num: " << row_num << endl;
        cout << "image too small!\n";
        return false;
    }

    cv::Mat test_pic_little = cv_pic(cv::Range(177, 441+1), cv::Range(col_num-20, col_num-6));
    cv::Mat hsv_pic;
    cv::cvtColor(test_pic_little, hsv_pic, cv::COLOR_BGR2HSV);

    bool detect_flag = false;
    int h_bins = 60; int s_bins = 64;
    int histSize[] = { h_bins, s_bins };
    float h_ranges[] = { 0, 180 };
    float s_ranges[] = { 0, 256 };
    const float* ranges[] = { h_ranges, s_ranges };
    int channels[] = { 0, 1 };
    cv::Mat hist_pic;
    cv::calcHist(&hsv_pic, 1, channels, cv::Mat(), hist_pic, 2, histSize, ranges, true, false);
    normalize(hist_pic, hist_pic, 0, 1, NORM_MINMAX, -1, Mat()); // 归一化

    if (bar_vector.size()<5)
    {
        cout << "please init!\n";
        return false;
    }

    for (size_t i=0;i<5;++i)
    {
        cv::Mat hsv_bar;
        cv::cvtColor(bar_vector[i], hsv_bar, cv::COLOR_BGR2HSV);
        cv::Mat hist_bar;
        calcHist(&hsv_bar, 1, channels, cv::Mat(), hist_bar, 2, histSize, ranges, true, false);
        normalize(hist_bar, hist_bar, 0, 1, NORM_MINMAX, -1, Mat());
        double result = compareHist(hist_bar, hist_pic, cv::HISTCMP_CORREL);
        if (result>0.75)
        {
            detect_flag = true;
            break;
        }
    }

    if (detect_flag)
    {
        if (this->condition_flag == false)
        {
            this->remain_number += 1;
            if (this->remain_number >= this->remain_number_thresh)
            {
                this->condition_flag = true;
                this->skip_number = 0;
            }
        }
        else
        {
            this->skip_number = 0;
        }
    }
    else
    {
        if (this->condition_flag == false)
        {
            this->remain_number = 0;
        }
        else
        {
            this->skip_number += 1;
            if (this->skip_number >= this->skip_number_thresh)
            {
                this->condition_flag = false;
                this->remain_number = 0;
            }
        }
    }
    return this->condition_flag;
}