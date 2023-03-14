#include <iostream>
#include <string>
#include <Windows.h>

using namespace std;

;

//int my_main(int argc, char **argv)

typedef int (*ptrFun1)(int argc, char** argv);

//HMODULE hMod;
HMODULE hMod = LoadLibraryA(R"(E:\workspace\Qt_projects\ppocr_test_project\build-test_project-Desktop_Qt_5_12_8_MSVC2017_64bit-Release\release\test_project.dll)");
//HMODULE hMod = LoadLibraryA(R"(E:\workspace\Qt_projects\menghuanxiyou_detect_number_project\build-detect_number-Desktop_Qt_5_12_8_MSVC2017_64bit-Release\release\detect_number.dll)");

int main(int argc, char *argv[])
{
    system("chcp  65001");
    if(hMod!=NULL)
    {
        cout << "???\n";
        ptrFun1 my_main = (ptrFun1)GetProcAddress(hMod, "my_main");
        if(my_main != NULL)
        {
            cout << "!!!\n";
            my_main(argc, argv);
        }
    }
    return 0;
}
