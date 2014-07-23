// last modified 

#include "Aicheng.h"
#include <iostream>
#include <iomanip>
#include <algorithm>
#include <iterator>
#include <thread>
#include <mutex>
#include <cstdlib>
#include <unistd.h>
#include "AichengTopicsListWebpage.h"
#include "AichengTopicWebpage.h"
#include "JandownSeedWebpage.h"
#include "../helper/RichTxt.h"


using namespace std;


static mutex g_mtx;

static const string&
getPortalWebpageUrl (void) 
{
    static const string portal_url("http://www.ac168.info/bt/simple/");
    return(portal_url);
}

static const string&
getTopicsListWebpagePartUrl (Aicheng::AvClass av_class) 
{
    static const string west_part_url("index.php?f5.html");
    static const string cartoon_part_url("index.php?f6.html");
    static const string asia_mosaicked_part_url("index.php?f4.html");
    static const string asia_non_mosaicked_part_url("index.php?f16.html");

    switch (av_class) {
        case Aicheng::west: 
            return(west_part_url);
        case Aicheng::cartoon: 
            return(cartoon_part_url);
        case Aicheng::asia_mosaicked: 
            return(asia_mosaicked_part_url);
        case Aicheng::asia_non_mosaicked: 
            return(asia_non_mosaicked_part_url);
    }
}

static const string
getTopicsListWebpageUrl (Aicheng::AvClass av_class) 
{
    return(getPortalWebpageUrl() + getTopicsListWebpagePartUrl(av_class));
}

static bool
isThereInList ( const string& webpage_title,
                const vector<string>& ignore_keywords_list,
                string& which_keyword )
{
    for (const auto& e : ignore_keywords_list) {
        if (!e.empty() && string::npos != webpage_title.find(e)) {
            which_keyword = e;
            return(true);
        }
    }

    return(false);
}

static bool
parseValidTopicsUrls ( Aicheng::AvClass av_class,
                       const string& proxy_addr,
                       unsigned range_begin, unsigned range_end,
                       const vector<string>& hate_keywords_list,
                       const vector<string>& like_keywords_list,
                       vector<string>& valid_topics_urls_list,
                       bool b_progress )
{
    valid_topics_urls_list.clear();

    string current_url = getTopicsListWebpageUrl(av_class);
    bool b_stop = false;
    unsigned topics_cnt = 0;
    while (!current_url.empty() && !b_stop) {
        AichengTopicsListWebpage aicheng_topicslist_webpage(current_url, proxy_addr);
        if (!aicheng_topicslist_webpage.isLoaded()) {
            return(false);
        }
        
        const vector<pair<string, string>>& topics_title_and_url = aicheng_topicslist_webpage.getTitlesAndUrlsList();
        for (const auto& e : topics_title_and_url) {
            if (++topics_cnt > range_end) {
                b_stop = true;
                break;
            }
            
            const string& topic_title = e.first;
            const string& topic_url = e.second;
            static const string o_flag(RichTxt::bold_on + "O" + RichTxt::bold_off);
            static const string x_flag("x");
            
            // ignore the topics which do not in range
            if (topics_cnt < range_begin) {
                if (b_progress) {
                    cout << x_flag << " " << flush;
                }
                continue;
            }
            // ignore the topics which contain hate keyword by user set
            string which_keyword;
            if (isThereInList(topic_title, hate_keywords_list, which_keyword)) { 
                if (b_progress) {
                    cout << x_flag << " " << flush;
                }
                continue;
            }
            // ignore the topics which do not contain like keyword by user set
            if ( !like_keywords_list.empty() &&
                 !isThereInList(topic_title, like_keywords_list, which_keyword) ) { 
                if (b_progress) {
                    cout << x_flag << " " << flush;
                }
                continue;
            }
            
            valid_topics_urls_list.push_back(topic_url);
            
            if (b_progress) {
                cout << o_flag << " " << flush;
            }
        }
        
        current_url = aicheng_topicslist_webpage.getNextpageUrl();
    }


    return(true);
}

