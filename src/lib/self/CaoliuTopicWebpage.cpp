// last modified 

#include "CaoliuTopicWebpage.h"
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
        
        // there are some bad picture-webspaces, ignore them
        bool bad_pic_websapce = false;
        static const vector<string> bad_pic_websapces_list = { "iceimg.com", };
        for (const auto& e : bad_pic_websapces_list) {
            if (string::npos != pic_url.find(e)) {
                bad_pic_websapce = true;
                break;
            }
        }
        if (bad_pic_websapce) {
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

    static const string begin_keyword0("<img src='");
    static const string end_keyword0("'");
    if (parsePicturesUrlsHelper(webpage_txt, pictures_urls_list, begin_keyword0, end_keyword0)) {
        return(true);
    }

    static const string begin_keyword1("input type='image' src='");
    static const string end_keyword1("'");
    if (parsePicturesUrlsHelper(webpage_txt, pictures_urls_list, begin_keyword1, end_keyword1)) {
        return(true);
    }


    return(false);
}

static bool
parseSeedUrl (const string& webpage_txt, string& seed_url) 
{
    static const vector<string> keywords_seed_begin_list = { "http://www.rmdown.com/link.php?hash=",
                                                             "http://rmdown.com/link.php?hash=",
                                                             "http://www.xunfs.com/link.php?hash=",
                                                             "http://xunfs.com/link.php?hash=" };
    for (const auto& e : keywords_seed_begin_list) {
        const string& keyword_seed_begin = e;
        static const string keyword_seed_end("</a>");
        
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

CaoliuTopicWebpage::CaoliuTopicWebpage (const string& url, const string& proxy_addr)
    : TopicWebpage(url, parsePicturesUrls, parseSeedUrl, proxy_addr, "gbk", "UTF-8")
{
    ;
}

CaoliuTopicWebpage::~CaoliuTopicWebpage ()
{
    ;
}

