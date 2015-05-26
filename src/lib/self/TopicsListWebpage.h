// last modified 

#pragma once

#include <string>
#include <vector>
#include "../helper/Webpage.h"

using std::string;
using std::vector;
using std::pair;


class TopicsListWebpage : public Webpage
{
    public:
        // callback function for parse titles and URLs of topics
        typedef bool (*ParseTitlesAndUrls) ( const string& webpage_txt,
                                             const string& portal_url, 
                                             vector<pair<string, string>>& titles_and_urls_list ); 
        // callback function for parse next topicslist URL
        typedef bool (*ParseNextpageUrl) ( const string& webpage_txt,
                                           const string& portal_url, 
                                           string& nextpage_url ); 

    public:
        TopicsListWebpage ( const string& portal_url,
                            const string& url,
                            ParseTitlesAndUrls parseTitlesAndUrls,
                            ParseNextpageUrl parseNextpageUrl,
                            const string& proxy_addr = "",
                            const string& src_charset = "",
                            const string& dest_charset = "" );
        virtual ~TopicsListWebpage ();
        const vector<pair<string, string>>& getTitlesAndUrlsList (void) const;
        const string& getNextpageUrl (void) const;
        const string& getPortalWebpageUrl (void) const;


    private:
        vector<pair<string, string>> titles_and_urls_list_;
        string nextpage_url_;
        const string portal_url_;
};
