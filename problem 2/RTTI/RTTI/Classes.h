#pragma once

#include <string>
#include <iostream>
#include <set>
#include <vector>
#include <sstream>

#include "RTTI.h"

std::vector< std::string > baseClasses;

void getClasses(std::string &classesString, std::vector< std::string > &baseClasses) {
	std::string newClass;

	baseClasses = std::vector< std::string >();

	std::istringstream iss(classesString, std::istringstream::in);

	while (iss >> newClass) {
		baseClasses.push_back(newClass);
	}
}

#define CLASS( Base ) \
	class Base { \
	public: \
		static TypeId getTypeId() { \
			TypeId typeId; \
			typeId.name = std::string(#Base); \
			typeId.hash = getClassHash(std::string(#Base)); \
			return typeId; \
		}

#define CLASS_DERIVED( Derived, ...) \
	class Derived : __VA_ARGS__ { \
	public: \
		static TypeId getTypeId() { \
			TypeId typeId; \
			typeId.name = std::string(#Derived); \
			typeId.hash = getClassHash(std::string(#Derived)); \
			return typeId; \
		}

#define END_CLASS \
	};

#define REGISTER_CLASS( Class ) \
	tree[std::string(#Class)] = std::set<std::string>(); \
	tree[std::string(#Class)].insert(std::string(#Class)); \

#define REGISTER_CLASS_DERIVED( Derived, ... ) \
	tree[std::string(#Derived)] = std::set<std::string>(); \
	tree[std::string(#Derived)].insert(std::string(#Derived)); \
	getClasses(std::string(#__VA_ARGS__), baseClasses); \
	for (size_t i = 0; i < baseClasses.size(); ++i) { \
		baseClasses[i].erase(std::remove(baseClasses[i].begin(), baseClasses[i].end(), ',' ), baseClasses[i].end() ); \
		tree[std::string(#Derived)].insert(baseClasses[i]); \
		tree[baseClasses[i]].insert(std::string(#Derived));\
	}


#define TYPEID( ClassPointer ) (ClassPointer)->getTypeId()