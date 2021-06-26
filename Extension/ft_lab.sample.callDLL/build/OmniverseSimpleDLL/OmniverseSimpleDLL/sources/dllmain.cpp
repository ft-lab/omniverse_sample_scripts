
#include <windows.h>
#include <stdio.h>

#define DLL_API extern "C" __declspec(dllexport) 

// ----------------------------------------------------------------.
// DLLMain.
// ----------------------------------------------------------------.
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

// ----------------------------------------------------------------.
// External functions.
// ----------------------------------------------------------------.
DLL_API int ext_add (int a, int b) {
	return a + b;
}

DLL_API int ext_sub (int a, int b) {
	return a - b;
}
