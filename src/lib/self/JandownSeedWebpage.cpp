// last modified 

#include "JandownSeedWebpage.h"
#include <iostream>
#include <algorithm>
#include <unistd.h>
#include "../helper/Misc.h"


using namespace std;

static bool
parsePostMultiSections ( const string& webpage_txt,
                         vector<pair<string, string>>& post_sections_list ) 
{
    // parse the code section
    static const string keyword_code_section_begin("<input type=text name=code size=30 value=");
    static const string keyword_code_section_end(" >");
    const pair<string, size_t>& pair_tmp = fetchStringBetweenKeywords( webpage_txt,
                                                                       keyword_code_section_begin,
                                                                       keyword_code_section_end );
    const string& ref_content = pair_tmp.first;
    if (ref_content.empty()) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword "
             << "\"" << keyword_code_section_begin << "\"" << " and "
             << "\"" << keyword_code_section_end << "\"" << endl;
        return(false);
    }

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

