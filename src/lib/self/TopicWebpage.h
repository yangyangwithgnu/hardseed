// last modified 

#pragma once

#include <string>
#include <vector>
#include "Webpage.h"

using std::string;
using std::vector;


class TopicWebpage : public Webpage
{
    public:
        // callback function for parse the URLs of av pictures
        typedef bool (*ParsePicturesUrls) (const string& webpage_txt, vector<string>& pictures_urls_list); 
        // callback function for parse the URLs of seed
        typedef bool (*ParseSeedUrl) (const string& webpage_txt, string& seed_url); 

    public:
        TopicWebpage ( const string& url,
                       ParsePicturesUrls parsePicturesUrls,
                       ParseSeedUrl parseSeedUrl,
                       const string& proxy_addr,
                       const string& src_charset,
                       const string& dest_charset );
        virtual ~TopicWebpage ();
        const string& getSeedUrl (void) const;
        const vector<string>& getPicturesUrlsList (void) const;
        bool downloadAllPictures ( const string& path,
                                   const string& base_name,
                                   unsigned timeout_download_pic,
                                   vector<string>& fail_download_pics_urls_list,
                                   unsigned pictures_max_num = 32 );

    private:
        string seed_url_;
        vector<string> pictures_urls_list_;
};

