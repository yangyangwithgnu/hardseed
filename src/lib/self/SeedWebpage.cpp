// last modified 

#include "SeedWebpage.h"
#include <iostream>
#include <algorithm>
#include <unistd.h>

using namespace std;

SeedWebpage::SeedWebpage ( const string& url,
                           const string& proxy_addr,
                           const string& post_url,
                           ParsePostMultiSections parsePostMultiSections )
    : Webpage(url, "", proxy_addr), post_url_(post_url)
{
    if (!isLoaded()) {
        cerr << "WARNING! SeedWebpage::SeedWebpage() CANNOT load webpage \""
             << url << "\"" << endl;
        return;
    }

    // parse the post method multi sections
    parsePostMultiSections(getTxt(), post_sections_list_);
}

SeedWebpage::~SeedWebpage ()
{
    ;
}

// this is a multipart/formdata style HTTP post method
bool
SeedWebpage::downloadSeed (const string& path, const string& base_name)
{
    if (post_sections_list_.empty()) {
        return(false);
    }

    // make seed name
    static const string seed_postfix(".torrent");
    string seed_filename = path + "/" + base_name + seed_postfix;


    return(submitMultiPost(post_url_, seed_filename, post_sections_list_));
}

