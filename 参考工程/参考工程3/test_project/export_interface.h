#ifndef EXPORT_INTERFACE_H
#define EXPORT_INTERFACE_H

extern "C"
{
    __declspec(dllexport) int my_main(int argc, char **argv);
}


#endif // EXPORT_INTERFACE_H
