#pragma once
#include "Definitions.h" 

//базовыйкласс
VIRTUAL_CLASS( Base )
	int a;
END_CLASS( Base )
//методы
DECLARE_METHOD( Base, Both )
DECLARE_METHOD( Base, Virtual )

//класс‐наследник
VIRTUAL_CLASS_DERIVED( Derived, Base )
	int b;
END_CLASS_DERIVED( Derived, Base )
//методы
DECLARE_METHOD( Derived, Virtual )
DECLARE_METHOD( Derived, OnlyDerived )