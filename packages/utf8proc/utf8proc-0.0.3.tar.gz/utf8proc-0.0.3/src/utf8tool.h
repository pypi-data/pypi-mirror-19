
#include <string>

using namespace std;

string normalize(string query);

bool naturalSmallerThan(const string& aOriginal, const string& bOriginal);

/** list of strings, sorts them naturally, then return their indicies. Will replace "" by " ". */
vector<int> naturalSortedIndices(vector<string> strings);
vector<string> naturalSorted(vector<string> strings);