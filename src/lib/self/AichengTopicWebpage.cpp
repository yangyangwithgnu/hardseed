// last modified 

#include "AichengTopicWebpage.h"
#include <iostream>
#include <iterator>
#include <algorithm>
#include "../helper/Misc.h"


using namespace std;

static bool
parsePicturesUrlsHelper ( const string& webpage_txt,
                          vector<string>& pictures_urls_list,
                          const string& keyword_begin,
                          const string& keyword_end ) 
{
    bool b_ok = false;

    size_t keyword_pic_begin_pos = 0;
    while (true) {
        // parse picture URL
        const pair<string, size_t>& pair_tmp = fetchStringBetweenKeywords( webpage_txt,
                                                                           keyword_begin,
                                                                           keyword_end,
                                                                           keyword_pic_begin_pos );
        string pic_url = pair_tmp.first;
        if (pic_url.empty()) {
            break;
        }
        keyword_pic_begin_pos = pair_tmp.second;
        b_ok = true;
        
        // there are some bad picture-webspaces and logo pci, ignore them
        bool b_ignore_url = false;
        static const vector<string> ignore_urls_keywords_list = {
                                                                  "iceimg.com",
                                                                };
        for (const auto& e : ignore_urls_keywords_list) {
            if (string::npos != pic_url.find(e)) {
                b_ignore_url = true;
                break;
            }
        }
        if (b_ignore_url) {
            continue;
        }
        
        // convert https to http
        static const string keyword_https("https://");
        const auto https_pos = pic_url.find(keyword_https);
        if (string::npos != https_pos) {
            static const string keyword_http("http://");
            pic_url.replace(https_pos, keyword_https.size(), keyword_http);
        }
        
        // save the picture URL
        pictures_urls_list.push_back(pic_url);
    }

    return(b_ok);
}

static bool
parsePicturesUrls (const string& webpage_txt, vector<string>& pictures_urls_list) 
{
    pictures_urls_list.clear();

    // the list may be on the webpage at the same time
    static const vector<pair<string, string>> begin_and_end_keywords_list = { make_pair("<img src=\"", "\""), 
                                                                              make_pair("<img src='", "'") };
    
    bool b_ok = false;
    for (const auto& e : begin_and_end_keywords_list) {
        if (parsePicturesUrlsHelper(webpage_txt, pictures_urls_list, e.first, e.second)) {
            b_ok = true;
        }
    }


    return(b_ok);
}

static bool
parseSeedUrl (const string& webpage_txt, string& seed_url) 
{
    static const vector<string> keywords_seed_begin_list = { "http://www.jandown.com", 
                                                             "http://jandown.com", 
                                                             "http://www6.mimima.com",
                                                             "http://mimima.com" };

    for (const auto& e : keywords_seed_begin_list) {
        const string& keyword_seed_begin = e;
        static const string keyword_seed_end("\"");
        
        const pair<string, size_t>& pair_tmp = fetchStringBetweenKeywords( webpage_txt,
                                                                           keyword_seed_begin,
                                                                           keyword_seed_end );
        if (!pair_tmp.first.empty()) {
            seed_url = keyword_seed_begin + pair_tmp.first;
            return(true);
        }
    }


    return(false);
}

AichengTopicWebpage::AichengTopicWebpage (const string& url, const string& proxy_addr)
    : TopicWebpage(url, parsePicturesUrls, parseSeedUrl, proxy_addr, "gbk", "UTF-8")
{
    ;
}

AichengTopicWebpage::~AichengTopicWebpage ()
{
    ;
}

