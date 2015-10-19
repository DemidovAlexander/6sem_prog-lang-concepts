#pragma once

#include <string>
#include <map>
#include <set>
#include <queue>

int hashCounter = 0;
std::map< std::string, std::set<std::string> > tree;
std::map< std::string, int > hashes;

class TypeId {
public:
	std::string name;
	int hash;

	bool operator==(const TypeId &other) const {
		return hash == other.hash;
	}

	bool operator!=(const TypeId &other) const {
		return !( *this == other );
	}
};

int getClassHash(std::string &className) {
	if (hashes.find(className) == hashes.end()) {
		hashes[className] = hashCounter++;
	} 
	return hashes[className];
}

bool checkPath(std::string &source, std::string &destination) {
	if (source == destination) {
		return true;
	}
	
	std::set<std::string> used;
	std::queue<std::string> queue;

	queue.push(source);
	
	while (!queue.empty()) {
		used.insert(queue.front());
		for (std::string neighbour : tree[queue.front()]) {
			if (neighbour == destination) {
				return true;
			}
			if (used.find(neighbour) == used.end()) {
				queue.push(neighbour);
			}
		}
		queue.pop();
	}

	return false;
}

#define DYNAMIC_CAST( SourcePointer, DestinationClass, DestinationPointer ) \
	if (checkPath((SourcePointer)->getTypeId().name, std::string(#DestinationClass))) { \
		DestinationPointer = reinterpret_cast<DestinationClass*>( (SourcePointer) ); \
	} else { \
		throw std::invalid_argument( "can't cast" ); \
	}