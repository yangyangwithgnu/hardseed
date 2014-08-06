// last modified 

#include "RmdownSeedWebpage.h"
#include <iostream>
#include <algorithm>
#include <unistd.h>
#include "../helper/Misc.h"


using namespace std;

static bool
parsePostMultiSections ( const string& webpage_txt,
                         vector<pair<string, string>>& post_sections_list ) 
{
    // parse the ref section
    static const string& keyword_ref_section_begin("<INPUT size=58 name=\"ref\" value=\"");
    static const string& keyword_ref_section_end("\"");
    const pair<string, size_t>& pair_tmp = fetchStringBetweenKeywords( webpage_txt,
                                                                       keyword_ref_section_begin,
                                                                       keyword_ref_section_end );
    const string& ref_content = pair_tmp.first;
    if (ref_content.empty()) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword "
             << "\"" << keyword_ref_section_begin << "\"" << " and "
             << "\"" << keyword_ref_section_end << "\"" << endl;
        return(false);
    }
    post_sections_list.push_back(make_pair("ref", ref_content));
    const auto keyword_ref_section_end_pos = pair_tmp.second;

    // parse the reff section
    static const string& keyword_reff_section_begin("value=\"");
    static const string& keyword_reff_section_end("\"");
    const pair<string, size_t>& pair_tmp2 = fetchStringBetweenKeywords( webpage_txt,
                                                                       keyword_reff_section_begin,
                                                                       keyword_reff_section_end,
                                                                       keyword_ref_section_end_pos );
    const string& reff_content = pair_tmp2.first;
    if (reff_content.empty()) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword "
             << "\"" << keyword_reff_section_begin << "\"" << " and "
             << "\"" << keyword_reff_section_end << "\"" << endl;
        return(false);
    }
    post_sections_list.push_back(make_pair("reff", reff_content));


    return(true);
}

// seed fetch URL. http://www.rmdown.com/ and http://www.xunfs.com/ are
// the same one website, on the other word, from http://www.rmdown.com/abcd
// download the seed file same as from http://www.xunfs.com/abcd, so, I need
// just ONE fetch URL 
RmdownSeedWebpage::RmdownSeedWebpage (const string& url, const string& proxy_addr)
    : SeedWebpage(url, proxy_addr, "http://www.rmdown.com/download.php", parsePostMultiSections)
{
    ;
}

RmdownSeedWebpage::~RmdownSeedWebpage ()
{
    ;
}