static void
downloadTopicPicsAndSeed ( const string& topic_url,
                           const string& proxy_addr,
                           const string& path,
                           unsigned timeout_download_pic,
                           bool b_show_info )
{
    AichengTopicWebpage aicheng_topics_webpage(topic_url, proxy_addr);

    // ready for the basename of pictures and seed.
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    string base_name; // from topic title

    // 0) delete the web logo info;
    // 1) clear the "/" in topictitle string, if the "/" present in filename,
    // linux will treat it as directory, again, clear the "\" for windows;
    static const vector<string> keyword_logos_list = { " 亚洲无码区 bt下载 - powered by phpwind.net",
                                                       " 亚洲有码区 bt下载 - powered by phpwind.net",
                                                       " 欧美区 bt下载 - powered by phpwind.net",
                                                       " 动漫区 bt下载 - powered by phpwind.net" };
    const string& topic_webpage_title = aicheng_topics_webpage.getTitle();
    auto keyword_logo_pos = string::npos;
    for (const auto& f : keyword_logos_list) {
        keyword_logo_pos = topic_webpage_title.find(f);
        if (string::npos != keyword_logo_pos) {
            break;
        }
    }
    remove_copy_if( topic_webpage_title.cbegin(),
                    (string::npos == keyword_logo_pos) ? topic_webpage_title.cend() : topic_webpage_title.cbegin() + (int)keyword_logo_pos,
                    back_inserter(base_name),
                    [] (char ch) {return('\\' == ch || '/' == ch);} );

    // 2) the path + filename max length must less than pathconf(, _PC_NAME_MAX)
    const unsigned filename_max_length_without_postfix = (unsigned)pathconf(path.c_str(), _PC_NAME_MAX)
                                                         - string("99").size() // picture number
                                                         - string(".torrent").size();
    if (base_name.size() >= filename_max_length_without_postfix) {
        // the filename too long to create file. the way as following doesn't work, case filename encoding error: 
        // base_name.resize(filename_max_length_without_postfix - 1), because this is string on char not wstring on wchar.
        // there is another stupid way, random name from 'a' to 'z'
        base_name.resize(16);
        generate( base_name.begin(), base_name.end(), 
                  [] () {return('a' + rand() % ('z' - 'a'));} );
        base_name = "(rename)" + base_name;
    }
    // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
 
    // download all pictures
    vector<string> fail_download_pics_urls_list;
    bool b_download_pics_success = aicheng_topics_webpage.downloadAllPictures( path,
                                                                               base_name,
                                                                               timeout_download_pic,
                                                                               fail_download_pics_urls_list,
                                                                               8 );

    // download seed
    bool b_downloaded_seed_success = false;
    if (!aicheng_topics_webpage.getSeedUrl().empty()) {
        JandownSeedWebpage jan_seed_webpage(aicheng_topics_webpage.getSeedUrl(), proxy_addr);
        b_downloaded_seed_success = jan_seed_webpage.downloadSeed(path, base_name);
    }

    // show result info
    if (!b_show_info) {
        return;
    }
    static const string success_info("success");
    static const string fail_info = RichTxt::foreground_red + "failure" + RichTxt::reset_all;
    g_mtx.lock();
    cout << "  \"" << base_name << "\" - ";
    if (b_download_pics_success && b_downloaded_seed_success) {
        cout << success_info; 
    } else {
        cout << fail_info << " (download error from " << topic_url << ". ";
        if (!b_download_pics_success) {
            cout << "pictures error: ";
            copy(fail_download_pics_urls_list.cbegin(), fail_download_pics_urls_list.cend(), ostream_iterator<const string&>(cout, ", "));
            cout << "\b\b";
        }
        if (!b_downloaded_seed_success) {
            if (!b_download_pics_success) {
                cout << "; ";
            }
            cout << "seed error: " << aicheng_topics_webpage.getSeedUrl();
        }
        cout << ")";
    }
    cout << endl;
    g_mtx.unlock();
}

