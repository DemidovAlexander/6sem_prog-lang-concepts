#include "Definitions.h"
#include "MyClasses.h"

int main() {
	Base base;
	CONSTRUCT( Base, base )
	base.a = 0;

	Derived derived;
	CONSTRUCT_DERIVED_CLASS( Derived, Base, derived )
	derived.b = 1;
	derived.a = 1;

	CALL_METHOD(Both, base)
	CALL_METHOD(Both, derived)

	CALL_METHOD(OnlyDerived, derived)

	CALL_METHOD(Virtual, base)
	CALL_METHOD(Virtual, derived)

	Base reallyDerived = *(reinterpret_cast<Base*>(&derived));

	CALL_METHOD(Both, reallyDerived)
	CALL_METHOD(Virtual, reallyDerived)

	return 0;
}