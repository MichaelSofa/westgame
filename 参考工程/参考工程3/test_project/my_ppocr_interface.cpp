// Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#include "opencv2/core.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/imgproc.hpp"
#include <opencv2/opencv.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <Windows.h>
#include <wingdi.h>
#include <conio.h>
#include <include/args.h>
#include <include/paddleocr.h>
#include <include/paddlestructure.h>

#include <ctime>
#include <chrono>
#include "export_interface.h"

#pragma comment (lib, "User32.lib")

#define KEY_DOWN(vKey) ((GetAsyncKeyState(vKey) & 0x8000) ? 1:0)

using namespace PaddleOCR;

PPOCR* global_ocr;

bool my_load_ppocr(std::string model_dir, bool det_flag, bool rec_flag, bool cls_flag, bool use_angle_cls);

std::vector<OCRPredictResult> my_run_ppocr(cv::Mat img);

void my_release_ppocr();

// about screen shooting and get area

int window_x=0;
int window_y=0;
int window_w=0;
int window_h=0;

//抓取当前屏幕函数
void Screen(HBITMAP& hBmp) {
    //创建画板
    HBITMAP hOld;
    HDC hScreen = CreateDCA("DISPLAY", NULL, NULL, NULL);
    HDC hCompDC = CreateCompatibleDC(hScreen);
    //取屏幕宽度和高度
    int nWidth = GetSystemMetrics(SM_CXSCREEN);
    int	nHeight = GetSystemMetrics(SM_CYSCREEN);
    //创建Bitmap对象
    hBmp = CreateCompatibleBitmap(hScreen, nWidth, nHeight);
    hOld = (HBITMAP)SelectObject(hCompDC, hBmp);
    BitBlt(hCompDC, 0, 0, nWidth, nHeight, hScreen, 0, 0, SRCCOPY);
    SelectObject(hCompDC, hOld);
    //释放对象
    DeleteDC(hScreen);
    DeleteDC(hCompDC);
}

//把HBITMAP型转成Mat型
bool HBitmapToMat(HBITMAP& _hBmp, cv::Mat& _mat)
{
    //BITMAP操作
    BITMAP bmp;
    GetObject(_hBmp, sizeof(BITMAP), &bmp);
    int nChannels = bmp.bmBitsPixel == 1 ? 1 : bmp.bmBitsPixel / 8;
    //mat操作
    cv::Mat v_mat;
    v_mat.create(cv::Size(bmp.bmWidth, bmp.bmHeight), CV_MAKETYPE(CV_8U, nChannels));
    GetBitmapBits(_hBmp, bmp.bmHeight * bmp.bmWidth * nChannels, v_mat.data);
    cv::cvtColor(v_mat, v_mat, cv::COLOR_BGRA2BGR);
    _mat = v_mat;
    return TRUE;
}


BOOL MyFindWindowEnum(HWND hwnd, LPARAM lParam)
{
    CHAR wszTitle[MAX_PATH] = { 0 };
    LRESULT result = GetWindowTextA(hwnd, wszTitle, MAX_PATH);
    std::string string_title{wszTitle};
    std::string string_menghuan = "梦幻西游 ONLINE";
    if (string_title.find(string_menghuan)!=std::string::npos)
    {
        std::cout <<"string_title: "+string_title << std::endl;
        *((HWND *)lParam) = hwnd; //是梦幻西游!
        return FALSE;
    }
    return TRUE;
}

HWND MyFindWindow()
{
    HWND hPrevWnd = NULL;
    EnumWindows(MyFindWindowEnum, (LPARAM)&hPrevWnd);
    return hPrevWnd;
}


BOOL MyGetWindowRect()
{
    HWND hWnd = MyFindWindow();
    //HWND hWnd = GetForegroundWindow();
    if( hWnd == NULL )
    {
        return FALSE;
    }
    RECT windowRect;
    if (!::GetWindowRect(hWnd, &windowRect))
    {
        return FALSE;
    }

    window_y = windowRect.top;
    window_x = windowRect.left;
    window_w = windowRect.right - windowRect.left;
    window_h = windowRect.bottom - windowRect.top;
    return TRUE;
}



