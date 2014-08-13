// last modified 

#pragma once

#include <string>
#include <vector>
#include <curl/curl.h>

using std::string;
using std::vector;
using std::pair;

class Webpage
{
    public:
        explicit Webpage ( const string& url,
                           const string& filename = "",
                           const string& proxy_addr = "",
                           const unsigned timeout_second = 16,
                           const unsigned retry_times = 2,
                           const unsigned retry_sleep_second = 2,
                           const string& user_agent = "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0" );
        virtual ~Webpage ();
        
        string getProxyAddr (void) const;
        string checkProxyOutIpByThirdparty (void) const; 
        string checkProxyOutRegionByThirdparty (void) const; 
        
        string getUserAgent (void) const;
        string checkUserAgentByThirdparty (void) const; 
        
        const string& getTxt (void) const;
        const string& getTitle (void) const;
        
        long getLatestHttpStatusCode (void) const;
        bool isValidLatestHttpStatusCode (void) const; 
        
        string getHttpHeader (const string& url) const;
        string getRemoteFiletype (const string& url) const;
        string getRemoteFilecharset (const string& url) const;
        string getRemoteFilesize (const string& url) const;
        string getRemoteFilename (const string& url) const;
        string getRemoteFiletime (const string& url) const;
        
        bool isLoaded (void) const;
        size_t convertCharset (const string& src_charset, const string& dest_charset);
        bool saveasFile (const string& filename) const;
        
        bool downloadFile ( const string& url,
                            const string& filename,
                            const string& referer = "",
                            const unsigned timeout_second = 0,
                            const unsigned retry_times = 4,
                            const unsigned retry_sleep_second = 2);
        bool submitMultiPost ( const string& url,
                               const string& filename,
                               const vector<pair<string, string>>& post_sections_list,
                               const unsigned timeout_second = 32,
                               const unsigned retry_times = 2,
                               const unsigned retry_sleep_second = 2 );
        
        string escapeUrl (const string& raw_url) const;
        string unescapeHtml (const string& raw_txt) const;

    private:
        bool download_ ( const string& raw_url,
                         const string& filename,
                         const string& referer,
                         const unsigned timeout_second,
                         const unsigned retry_times,
                         const unsigned retry_sleep_second );
        long parseLatestHttpStatusCode_ (void);

    private:
        enum HttpHeader_ {header, type, charset, length, name, modified};
        string requestHttpHeader_ ( const string& raw_url,
                                    HttpHeader_ header_item,
                                    const unsigned timeout_second = 4,
                                    const unsigned retry_times = 2,
                                    const unsigned retry_sleep_second = 2 ) const;

    private:
        CURL* p_curl_;
        string url_;
        char libcurl_err_info_buff_[CURL_ERROR_SIZE];
        string proxy_addr_;
        string txt_;
        string title_;
        bool b_loaded_ok_;
        long latest_http_status_code_;
        const string user_agent_;
};

