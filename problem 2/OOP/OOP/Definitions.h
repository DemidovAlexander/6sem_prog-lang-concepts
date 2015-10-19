#pragma once

#include <string.h>
#include <stdlib.h>
#include <cstdio>

#include "Method.h"

#define VIRTUAL_CLASS( T ) struct T##_STRUCT { \
	Method table[10000];\
	size_t tableSize;
#define END_CLASS( T ) }; typedef struct T##_STRUCT T;\
	void T##_register_methods(Method* table, size_t* tableSize);

#define CONSTRUCT( T, INST ) \
	INST.tableSize = 0;\
	T##_register_methods( INST.table, &INST.tableSize );

#define DECLARE_METHOD( T, NAME ) void T##_##NAME( void* THIS );
#define DEFINE_METHOD( T, NAME ) void T##_##NAME( void* THIS ) { printf( "void %s::%s()\n", #T, #NAME );
#define END_DEFINITION }

#define REGISTER_METHOD( T, NAME, TABLE, TABLE_SIZE ) \
	TABLE[*TABLE_SIZE].methodName = #NAME;\
	TABLE[*TABLE_SIZE].func = T##_##NAME;\
	++(*TABLE_SIZE);

#define REGISTER_DERIVED_METHOD( T, NAME, TABLE, TABLE_SIZE ) \
	for (size_t i = 0; i < *TABLE_SIZE; ++i) {\
		if (strcmp(TABLE[i].methodName , #NAME) == 0) {\
			TABLE[i].func = T##_##NAME;\
		}\
	}

#define CALL_METHOD( NAME, INST ) \
	for (size_t i = 0; i < INST.tableSize; ++i) {\
	if (strcmp(INST.table[i].methodName , #NAME) == 0) {\
			INST.table[i].func( &INST );\
			break;\
		}\
	}\

#define VIRTUAL_CLASS_DERIVED( T, P ) struct T##_STRUCT : P {
#define END_CLASS_DERIVED( T, P ) }; typedef struct T##_STRUCT T;\
	void T##_register_methods(Method* table, size_t* tableSize);

#define CONSTRUCT_DERIVED_CLASS( T, P, INST ) \
	INST.tableSize = 0;\
	P##_register_methods( INST.table, &INST.tableSize );\
	T##_register_methods( INST.table, &INST.tableSize );