static const string&
getNextProxyAddr (const vector<string>& proxy_addrs_list)
{
    if (proxy_addrs_list.empty()) {
        static const string empty_str("");
        return(empty_str);
    }

    static unsigned current_pos;
    if (current_pos >= proxy_addrs_list.size()) {
        current_pos = 0;
    }
    return(proxy_addrs_list[current_pos++]);
}

Aicheng::Aicheng ( AvClass av_class,
                   const vector<string>& proxy_addrs_list,
                   unsigned range_begin, unsigned range_end,
                   const vector<string>& hate_keywords_list,
                   const vector<string>& like_keywords_list,
                   unsigned threads_total,
                   unsigned timeout_download_pic,
                   const string& path )
{
    // parse the URLs of valid topics by: range, hate keywords, like keywords
    cout << "Parse the URLs of topics from " << range_begin << " to " << range_end << ": ";
    vector<string> valid_topics_urls_list;
    parseValidTopicsUrls( av_class,
                          getNextProxyAddr(proxy_addrs_list),
                          range_begin, range_end,
                          hate_keywords_list,
                          like_keywords_list,
                          valid_topics_urls_list,
                          true );
    if (valid_topics_urls_list.empty()) {
        cout << "(There is no topic which you like) " << endl;
        return;
    }
    cout << endl << endl;

    // download all pictures and seeds of topics
    cout << "Download the pictures and seeds of topics: " << endl;
    unsigned parsed_topics_cnt = 0;
    for (unsigned i = 0; i < (valid_topics_urls_list.size() / threads_total); ++i) {
        vector<thread> threads_list;
        for (unsigned j = 0; j < threads_total; ++j) {
            ++parsed_topics_cnt;
            threads_list.push_back(thread( &downloadTopicPicsAndSeed,
                                           ref(valid_topics_urls_list[i * threads_total + j]),
                                           ref(getNextProxyAddr(proxy_addrs_list)),
                                           ref(path),
                                           timeout_download_pic,
                                           true ));
        }
        for (auto& e : threads_list) {
            if (e.joinable()) {
                e.join();
            }
        }
        
        if (!threads_list.empty()) {
            cout << setprecision(1) << setiosflags(ios::fixed);
            cout << "  " << RichTxt::bold_on << RichTxt::underline_on << "<---- "
                 << 100.0 * parsed_topics_cnt / valid_topics_urls_list.size()
                 << "% ---->" << RichTxt::underline_off << RichTxt::bold_off << endl; 
            cout << resetiosflags(ios::fixed);
        }
    }

    vector<thread> threads_list;
    for (unsigned i = (valid_topics_urls_list.size() / threads_total) * threads_total; i < valid_topics_urls_list.size(); ++i) {
        ++parsed_topics_cnt;
        threads_list.push_back(thread( &downloadTopicPicsAndSeed,
                                       ref(valid_topics_urls_list[i]),
                                       ref(getNextProxyAddr(proxy_addrs_list)),
                                       ref(path),
                                       timeout_download_pic,
                                       true ));
    }
    for (auto& e : threads_list) {
        if (e.joinable()) {
            e.join();
        }
    }
    if (!threads_list.empty()) {
        cout << setprecision(1) << setiosflags(ios::fixed);
        cout << "  " << RichTxt::bold_on << RichTxt::underline_on << "<---- "
             << 100.0 * parsed_topics_cnt / valid_topics_urls_list.size()
             << "% ---->" << RichTxt::underline_off << RichTxt::bold_off << endl; 
        cout << resetiosflags(ios::fixed);
    }

    cout << endl;
    cout << "Hey kiddo, your hot babes " << path << ", enjoy it! " << endl;
}

Aicheng::~Aicheng ()
{
    ;
}

