// last modified 

#pragma once

#include <string>
#include <vector>

using std::string;
using std::vector;


class Caoliu
{
    public:
        enum AvClass { west_reposted, cartoon_reposted, asia_mosaicked_reposted, asia_non_mosaicked_reposted,
                       west_original, cartoon_original, asia_mosaicked_original, asia_non_mosaicked_original,
                       selfie };

    public:
        Caoliu ( AvClass av_class,
                 const vector<string>& proxy_addrs_list,
                 unsigned range_begin, unsigned range_end,
                 const vector<string>& hate_keywords_list,
                 const vector<string>& like_keywords_list,
                 unsigned threads_total,
                 unsigned timeout_download_pic,
                 const string& path );
        virtual ~Caoliu ();
};

