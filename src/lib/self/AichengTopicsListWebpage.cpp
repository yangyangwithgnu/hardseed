// last modified 

#include "AichengTopicsListWebpage.h"
#include <iostream>
#include <cstdlib>
#include "../helper/Misc.h"


using namespace std;



static bool
parseTitlesAndUrls ( const string& webpage_txt,
                     const string& portal_url,
                     vector<pair<string, string>>& titles_and_urls_list ) 
{
    const unsigned size_back = titles_and_urls_list.size();
//cout << webpage_txt << endl;

    const auto topics_list_txt_pos = webpage_txt.find(R"(style="border-top:0">普通主题</td></tr>)");
    size_t keyword_topic_url_begin_pos = ((string::npos == topics_list_txt_pos) ? 0 : topics_list_txt_pos);
    size_t keyword_topic_url_end_pos = 0;
    //static const vector<string> rule_topic_keywords_list = { "", "版规", "求 片 區" }; // "防止盗号" must be the first, because
                                                                                               //// "版规" and "防止盗号" successively appear
                                                                                               //// in the same topics list webpage
                                                                                               //// http://www.ac168.info/bt/simple/index.php?f16.html
    //for (const auto& e : rule_topic_keywords_list) {
        //keyword_topic_url_begin_pos = webpage_txt.find(e);
        //if (string::npos != keyword_topic_url_begin_pos) {
            //break;
        //}
    //}
    //if (string::npos == keyword_topic_url_begin_pos) {
        //keyword_topic_url_begin_pos = 0;
    //}

    while (true) {
        // parse topic URL
        static const string keyword_topic_url_begin("<h3><a href=\"");
        static const string keyword_topic_url_end("\"");
        const pair<string, size_t>& pair_url = fetchStringBetweenKeywords( webpage_txt,
                                                                           keyword_topic_url_begin,
                                                                           keyword_topic_url_end,
                                                                           keyword_topic_url_begin_pos );
        const string& topic_url_part = pair_url.first;
        if (topic_url_part.empty()) {
            break;
        }
        const string topic_url = portal_url + topic_url_part;
        keyword_topic_url_end_pos = pair_url.second;
        
        // parse topic title
        static const string keyword_topic_title_begin("target=_blank>");
        static const string keyword_topic_title_end("</a></h3>");
        const pair<string, size_t>& pair_title = fetchStringBetweenKeywords( webpage_txt,
                                                                             keyword_topic_title_begin,
                                                                             keyword_topic_title_end,
                                                                             //keyword_topic_url_end_pos - keyword_topic_title_begin.size() );
                                                                             keyword_topic_url_end_pos );
        const string& topic_title = pair_title.first;
        keyword_topic_url_begin_pos = pair_title.second;
        
        // save url and title of the topic 
        titles_and_urls_list.push_back(make_pair(topic_title, topic_url));
    }

    return(titles_and_urls_list.size() > size_back);
}

static bool
parseNextpageUrl (const string& webpage_txt, const string& portal_url, string& nextpage_url) 
{
    nextpage_url.empty();

    static const string keyword_nextpage_begin("</b><a href=\"");
    static const string keyword_nextpage_end("\">");
    const string& nextpage_url_part = fetchStringBetweenKeywords( webpage_txt,
                                                                  keyword_nextpage_begin,
                                                                  keyword_nextpage_end ).first;
    if (nextpage_url_part.empty()) {
        return(false);
    }

    // portal_url 中多了 "/bt"
    nextpage_url = string(portal_url.cbegin(), portal_url.cend() - (const int)string("/bt").length()) + nextpage_url_part;
    
    return(true);
}

AichengTopicsListWebpage::AichengTopicsListWebpage (const string& portal_url, const string& url, const string& proxy_addr)
    : TopicsListWebpage(portal_url, url, parseTitlesAndUrls, parseNextpageUrl, proxy_addr, "gbk", "UTF-8")
{
    ;
}

AichengTopicsListWebpage::~AichengTopicsListWebpage ()
{
    ;
}

