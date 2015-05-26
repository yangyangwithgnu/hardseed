// last modified 

#pragma once

#include <string>
#include <vector>

using std::string;
using std::vector;


class Aicheng
{
    public:
        enum AvClass {west, cartoon, asia_mosaicked, asia_non_mosaicked};

    public:
        Aicheng ( const string& portal_url,
                  AvClass av_class,
                  const vector<string>& proxy_addrs_list,
                  unsigned range_begin, unsigned range_end,
                  const vector<string>& hate_keywords_list,
                  const vector<string>& like_keywords_list,
                  unsigned threads_total,
                  unsigned timeout_download_pic,
                  const string& path );
        virtual ~Aicheng ();
        
        const string& getPortalWebpageUrl (void) const;


    private:
        const string portal_url_;
};

