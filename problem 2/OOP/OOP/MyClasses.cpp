#include "Definitions.h" 
#include "MyClasses.h" 
#include <cstdio>

//Base class methods

//Both
DEFINE_METHOD( Base, Both )
	printf( "a = %d\n", ((Base*)(THIS))->a);
END_DEFINITION

//Virtual base
DEFINE_METHOD( Base, Virtual )
	printf( "Base\n");
END_DEFINITION

//Derived class methods

//OnlyDerived
DEFINE_METHOD( Derived, OnlyDerived )
	printf( "b = %d\n", ((Derived*)(THIS))->b);
END_DEFINITION

//Virtual derived
DEFINE_METHOD( Derived, Virtual )
	printf( "Derived\n");
END_DEFINITION


void Base_register_methods(Method* table, size_t* tableSize) {
	REGISTER_METHOD( Base, Both, table, tableSize) 
	REGISTER_METHOD( Base, Virtual, table, tableSize )
}


void Derived_register_methods(Method* table, size_t* tableSize) {
	REGISTER_DERIVED_METHOD( Derived, Virtual, table, tableSize )
	REGISTER_METHOD( Derived, OnlyDerived, table, tableSize )
}