// end screen shooting



void check_params() {
  if (FLAGS_det) {
    if (FLAGS_det_model_dir.empty() || FLAGS_image_dir.empty()) {
      std::cout << "Usage[det]: ./ppocr "
                   "--det_model_dir=/PATH/TO/DET_INFERENCE_MODEL/ "
                << "--image_dir=/PATH/TO/INPUT/IMAGE/" << std::endl;
      exit(1);
    }
  }
  if (FLAGS_rec) {
    std::cout
        << "In PP-OCRv3, rec_image_shape parameter defaults to '3, 48, 320',"
           "if you are using recognition model with PP-OCRv2 or an older "
           "version, "
           "please set --rec_image_shape='3,32,320"
        << std::endl;
    if (FLAGS_rec_model_dir.empty() || FLAGS_image_dir.empty()) {
      std::cout << "Usage[rec]: ./ppocr "
                   "--rec_model_dir=/PATH/TO/REC_INFERENCE_MODEL/ "
                << "--image_dir=/PATH/TO/INPUT/IMAGE/" << std::endl;
      exit(1);
    }
  }
  if (FLAGS_cls && FLAGS_use_angle_cls) {
    if (FLAGS_cls_model_dir.empty() || FLAGS_image_dir.empty()) {
      std::cout << "Usage[cls]: ./ppocr "
                << "--cls_model_dir=/PATH/TO/REC_INFERENCE_MODEL/ "
                << "--image_dir=/PATH/TO/INPUT/IMAGE/" << std::endl;
      exit(1);
    }
  }
  if (FLAGS_table) {
    if (FLAGS_table_model_dir.empty() || FLAGS_det_model_dir.empty() ||
        FLAGS_rec_model_dir.empty() || FLAGS_image_dir.empty()) {
      std::cout << "Usage[table]: ./ppocr "
                << "--det_model_dir=/PATH/TO/DET_INFERENCE_MODEL/ "
                << "--rec_model_dir=/PATH/TO/REC_INFERENCE_MODEL/ "
                << "--table_model_dir=/PATH/TO/TABLE_INFERENCE_MODEL/ "
                << "--image_dir=/PATH/TO/INPUT/IMAGE/" << std::endl;
      exit(1);
    }
  }
  if (FLAGS_layout) {
    if (FLAGS_layout_model_dir.empty() || FLAGS_image_dir.empty()) {
      std::cout << "Usage[layout]: ./ppocr "
                << "--layout_model_dir=/PATH/TO/LAYOUT_INFERENCE_MODEL/ "
                << "--image_dir=/PATH/TO/INPUT/IMAGE/" << std::endl;
      exit(1);
    }
  }
  if (FLAGS_precision != "fp32" && FLAGS_precision != "fp16" &&
      FLAGS_precision != "int8") {
    std::cout << "precison should be 'fp32'(default), 'fp16' or 'int8'. "
              << std::endl;
    exit(1);
  }
}

void ocr(std::vector<cv::String> &cv_all_img_names) {
  PPOCR ocr = PPOCR();

  if (FLAGS_benchmark) {
    ocr.reset_timer();
  }

  std::vector<cv::Mat> img_list;
  std::vector<cv::String> img_names;
  for (int i = 0; i < cv_all_img_names.size(); ++i) {
    cv::Mat img = cv::imread(cv_all_img_names[i], cv::IMREAD_COLOR);
    if (!img.data) {
      std::cerr << "[ERROR] image read failed! image path: "
                << cv_all_img_names[i] << std::endl;
      continue;
    }
    img_list.push_back(img);
    img_names.push_back(cv_all_img_names[i]);
  }
  // new
  auto duration_since_epoch = std::chrono::system_clock::now().time_since_epoch();
  auto microseconds_since_epoch = std::chrono::duration_cast<std::chrono::microseconds>(duration_since_epoch).count();
  auto old_milliseconds_since_epoch = microseconds_since_epoch/1000;
  // end new
  std::vector<std::vector<OCRPredictResult>> ocr_results =
      ocr.ocr(img_list, FLAGS_det, FLAGS_rec, FLAGS_cls);

  // new
  duration_since_epoch = std::chrono::system_clock::now().time_since_epoch();
  microseconds_since_epoch = std::chrono::duration_cast<std::chrono::microseconds>(duration_since_epoch).count();
  auto new_milliseconds_since_epoch = microseconds_since_epoch / 1000;

  std::cout << "spend_time: " << new_milliseconds_since_epoch - old_milliseconds_since_epoch << std::endl;
  // endnew
  for (int i = 0; i < img_names.size(); ++i) {
    std::cout << "predict img: " << cv_all_img_names[i] << std::endl;
    Utility::print_result(ocr_results[i]);
    if (FLAGS_visualize && FLAGS_det) {
      std::string file_name = Utility::basename(img_names[i]);
      cv::Mat srcimg = img_list[i];
      Utility::VisualizeBboxes(srcimg, ocr_results[i],
                               FLAGS_output + "/" + file_name);
    }
  }
  if (FLAGS_benchmark) {
    ocr.benchmark_log(cv_all_img_names.size());
  }
}

