# TEMPLATE = app
# CONFIG += console c++11
TEMPLATE = lib
CONFIG += c++11
# CONFIG -= app_bundle
CONFIG -= qt

INCLUDEPATH += "E:/softwares/opencv/build/include"
INCLUDEPATH += "E:/softwares/opencv/build/include/opencv2"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/paddle/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/protobuf/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/glog/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/gflags/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/xxhash/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/zlib/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/onnxruntime/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/paddle2onnx/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/boost"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/eigen3"
INCLUDEPATH += "E:/softwares/PaddleOCR/PaddleOCR/deploy/cpp_infer"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/mklml/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/paddle_inference/third_party/install/mkldnn/include"
INCLUDEPATH += "E:/softwares/PaddleOCR/PaddleOCR/deploy/cpp_infer/build/third-party/extern_autolog-src"

CONFIG(release, debug|release): {
LIBS += -L"E:/softwares/opencv/build/x64/vc15/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/paddle/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/protobuf/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/glog/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/gflags/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/xxhash/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/onnxruntime/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/paddle2onnx/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/mklml/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/mkldnn/lib"
LIBS += -lpaddle_inference -lmklml -llibiomp5md -lmkldnn -lglog -lgflags_static -llibprotobuf
LIBS += -lxxhash -llibcmt -lshlwapi -lcomctl32 -lole32 -lsetupapi -lws2_32
LIBS += -lkernel32 -luser32 -lwinspool -lshell32 -loleaut32 -luuid -lcomdlg32 -ladvapi32
LIBS += -lopencv_world455
LIBS += -lgdi32
QMAKE_CFLAGS_RELEASE += -MT
QMAKE_CXXFLAGS_RELEASE += -MT
}
else:CONFIG(debug, debug|release): {
LIBS += -L"E:/softwares/opencv/build/x64/vc15/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/paddle/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/protobuf/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/glog/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/gflags/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/xxhash/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/onnxruntime/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/paddle2onnx/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/mklml/lib"
LIBS += -L"E:/softwares/PaddleOCR/paddle_inference/third_party/install/mkldnn/lib"
LIBS += -lpaddle_inference -lmklml -llibiomp5md -lmkldnn -lglog -lgflags_static -llibprotobuf
LIBS += -lxxhash -llibcmt -lshlwapi -lcomctl32 -lole32 -lsetupapi -lws2_32
LIBS += -lkernel32 -luser32 -lwinspool -lshell32 -loleaut32 -luuid -lcomdlg32 -ladvapi32
LIBS += -lopencv_world455d
LIBS += -lgdi32
QMAKE_CFLAGS_DEBUG += -MTd
QMAKE_CXXFLAGS_DEBUG += -MTd
}

HEADERS += \
    export_interface.h

SOURCES += \
        args.cpp \
        clipper.cpp \
        my_ppocr_interface.cpp \
        ocr_cls.cpp \
        ocr_det.cpp \
        ocr_rec.cpp \
        paddleocr.cpp \
        paddlestructure.cpp \
        postprocess_op.cpp \
        preprocess_op.cpp \
        structure_layout.cpp \
        structure_table.cpp \
        utility.cpp

DEFINES += WIN32
DEFINES += _WINDOWS
DEFINES += NDEBUG
DEFINES += USE_MKL
DEFINES += GOOGLE_GLOG_DLL_DECL=
#DEFINES += STATIC_LIB
