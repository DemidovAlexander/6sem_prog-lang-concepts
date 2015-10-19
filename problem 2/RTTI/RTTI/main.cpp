#include <iostream>

#include "Classes.h"
#include "RTTI.h"

CLASS( X )
	private:
		int a;
	public:
		X() : a(23) {}
		void Print() { std::cout << "X:" << a << std::endl; }
END_CLASS

CLASS_DERIVED( Y, public X )
	private:
		int b;
	public:
		Y() : b(27) {}
		void Print() { std::cout << "Y:" << b << std::endl; }
END_CLASS

CLASS_DERIVED(Z, public Y)
	private:
		int c;
	public:
		Z() : c(31) {}
		void Print() { std::cout << "Z:" << c << std::endl; }
END_CLASS

CLASS_DERIVED(A, public X, public Y)
	private:
		int d;
	public:
		A() : d(45) {}
		void Print() { std::cout << "A:" << d << std::endl; }
END_CLASS


int main() {
	REGISTER_CLASS(X)
	REGISTER_CLASS_DERIVED(Y, X)
	REGISTER_CLASS_DERIVED(Z, Y)
	REGISTER_CLASS_DERIVED(A, X, Y)

	X *x = new X();
	x->Print();

	Y *y = new Y();
	y->Print();

	Z *z = new Z();
	z->Print();

	A *a = new A();
	a->Print();

	std::cout << TYPEID(x).name << ' ' << TYPEID(x).hash << std::endl;
	std::cout << TYPEID(y).name << ' ' << TYPEID(y).hash << std::endl;
	std::cout << TYPEID(z).name << ' ' << TYPEID(z).hash << std::endl;
	std::cout << TYPEID(a).name << ' ' << TYPEID(a).hash << std::endl;

	Y *yy;
	DYNAMIC_CAST( z, Y, yy )
	std::cout << TYPEID(yy).name << ' ' << TYPEID(yy).hash << std::endl;
	DYNAMIC_CAST( a, Y, yy )
	std::cout << TYPEID(yy).name << ' ' << TYPEID(yy).hash << std::endl;

	X *xx;
	DYNAMIC_CAST( z, X, xx )
	std::cout << TYPEID(xx).name << ' ' << TYPEID(xx).hash << std::endl;
	DYNAMIC_CAST( a, X, xx )
	std::cout << TYPEID(xx).name << ' ' << TYPEID(xx).hash << std::endl;

	X *xxx;
	DYNAMIC_CAST( z, X, xxx )
	std::cout << TYPEID(xxx).name << ' ' << TYPEID(xxx).hash << std::endl;
	xxx->Print();

	Y *yyy;
	DYNAMIC_CAST( xxx, Y, yyy )
	std::cout << TYPEID(yyy).name << ' ' << TYPEID(yyy).hash << std::endl;
	yyy->Print();

	X* xxxx;
	xxxx = new Z();
	Z* zzzz;
	std::cout << TYPEID(xxxx).name << ' ' << TYPEID(xxxx).hash << std::endl;
	DYNAMIC_CAST(xxxx, Z, zzzz)
	zzzz->Print();
		
	return 0;
}