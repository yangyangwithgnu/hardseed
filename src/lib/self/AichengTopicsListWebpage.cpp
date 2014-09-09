// last modified 

#include "AichengTopicsListWebpage.h"
#include <iostream>
#include <cstdlib>
#include "../helper/Misc.h"


using namespace std;


static const string&
getPortalWebpageUrl (void) 
{
    static const string portal_url("http://www.ac168.info/bt/");
    return(portal_url);
}

static bool
parseTitlesAndUrls ( const string& webpage_txt,
                     vector<pair<string, string>>& titles_and_urls_list ) 
{
    const unsigned size_back = titles_and_urls_list.size();

    size_t keyword_topic_url_begin_pos = 0, keyword_topic_url_end_pos = 0;
    static const vector<string> rule_topic_keywords_list = { "防止盗号", "版规", "求 片 區" }; // "防止盗号" must be the first, because
                                                                                               // "版规" and "防止盗号" successively appear
                                                                                               // in the same topics list webpage
                                                                                               // http://www.ac168.info/bt/simple/index.php?f16.html
    for (const auto& e : rule_topic_keywords_list) {
        keyword_topic_url_begin_pos = webpage_txt.find(e);
        if (string::npos != keyword_topic_url_begin_pos) {
            break;
        }
    }
    if (string::npos == keyword_topic_url_begin_pos) {
        keyword_topic_url_begin_pos = 0;
    }

    while (true) {
        // parse topic URL
        static const string keyword_topic_url_begin("<li><a href=\"");
        static const string keyword_topic_url_end("\">");
        const pair<string, size_t>& pair_url = fetchStringBetweenKeywords( webpage_txt,
                                                                           keyword_topic_url_begin,
                                                                           keyword_topic_url_end,
                                                                           keyword_topic_url_begin_pos );
        const string& topic_url_part = pair_url.first;
        if (topic_url_part.empty()) {
            break;
        }
        const string topic_url = getPortalWebpageUrl() + topic_url_part;
        keyword_topic_url_end_pos = pair_url.second;
        
        // parse topic title
        static const string keyword_topic_title_begin("\">");
        static const string keyword_topic_title_end("</a>");
        const pair<string, size_t>& pair_title = fetchStringBetweenKeywords( webpage_txt,
                                                                             keyword_topic_title_begin,
                                                                             keyword_topic_title_end,
                                                                             keyword_topic_url_end_pos - keyword_topic_title_begin.size() );
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

    static const string keyword_nextpage_begin("</b>&nbsp; <a href=");
    static const string keyword_nextpage_end(">");
    const string& nextpage_url_part = fetchStringBetweenKeywords( webpage_txt,
                                                                  keyword_nextpage_begin,
                                                                  keyword_nextpage_end ).first;
    if (nextpage_url_part.empty()) {
        return(false);
    }

    nextpage_url = getPortalWebpageUrl() + nextpage_url_part;
    
    return(true);
}

AichengTopicsListWebpage::AichengTopicsListWebpage (const string& url, const string& proxy_addr)
    : TopicsListWebpage(url, parseTitlesAndUrls, parseNextpageUrl, proxy_addr, "gbk", "UTF-8")
{
    ;
}

AichengTopicsListWebpage::~AichengTopicsListWebpage ()
{
    ;
}

