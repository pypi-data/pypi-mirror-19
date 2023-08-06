#include <string>
#include <istream>
#include <ostream>
#include <sstream>
#include <iterator>
#include <algorithm>
#include <vector>
#include <utility>
#include <iostream>

/*
Simple helper tool that normalizes strings using the same utf8 proc tool that's used by
the bgtfsLib. The compilation script copies the utf8 stuff from the bgtfsLib dir into this
directory. stdin is simply normalized and printed back to stdout.
*/

using namespace std;

#include "utf8proc.h"

string normalize(string query) {
  uint8_t *output = nullptr;
  int32_t error = utf8proc_map((const uint8_t *)query.c_str(), 0, &output,
			       UTF8PROC_NULLTERM | UTF8PROC_COMPOSE | UTF8PROC_CASEFOLD | UTF8PROC_STRIPMARK
			       | UTF8PROC_COMPAT | UTF8PROC_LUMP);
  if (error < 0) {
    return query;
  }
  else {
    string result = "";
    if (output != nullptr) {
      result = std::string((char*)output);
      free(output);
    }
    return result;
  }
}

bool naturalSmallerThan(const std::string& aOriginal, const std::string& bOriginal) {
  auto aNormalized = normalize(aOriginal);
  const char* a = aNormalized.c_str();
  auto bNormalized = normalize(bOriginal);
  const char* b = bNormalized.c_str();
  while (*a != '\0' and *b != '\0') {
    if (isdigit(*a) and isdigit(*b)) {
      char* end;
      auto aNumber = strtol(a, &end, 10);
      a = end;
      auto bNumber = strtol(b, &end, 10);
      b = end;
      if (aNumber != bNumber) {
	return aNumber < bNumber;
      }
    } else {
      if (*a != *b) {
	return *a < *b;
      }
      a++;
      b++;
    }
  }
  return *a < *b;
}

vector<string> naturalSorted(vector<string> strings) {
  sort(strings.begin(), strings.end(), [](const string &a, const string &b) {
      return naturalSmallerThan(a, b);
    });

    return strings;
}

vector<int> naturalSortedIndices(vector<string> strings) {
  // turn into pairs (original index)
  vector<pair<string, int>> pairs;
  int index = 0;
  for (const auto &string : strings) {
    pairs.push_back({string, index});
    index ++;
  }
  
  // sort
  sort(pairs.begin(), pairs.end(), [](const pair<string, int> &a, const pair<string, int> &b) {
      return naturalSmallerThan(a.first, b.first);
    });
    
  vector<int> result;
  result.reserve(pairs.size());
  for (auto p : pairs) {
    result.push_back(p.second);
  }
  return result;
}
