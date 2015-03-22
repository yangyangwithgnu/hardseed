// last modified 

#include "Misc.h"
#include <algorithm>
#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <ctime>
#include <unistd.h>
#include <sys/types.h>

using std::cerr;
using std::endl;
using std::make_pair;

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

// first return is the string between keyword_begin and keyword_end;
// second return is end_pos + keyword_end.size().
pair<string, size_t>
fetchStringBetweenKeywords ( const string& txt,
                             const string& keyword_begin,
                             const string& keyword_end,
                             size_t from_pos )
{
    const auto begin_pos = txt.find(keyword_begin, from_pos);
    if (string::npos == begin_pos) {
        //cerr << "WARNING! fetchStringBetweenKeywords() CANNOT find the keyword \"" << kyeword_begin << "\"" << endl;
        return(make_pair("", 0));
    }
    const auto end_pos = txt.find(keyword_end, begin_pos + keyword_begin.size());
    if (string::npos == end_pos) {
        //cerr << "WARNING! fetchStringBetweenKeywords() CANNOT find the keyword \"" << kyeword_end << "\"" << endl;
        return(make_pair("", 0));
    }


    return(make_pair( txt.substr(begin_pos + keyword_begin.size(), end_pos - begin_pos - keyword_begin.size()),
                      end_pos + keyword_end.size() ));
}

// get file size by FILE*.
// return -1 if failure
long
getFileSize (FILE* fs)
{
    // backup current offset
    long offset_bak = ftell(fs);

    // get the filesize
    fseek(fs, 0, SEEK_END);
    long file_size = ftell(fs);

    // restore last offset
    fseek(fs, offset_bak, SEEK_SET);


    return(file_size);
}

// process_name + process_id + thread_id + rand
extern char *__progname;
string
makeRandomFilename (void) 
{
    static bool b_first = true;
    if (b_first) {
        srand((unsigned)time(NULL));
        b_first = false;
    }

    const string& filename = string(__progname) + "_" +
                             convNumToStr(getpid()) + "_"
                             + convNumToStr(pthread_self()) + "_"
                             + convNumToStr(rand());

#ifdef CYGWIN
    return("c:\\" + filename);
#else
    return("/tmp/" + filename);
#endif
}
