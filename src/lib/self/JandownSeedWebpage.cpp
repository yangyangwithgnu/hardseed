// last modified 

#include "JandownSeedWebpage.h"
#include <iostream>
#include <algorithm>
#include <unistd.h>

using namespace std;

static bool
parsePostMultiSections ( const string& webpage_txt,
                         vector<pair<string, string>>& post_sections_list ) 
{
    // parse the code section
    static const string& keyword_code_section_begin("<input type=text name=code size=30 value=");
    const auto keyword_code_section_begin_pos = webpage_txt.find(keyword_code_section_begin);
    if (string::npos == keyword_code_section_begin_pos) {
        cerr << "WARNING! JandownSeedWebpage::JandownSeedWebpage() CANNOT find the keyword \""
             << keyword_code_section_begin << endl;
        return(false);
    }
    static const string& keyword_code_section_end(" >");
    const auto keyword_code_section_end_pos = webpage_txt.find( keyword_code_section_end,
                                                                keyword_code_section_begin_pos + keyword_code_section_begin.size() );
    if (string::npos == keyword_code_section_end_pos) {
        cerr << "WARNING! JandownSeedWebpage::JandownSeedWebpage() CANNOT find the keyword \""
             << keyword_code_section_end << endl;
        return(false);
    }
    const string ref_content = webpage_txt.substr( keyword_code_section_begin_pos + keyword_code_section_begin.size(),
                                                   keyword_code_section_end_pos - keyword_code_section_begin_pos - keyword_code_section_begin.size() );
    post_sections_list.push_back(make_pair("code", ref_content));


    return(true);
}

// seed fetch URL. http://www.jandown.com/ and http://www6.mimima.com/ are
// the same one website, on the other word, from http://www.jandown.com/abcd
// download the seed file same as from http://www6.mimima.com/abcd, so, I need
// just ONE fetch URL 
JandownSeedWebpage::JandownSeedWebpage (const string& url, const string& proxy_addr)
    : SeedWebpage(url, proxy_addr, "http://www.jandown.com/fetch.php", parsePostMultiSections)
{
    ;
}

JandownSeedWebpage::~JandownSeedWebpage ()
{
    ;
}

