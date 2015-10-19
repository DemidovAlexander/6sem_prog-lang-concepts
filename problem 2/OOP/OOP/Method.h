#pragma once


typedef void (*funcPointer)(void*);

struct Method {
	char* methodName;
	funcPointer func;
};