void structure(std::vector<cv::String> &cv_all_img_names) {
  PaddleOCR::PaddleStructure engine = PaddleOCR::PaddleStructure();

  if (FLAGS_benchmark) {
    engine.reset_timer();
  }

  for (int i = 0; i < cv_all_img_names.size(); i++) {
    std::cout << "predict img: " << cv_all_img_names[i] << std::endl;
    cv::Mat img = cv::imread(cv_all_img_names[i], cv::IMREAD_COLOR);
    if (!img.data) {
      std::cerr << "[ERROR] image read failed! image path: "
                << cv_all_img_names[i] << std::endl;
      continue;
    }

    std::vector<StructurePredictResult> structure_results = engine.structure(
        img, FLAGS_layout, FLAGS_table, FLAGS_det && FLAGS_rec);

    for (int j = 0; j < structure_results.size(); j++) {
      std::cout << j << "\ttype: " << structure_results[j].type
                << ", region: [";
      std::cout << structure_results[j].box[0] << ","
                << structure_results[j].box[1] << ","
                << structure_results[j].box[2] << ","
                << structure_results[j].box[3] << "], score: ";
      std::cout << structure_results[j].confidence << ", res: ";

      if (structure_results[j].type == "table") {
        std::cout << structure_results[j].html << std::endl;
        if (structure_results[j].cell_box.size() > 0 && FLAGS_visualize) {
          std::string file_name = Utility::basename(cv_all_img_names[i]);

          Utility::VisualizeBboxes(img, structure_results[j],
                                   FLAGS_output + "/" + std::to_string(j) +
                                       "_" + file_name);
        }
      } else {
        std::cout << "count of ocr result is : "
                  << structure_results[j].text_res.size() << std::endl;
        if (structure_results[j].text_res.size() > 0) {
          std::cout << "********** print ocr result "
                    << "**********" << std::endl;
          Utility::print_result(structure_results[j].text_res);
          std::cout << "********** end print ocr result "
                    << "**********" << std::endl;
        }
      }
    }
  }
  if (FLAGS_benchmark) {
    engine.benchmark_log(cv_all_img_names.size());
  }
}


