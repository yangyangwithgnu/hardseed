// last modified 

#include "CaoliuTopicsListWebpage.h"
#include <iostream>
#include <cstdlib>
#include "../helper/Misc.h"


using namespace std;


static const string&
getPortalWebpageUrl (void) 
{
    static const string portal_url("http://1024go.info/");
    return(portal_url);
}

static bool
parseTitlesAndUrls ( const string& webpage_txt,
                     vector<pair<string, string>>& titles_and_urls_list ) 
{
    const unsigned size_back = titles_and_urls_list.size();

    size_t keyword_topic_url_begin_pos = 0, keyword_topic_url_end_pos = 0;
    keyword_topic_url_begin_pos = webpage_txt.find("普通主題");
    if (string::npos == keyword_topic_url_begin_pos) {
        keyword_topic_url_begin_pos = 0;
    }

    while (true) {
        // parse topic URL
        static const string keyword_topic_url_begin("<h3><a href=\"");
        static const string keyword_topic_url_begin2("htm_data");
        static const string keyword_topic_url_end("\"");
        const pair<string, size_t>& pair_url = fetchStringBetweenKeywords( webpage_txt,
                                                                           keyword_topic_url_begin + keyword_topic_url_begin2,
                                                                           keyword_topic_url_end,
                                                                           keyword_topic_url_begin_pos );
        const string& topic_url_part = pair_url.first;
        if (topic_url_part.empty()) {
            break;
        }
        const string& topic_url = getPortalWebpageUrl() + keyword_topic_url_begin2 + topic_url_part;
        keyword_topic_url_end_pos = pair_url.second;
        
        // parse topic title
        static const string keyword_topic_title_begin("id=\"\">");
        static const string keyword_topic_title_end("</a></h3>");
        const pair<string, size_t>& pair_title = fetchStringBetweenKeywords( webpage_txt,
                                                                             keyword_topic_title_begin,
                                                                             keyword_topic_title_end,
                                                                             keyword_topic_url_end_pos );
        const string& topic_title = pair_title.first;
        keyword_topic_url_begin_pos = pair_title.second;
        
        // save url and title of the topic 
        titles_and_urls_list.push_back(make_pair(topic_title, topic_url));
    }

    return(titles_and_urls_list.size() > size_back);
}

static bool
parseNextpageUrl (const string& webpage_txt, string& nextpage_url) 
{
    nextpage_url.empty();

    static const string keyword_nextpage("下一頁");
    const auto keyword_nextpage_pos = webpage_txt.find(keyword_nextpage);
    if (string::npos == keyword_nextpage_pos) {
        return(false);
    }

    static const string keyword_href("href=\'");
    const auto keyword_href_pos = webpage_txt.rfind(keyword_href, keyword_nextpage_pos);
    if (string::npos == keyword_href_pos) {
        cerr << "WARNING! parseNextpageUrl() cannot find the keyword " << keyword_href << ". " << endl;
        return(false);
    }

    const auto nextpage_suburl_begin_pos = keyword_href_pos + keyword_href.size();
    const auto nextpage_suburl_end_pos = webpage_txt.find("'", nextpage_suburl_begin_pos);
    if (string::npos == nextpage_suburl_end_pos) {
        cerr << "WARNING! parseNextpageUrl() cannot find the keyword '. " << endl;
        return(false);
    }

    nextpage_url = getPortalWebpageUrl() +
                   webpage_txt.substr(nextpage_suburl_begin_pos, nextpage_suburl_end_pos - nextpage_suburl_begin_pos);
    

    return(true);
}

CaoliuTopicsListWebpage::CaoliuTopicsListWebpage (const string& url, const string& proxy_addr)
    : TopicsListWebpage(url, parseTitlesAndUrls, parseNextpageUrl, proxy_addr, "gbk", "UTF-8")
{
    ;
}

CaoliuTopicsListWebpage::~CaoliuTopicsListWebpage ()
{
    ;
}

