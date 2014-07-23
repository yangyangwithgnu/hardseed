// last modified 

#include "Misc.h"
#include <algorithm>


// split raw string to more sub-str by token-chars.
// note:
// 0) case sensitive;
// 1) if there are consecutive two token-chars in raw string, splitStr()
// will make a empty sub-str into splited_substr_list.
void
splitStr ( const string& str,
           const string& tokens_list,
           vector<string>& splited_substr_list,
           vector<char>& appeared_tokens_list )
{
    size_t begin_pos = 0, end_pos;
    while (begin_pos < str.size()) {
        const auto iter_token = find_first_of( str.cbegin() + (int)begin_pos, str.cend(),
                                               tokens_list.cbegin(), tokens_list.cend() );
        if (str.cend() == iter_token) {
            splited_substr_list.push_back(str.substr(begin_pos));
            break;
        }
        
        appeared_tokens_list.push_back(*iter_token);
        end_pos = (unsigned)(iter_token - str.cbegin());
        splited_substr_list.push_back(str.substr(begin_pos, end_pos - begin_pos));
        
        begin_pos = end_pos + 1;
    }

    if (splited_substr_list[0].empty()) {
        splited_substr_list.erase(splited_substr_list.begin());
    }
}