int my_main(int argc, char **argv) {
  // Parsing command-line
  google::ParseCommandLineFlags(&argc, &argv, true);
  //check_params();
  std::string model_dir = R"(E:\workspace\Qt_projects\ppocr_test_project\ppocr_model)";

  //if (!Utility::PathExists(FLAGS_output)) {
  //  Utility::CreateDir(FLAGS_output);
  //}
  bool load_result = my_load_ppocr(model_dir, false, true, false, false);
  //bool load_result = my_load_ppocr(model_dir, true, true, true, true);
  if (!load_result)
  {
      std::cout << "model dir not found!\n";
      return 1;
  }
  /*
  cv::Mat img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\0.jpg)", cv::IMREAD_COLOR);
  std::vector<OCRPredictResult> ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\1.jpg)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\2.jpg)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\3.jpg)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\4.jpg)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\5.jpg)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\6-little.png)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\7-little.png)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);

  img = cv::imread(R"(E:\softwares\PaddleOCR\PaddleOCR\doc\imgs\8-little.png)", cv::IMREAD_COLOR);
  ocr_result = my_run_ppocr(img);
  Utility::print_result(ocr_result);
  */
  while (true)
  {
      if (KEY_DOWN('\\'))
      {
          break;
      }
      int ret_val = MyGetWindowRect();
      if (!ret_val)
      {
          continue;
      }

      if (window_h <= 0 || window_w <= 0)
      {
          continue;
      }
      if (window_x < 0 || window_y < 0)
      {
          continue;
      }

      cv::Mat image;
      HBITMAP hBmp;
      Screen(hBmp);
      HBitmapToMat(hBmp, image);
      DeleteObject(hBmp);
      if (window_x + window_w > image.cols || window_y + window_h > image.rows)
      {
          continue;
      }

      image = image(cv::Range(window_y, window_y+window_h), cv::Range(window_x, window_x+window_w));
      if(window_h <= 94 || window_w <= 230)
      {
          continue;
      }
      cv::Mat image_text = image(cv::Range(window_h-94, window_h-69), cv::Range(window_w/2-115, window_w/2+156));
      std::vector<OCRPredictResult> ocr_result = my_run_ppocr(image_text);
      Utility::print_result(ocr_result);
  }
  my_release_ppocr();
  return 0;
}


bool my_load_ppocr(std::string model_dir, bool det_flag, bool rec_flag, bool cls_flag, bool use_angle_cls)
{
  if (!Utility::PathExists(model_dir)) {
    std::cerr << "[ERROR] image path not exist! image_dir: " << model_dir
            << std::endl;
    return false;
  }
  if (model_dir.back() == '/' || model_dir.back() == '\\')
  {
    FLAGS_rec_char_dict_path = model_dir + "ppocr_keys_v1.txt";
    FLAGS_layout_dict_path = model_dir + "layout_publaynet_dict.txt";
    FLAGS_table_char_dict_path = model_dir + "table_structure_dict_ch.txt";
    FLAGS_det_model_dir = model_dir + "det_db";
    FLAGS_cls_model_dir = model_dir + "cls";
    FLAGS_rec_model_dir = model_dir + "rec_rcnn";
  }
  else
  {
      FLAGS_rec_char_dict_path = model_dir + "/ppocr_keys_v1.txt";
      FLAGS_layout_dict_path = model_dir + "/layout_publaynet_dict.txt";
      FLAGS_table_char_dict_path = model_dir + "/table_structure_dict_ch.txt";
      FLAGS_det_model_dir = model_dir + "/det_db";
      FLAGS_cls_model_dir = model_dir + "/cls";
      FLAGS_rec_model_dir = model_dir + "/rec_rcnn";
  }
  FLAGS_det = det_flag;
  FLAGS_rec = rec_flag;
  FLAGS_cls = cls_flag;
  FLAGS_use_angle_cls = use_angle_cls;
  global_ocr = new PPOCR();
  return true;
}

std::vector<OCRPredictResult> my_run_ppocr(cv::Mat img)
{
    std::cout << "into my_run_ppocr\n";
    auto duration_since_epoch = std::chrono::system_clock::now().time_since_epoch();
    auto microseconds_since_epoch = std::chrono::duration_cast<std::chrono::microseconds>(duration_since_epoch).count();
    auto old_milliseconds_since_epoch = microseconds_since_epoch/1000;
    std::vector<cv::Mat> imgs = {img};
    std::vector<std::vector<OCRPredictResult>> ocr_results =
        global_ocr->ocr(imgs, FLAGS_det, FLAGS_rec, FLAGS_cls);

    duration_since_epoch = std::chrono::system_clock::now().time_since_epoch();
    microseconds_since_epoch = std::chrono::duration_cast<std::chrono::microseconds>(duration_since_epoch).count();
    auto new_milliseconds_since_epoch = microseconds_since_epoch / 1000;
    std::cout << "spend_time: " << new_milliseconds_since_epoch - old_milliseconds_since_epoch << std::endl;
    return  ocr_results[0];
}

void my_release_ppocr()
{
    if (global_ocr != nullptr)
    {
        delete global_ocr;
    }
}
