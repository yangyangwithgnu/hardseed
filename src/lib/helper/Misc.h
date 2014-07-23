// last modified 

#pragma once

#include <sstream>
#include <string>
#include <vector>

using std::string;
using std::ostringstream;
using std::vector;


// why not std::to_string()? 
// you know, I have to port this linux code to win32 by cygwin, and there
// is a bug on cygwin case it cannot find to_string(), so, I must do it
// by myself
template<typename T>
string
convNumToStr (T num)
{
    ostringstream oss;
    oss << num;

    return(oss.str());
}

// split raw string to more sub-str by token-chars.
void
splitStr ( const string& str,
           const string& tokens_list,
           vector<string>& splited_substr_list,
           vector<char>& appeared_tokens_list );

