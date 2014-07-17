// last modified 

#include "RmdownSeedWebpage.h"
#include <iostream>
#include <algorithm>
#include <unistd.h>

using namespace std;

static bool
parsePostMultiSections ( const string& webpage_txt,
                         vector<pair<string, string>>& post_sections_list ) 
{
    // parse the ref section
    static const string& keyword_ref_section("<INPUT size=58 name=\"ref\" value=\"");
    const auto keyword_ref_section_begin_pos = webpage_txt.find(keyword_ref_section);
    if (string::npos == keyword_ref_section_begin_pos) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword \""
             << keyword_ref_section << endl;
        return(false);
    }
    const auto keyword_ref_section_end_pos = webpage_txt.find("\"", keyword_ref_section_begin_pos + keyword_ref_section.size());
    if (string::npos == keyword_ref_section_end_pos) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword _\"_" << endl;
        return(false);
    }
    const string ref_content = webpage_txt.substr(  keyword_ref_section_begin_pos + keyword_ref_section.size(),
                                                    keyword_ref_section_end_pos - keyword_ref_section_begin_pos - keyword_ref_section.size() );
    post_sections_list.push_back(make_pair("ref", ref_content));

    // parse the reff section
    static const string& keyword_reff_section("value=\"");
    const auto keyword_reff_section_begin_pos = webpage_txt.find(keyword_reff_section, keyword_ref_section_end_pos);
    if (string::npos == keyword_reff_section_begin_pos) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword _" << keyword_reff_section << "_" << endl;
        return(false);
    }
    const auto keyword_reff_section_end_pos = webpage_txt.find("\"", keyword_reff_section_begin_pos + keyword_reff_section.size());
    if (string::npos == keyword_reff_section_end_pos) {
        cerr << "WARNING! parsePostMultiSections() CANNOT find the keyword _\"_" << endl;
        return(false);
    }
    const string reff_content = webpage_txt.substr( keyword_reff_section_begin_pos + keyword_reff_section.size(),
                                                    keyword_reff_section_end_pos - keyword_reff_section_begin_pos - keyword_reff_section.size() );
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

