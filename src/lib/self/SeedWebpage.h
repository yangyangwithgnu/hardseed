// last modified 

#pragma once

#include <string>
#include <vector>
#include "../helper/Webpage.h"

using std::string;
using std::vector;
using std::pair;


class SeedWebpage : public Webpage
{
    public:
        // callback function for parse the multi sections of post 
        typedef bool (*ParsePostMultiSections) ( const string& webpage_txt,
                                                 vector<pair<string, string>>& post_sections_list ); 

    public:
        SeedWebpage ( const string& url,
                      const string& proxy_addr,
                      const string& post_url,
                      ParsePostMultiSections parsePostMultiSections );
        virtual ~SeedWebpage ();
        bool downloadSeed (const string& path, const string& base_name);

    private:
        const string post_url_; 
        vector<pair<string, string>> post_sections_list_;
};
