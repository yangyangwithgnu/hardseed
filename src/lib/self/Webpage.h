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
                           const unsigned retry_sleep_second = 2 );
        virtual ~Webpage ();
        
        const string& getTxt (void) const;
        const string& getTitle (void) const;
        //const string& getUrl (void) const;
        
        long getLatestHttpStatusCode (void) const;
        bool isValidLatestHttpStatusCode (void) const; 
        
        const string& getHttpHeader (void) const;
        const string& getRemoteFiletype (void) const;
        const string& getRemoteFilesize (void) const;
        const string& getRemoteFilename (void) const;
        const string& getRemoteFiletime (void) const;
        
        bool isLoaded (void) const;
        size_t convertCharset (const string& src_charset, const string& dest_charset);
        bool saveasFile (const string& filename) const;
        
        bool downloadFile ( const string& url,
                            const string& filename,
                            const string& referer = "",
                            const unsigned timeout_second = 0,
                            const unsigned retry_times = 2,
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
        void requestHttpHeader_ (void);
        bool download_ ( const string& raw_url,
                         const string& filename,
                         const string& referer,
                         const unsigned timeout_second,
                         const unsigned retry_times,
                         const unsigned retry_sleep_second );
        long parseLatestHttpStatusCode_ (void);

    private:
        CURL* p_curl_;
        string url_;
        char libcurl_err_info_buff_[CURL_ERROR_SIZE];
        string proxy_addr_;
        string http_header_;
        string remote_filetype_;
        string remote_filesize_;
        string remote_filename_;
        string remote_filetime_;
        string txt_;
        string title_;
        bool b_loaded_ok_;
        long latest_http_status_code_;
};

