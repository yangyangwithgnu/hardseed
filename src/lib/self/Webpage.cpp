// last modified 

#include "Webpage.h"
#include <iostream>
#include <algorithm>
#include <sstream>
#include <iterator>
#include <cstring>
#include <cstdlib>
#include <string>
#include <fstream>
#include <cstdio>
#include <iconv.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <curl/curl.h>
#include "../helper/Misc.h"


using namespace std;


static bool
checkErrLibcurl (const CURLcode curl_code, const char* libcurl_err_info, bool b_exit = false, bool b_show_err_info = false)
{
    bool b_success = true;
    if (CURLE_OK != curl_code) {
        if (b_show_err_info) {
            cerr << "WARNING! " << libcurl_err_info << endl;
        }
        b_success = false;
        if (b_exit) {
            exit(EXIT_FAILURE);
        }
    }
    return(b_success);
}

static CURL*
initLibcurl (const char* libcurl_err_info_buff)
{
    CURL* p_curl = nullptr;

    // libcurl global and easy init
    if (nullptr == (p_curl = curl_easy_init())) {
        cerr << "ERROR! cannot easy init libcurl. " << endl;
        exit(EXIT_FAILURE);
    }

    // the libcurl error info buffer
    if (CURLE_OK != curl_easy_setopt(p_curl, CURLOPT_ERRORBUFFER, libcurl_err_info_buff)) {
        cerr << "ERROR! " << libcurl_err_info_buff << endl;
        exit(EXIT_FAILURE);
    }

    // follow the URL redirect
    checkErrLibcurl(curl_easy_setopt(p_curl, CURLOPT_FOLLOWLOCATION, true), libcurl_err_info_buff);

    // to allow multi-threaded unix applications to still set/use all timeout options etc, without risking getting signals
    checkErrLibcurl(curl_easy_setopt(p_curl, CURLOPT_NOSIGNAL, true), libcurl_err_info_buff);

    // automatically set the Referer to redirect source
    checkErrLibcurl(curl_easy_setopt(p_curl, CURLOPT_AUTOREFERER, true), libcurl_err_info_buff);

    // Set low speed limit in bytes per second.
    // It contains the average transfer speed in bytes per second that the transfer should be below
    // during CURLOPT_LOW_SPEED_TIME seconds for libcurl to consider it to be too slow and abort.
    // The default is 8KB/s.
    checkErrLibcurl(curl_easy_setopt(p_curl, CURLOPT_LOW_SPEED_LIMIT, 8 * 1024), libcurl_err_info_buff);

    //// display libcurl action info
    //checkErrLibcurl(curl_easy_setopt(p_curl, CURLOPT_VERBOSE, true), libcurl_err_info_buff);


    return(p_curl);
}

static void
cleanupLibcul (CURL* p_curl)
{
    curl_easy_cleanup(p_curl);
}

// check proxy by http://ip38.com
static pair<string, string>
parseProxyOutIpAndRegionByThirdparty (const string& proxy_addr)
{
    static const string thirdparty("http://ip38.com");
    Webpage webpage(thirdparty, "", proxy_addr, 16, 2, 2);
    if (!webpage.isLoaded()) {
        //cerr << "ERROR! " << thirdparty << " loaded failure. " << endl;
        return(make_pair("", ""));
    }

    webpage.convertCharset("GBK", "UTF-8");
    const string& webpage_txt = webpage.getTxt();

    static const string keyword_outip_begin("<font color=#FF0000>");
    static const string keyword_outip_end("</font>");
    const pair<string, size_t> pair_tmp = fetchStringBetweenKeywords( webpage_txt,
                                                                      keyword_outip_begin,
                                                                      keyword_outip_end );
    const string outip = pair_tmp.first;
    const size_t outip_end_pos = pair_tmp.second;

    static const string keyword_region_begin("来自：<font color=#FF0000>");
    static const string keyword_region_end("</font>");
    const string region = fetchStringBetweenKeywords( webpage_txt,
                                                      keyword_region_begin,
                                                      keyword_region_end,
                                                      outip_end_pos ).first;


    return(make_pair(outip, region));
}

string
Webpage::checkProxyOutIpByThirdparty (void) const
{
    return(parseProxyOutIpAndRegionByThirdparty(proxy_addr_).first);
}

string
Webpage::checkProxyOutRegionByThirdparty (void) const
{
    return(parseProxyOutIpAndRegionByThirdparty(proxy_addr_).second);
}

string
Webpage::getProxyAddr (void) const
{
    return(proxy_addr_);
}

string
Webpage::getUserAgent (void) const
{
    return(user_agent_);
}

// check user agent by http://www.useragentstring.com/index.php string
string
Webpage::checkUserAgentByThirdparty (void) const
{
    static const string thirdparty("http://www.useragentstring.com");
    Webpage webpage(thirdparty, "", "", 16, 2, 2, user_agent_);
    if (!webpage.isLoaded()) {
        //cerr << "ERROR! " << thirdparty << " loaded failure. " << endl;
        return("");
    }

    static const string keyword_user_agent_begin("<textarea name=\'uas\' id=\'uas_textfeld\' rows=\'4\' cols=\'30\'>");
    static const string keyword_user_agent_end("</textarea>");
    const string user_agent = fetchStringBetweenKeywords( webpage.getTxt(),
                                                          keyword_user_agent_begin,
                                                          keyword_user_agent_end ).first;


    return(user_agent);
}

// some chars invalid in URL string, such as, space char, chinese char, so I have to
// escape to legal URL.
// OK, curl_easy_escape() likely do this job, but it's stupid: the function converts
// all characters that are not a-z, A-Z, 0-9, '-', '.', '_' or '~' to their "URL escaped"
// version (%NN where NN is a two-digit hexadecimal number), in the other words, it always
// convert ':', '/', '?', and so on, that's a bad news. 
// This is my way to escape URL:
// 0) split one raw URL string to more sub-string by token chars, such as ':', '/', '='
// and '?' (may be more);
// 1) escape all sub-str by curl_easy_escape();
// 2) splice escaped sub-string to URL.
string
Webpage::escapeUrl (const string& raw_url) const
{
    // split one raw URL string to more sub-string by token chars
    static const string tokens_list(":/=?&,;%");
    vector<string> splited_substr_list;
    vector<char> appeared_tokens_list;
    splitStr(raw_url, tokens_list, splited_substr_list, appeared_tokens_list);

    // escape all sub-string
    vector<string> escaped_substr_list;
    for (const auto& e : splited_substr_list) {
        char* p_str_escaped = curl_easy_escape(p_curl_, e.c_str(), 0);
        if (nullptr == p_str_escaped) {
            cerr << "WARNING! " << libcurl_err_info_buff_ << endl;
        }
        escaped_substr_list.push_back(p_str_escaped);
        curl_free(p_str_escaped);
    }

    // splice escaped sub-string to URL
    string url_escaped;
    bool b_tokens_first = (string::npos != tokens_list.find(raw_url[0]));
    for (unsigned i = 0; i < escaped_substr_list.size() && i < appeared_tokens_list.size(); ++i) {
        if (b_tokens_first) {
            url_escaped += appeared_tokens_list[i] + escaped_substr_list[i];
        } else {
            url_escaped += escaped_substr_list[i] + appeared_tokens_list[i];
        } }
    if (escaped_substr_list.size() > appeared_tokens_list.size()) {
        url_escaped += escaped_substr_list[escaped_substr_list.size() - 1];
    }


    return(url_escaped);
}

string
Webpage::unescapeHtml (const string& raw_txt) const
{
    string unescaped_html_str = raw_txt;

    // more see http://www.theukwebdesigncompany.com/articles/entity-escape-characters.php
    static const vector<pair<string, string>> escaped_html_chars_list = { make_pair("&apos;", "'"),
                                                                          make_pair("&quot;", "\""),
                                                                          make_pair("&amp;", "&"),
                                                                          make_pair("&lt;", "<"),
                                                                          make_pair("&gt;", ">"),
                                                                          make_pair("&nbsp;", " "),
                                                                          make_pair("&#160;", " "),
                                                                          make_pair("&#12539;", "・"),
                                                                          make_pair("&#9711;", "◯"),
                                                                          make_pair("&#9834;", "♪"),
                                                                          make_pair("&#39;", "'") };

    bool b_find;
    size_t pos = 0;
    do {
        b_find = false;
        for (const auto& e : escaped_html_chars_list) {
            pos = 0;
            const string& escaped_str = e.first, unescaped_str = e.second;
            pos = unescaped_html_str.find(escaped_str, pos);
            if (string::npos != pos) {
                unescaped_html_str.replace(pos, escaped_str.size(), unescaped_str);
                b_find = true;
                break;
            }
        }
    } while (b_find);

    return(unescaped_html_str);
}

string
Webpage::requestHttpHeader_ ( const string& raw_url,
                              HttpHeader_ header_item,
                              const unsigned timeout_second,
                              const unsigned retry_times,
                              const unsigned retry_sleep_second ) const 
{
    const string random_filename = makeRandomFilename();
    FILE* fs_http_header = fopen(random_filename.c_str(), "w");
    if (nullptr == fs_http_header) {
        return("");
    }

    // deal with raw URL, first unescape html, second escape URL
    const string url = escapeUrl(unescapeHtml(raw_url));

    // timeout
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_TIMEOUT, timeout_second), libcurl_err_info_buff_);

    // get HTTP header
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_URL, url.c_str()), libcurl_err_info_buff_);
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_PROXY, proxy_addr_.c_str()), libcurl_err_info_buff_);
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_NOBODY, true), libcurl_err_info_buff_); // just request the HTTP header
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_WRITEHEADER, fs_http_header), libcurl_err_info_buff_);
    for (unsigned i = 0; i < retry_times; ++i) {
        if (checkErrLibcurl(curl_easy_perform(p_curl_), libcurl_err_info_buff_)) {
            break;
        }
        sleep(retry_sleep_second);
    }

    // reset, I.E., request HTTP body
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_NOBODY, false), libcurl_err_info_buff_);
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_WRITEHEADER, nullptr), libcurl_err_info_buff_); 
    fclose(fs_http_header);

    // load the file to memory, and parse HTTP header info
    string http_header, remote_filename, remote_filesize, remote_filetype, remote_filecharset, remote_filetime;
    static const vector<string> httpheader_keywords_list = { "Content-Type: ", // file type
                                                             "Content-Length: ", // file size
                                                             "Content-Disposition: ", // file name
                                                             "Last-Modified: " }; // file modified time
    ifstream ifs(random_filename);
    string line;
    while (getline(ifs, line)) {
        // load to memory
        http_header += (line + '\n');
        
        // parse HTTP header item
        for (const auto& e : httpheader_keywords_list) {
            const auto item_name_pos = line.find(e);
            if (string::npos == item_name_pos) {
                continue;
            }
            
            line.pop_back(); // the last char in line is '\r'
            const string& item_content = line.substr(item_name_pos + e.size());
            if ("Content-Type: " == e) {
                static const string kyeword_separator("; ");
                const auto separator_pos = item_content.find(kyeword_separator);
                if (string::npos == separator_pos) {
                    remote_filetype = item_content;
                } else {
                    remote_filetype = item_content.substr(0, separator_pos);
                    remote_filecharset = item_content.substr(separator_pos + kyeword_separator.size());
                }
            } else if ("Content-Length: " == e) {
                remote_filesize = item_content;
            } else if ("Content-Disposition: " == e) {
                remote_filename = item_content;
            } else if ("Last-Modified: " == e) {
                remote_filetime = item_content;
            }
        }
    }
    ifs.close();
    remove(random_filename.c_str()); 

    // return http header item
    switch (header_item) {
        case header: 
            return(http_header);
        case name: 
            return(remote_filename);
        case type: 
            return(remote_filetype);
        case charset: 
            return(remote_filecharset);
        case length: 
            return(remote_filesize);
        case modified: 
            return(remote_filetime);
    }
}

string
Webpage::getHttpHeader (const string& url) const
{
    return(requestHttpHeader_(url, header));
}

string
Webpage::getRemoteFiletype (const string& url) const
{
    return(requestHttpHeader_(url, type));
}

string
Webpage::getRemoteFilecharset (const string& url) const
{
    return(requestHttpHeader_(url, charset));
}

string
Webpage::getRemoteFilename (const string& url) const
{
    return(requestHttpHeader_(url, name));
}

string
Webpage::getRemoteFilesize (const string& url) const
{
    return(requestHttpHeader_(url, length));
}

string
Webpage::getRemoteFiletime (const string& url) const
{
    return(requestHttpHeader_(url, modified));
}

// once maked Webpage obj, the page in memory, but if filename is not empty,
// it will saveas file, otherwise, no file.
// notes:
// 0) no https
// 1) List of User Agent Strings, see http://www.useragentstring.com/pages/useragentstring.php
Webpage::Webpage ( const string& url,
                   const string& filename,
                   const string& proxy_addr,
                   const unsigned timeout_second,
                   const unsigned retry_times,
                   const unsigned retry_sleep_second,
                   const string& user_agent )
    : p_curl_(initLibcurl(libcurl_err_info_buff_)),
      url_(url),
      proxy_addr_(proxy_addr),
      b_loaded_ok_(false),
      user_agent_(user_agent)
{
    // set proxy.
    // proxy_addr is made up of protocol, IP and port.
    // [protocol://][IP][:port], e.g.,
    // http://127.0.0.1:8087, this is for GoAgent proxy;
    // socks4://127.0.0.1:7070, this is for ssh proxy (yes, the port is setted by ssh -D);
    // protocol support as follow: http, https, socks4, socks4a, socks5, socks5h.
    // if proxy_addr is "", disable proxy
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_PROXY, proxy_addr_.c_str()), libcurl_err_info_buff_);

    // pretend as browser
    if (!user_agent.empty()) {
        checkErrLibcurl( curl_easy_setopt(p_curl_, CURLOPT_USERAGENT, user_agent_.c_str()),
                         libcurl_err_info_buff_ );
    }

    // don't download none-webpage file when construct the obj 
    if ("text/html" != getRemoteFiletype(url_)) {
        return;
    }

    // download webpage to local file
    const string& localfile = (filename.empty() ? makeRandomFilename() : filename);
    b_loaded_ok_ = download_(url_, localfile, "", timeout_second, retry_times, retry_sleep_second);
    if (!b_loaded_ok_) {
        if (filename.empty()) {
            remove(localfile.c_str()); 
        }
        return;
    }

    // read webpage file into string
    ifstream ifs(localfile);
    string line;
    txt_.clear();
    while (getline(ifs, line)) {
        txt_ += (line + '\n');
    }
    ifs.close();

    // the caller don't care the loacl file, so delete it
    if (filename.empty()) {
        remove(localfile.c_str()); 
    }

    // parse title
    static const string title_keyword_begin("<title>"), title_keyword_end("</title>");
    title_ = unescapeHtml(fetchStringBetweenKeywords(txt_, title_keyword_begin, title_keyword_end).first);
}

Webpage::~Webpage ()
{
    cleanupLibcul(p_curl_);
}

// why same as download_()?
// for future
bool
Webpage::downloadFile ( const string& url,
                        const string& filename,
                        const string& referer,
                        const unsigned timeout_second,
                        const unsigned retry_times,
                        const unsigned retry_sleep_second )
{
    return(download_( url,
                      filename,
                      referer,
                      timeout_second,
                      retry_times,
                      retry_sleep_second ));
}

long
Webpage::parseLatestHttpStatusCode_ (void)
{
    checkErrLibcurl(curl_easy_getinfo(p_curl_, CURLINFO_RESPONSE_CODE, &latest_http_status_code_), libcurl_err_info_buff_);
    return(latest_http_status_code_);
}

long
Webpage::getLatestHttpStatusCode (void) const
{
    return(latest_http_status_code_);
}

bool
Webpage::isValidLatestHttpStatusCode (void) const
{
    // HTTP status code, 4XX stand for client error, 5XX for server error,
    // More info http://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    static const char client_error_code = '4', server_error_code = '5';
    const string& latest_http_status_code_str = convNumToStr(latest_http_status_code_);
    return( client_error_code != latest_http_status_code_str[0] && 
            server_error_code != latest_http_status_code_str[0] );
}

// download internet file to local file, such as, webpage, picture, mp3, etc.
// note: URL must be http, CANNOT be https
bool
Webpage::download_ ( const string& raw_url,
                     const string& filename,
                     const string& referer,
                     const unsigned timeout_second,
                     const unsigned retry_times,
                     const unsigned retry_sleep_second )
{
    // deal with raw URL, first unescape html, second escape URL
    string url = escapeUrl(unescapeHtml(raw_url));
        
    // convert https to http
    static const string keyword_https("https://");
    const auto https_pos = url.find(keyword_https);
    if (string::npos != https_pos) {
        static const string keyword_http("http://");
        url.replace(https_pos, keyword_https.size(), keyword_http);
    }

    // set the target URL
    curl_easy_setopt(p_curl_, CURLOPT_URL, url.c_str());

    // set the referer page.
    // note curl_easy_setopt(p_curl_, CURLOPT_REFERER, "") still send referer
    // in HTTP header (empty string ""), if you don't wanna sent referer info,
    // never touch CURLOPT_REFERER.
    if (!referer.empty()) {
        curl_easy_setopt(p_curl_, CURLOPT_REFERER, referer.c_str());
    }

    // low speed to abort.
    // If the speed below the CURLOPT_LOW_SPEED_LIMIT too long time, abort it.
    static const unsigned low_speed_timeout = 4;
    checkErrLibcurl( curl_easy_setopt(p_curl_, CURLOPT_LOW_SPEED_TIME, low_speed_timeout), 
                     libcurl_err_info_buff_ );

    // ready for downloading webpage to locale tmp file
    FILE* fs = fopen(filename.c_str(), "w+");
    if (nullptr == fs) {
        cerr << "ERROR! Webpage::download() something happened. Fail to open file " << filename << endl;
        return(false);
    }
    checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_WRITEDATA, fs), libcurl_err_info_buff_);

    // download the URL webpage to locale file
    bool b_downloaded = false;
    for (unsigned i = 0; i < retry_times; ++i) {
        // timeout to abort. if current download failured, next time
        // the download timeout increase one timeout_second
        checkErrLibcurl( curl_easy_setopt(p_curl_, CURLOPT_TIMEOUT, (long)(timeout_second * (i + 1))), 
                         libcurl_err_info_buff_ );
        
        // download
        bool b_ok = checkErrLibcurl(curl_easy_perform(p_curl_), libcurl_err_info_buff_);
        latest_http_status_code_ = parseLatestHttpStatusCode_(); // notice, parseLatestHttpStatusCode_() must
                                                                 // very close every curl_easy_perform(p_curl_)
        
        // notice, even though there is HTTP request status error, libcurl still download
        // web file success, of course, this is not real success, so, I have to check the
        // http status code
        if (b_ok && isValidLatestHttpStatusCode() && getFileSize(fs) > 0) {
            b_downloaded = true;
            break;
        } 
        
        //cerr << "WARNING! Webpage::download() something happened. Fail to download " << url
             //<< ", sleeping " << retry_sleep_second << " seconds will retry " << i + 1 << ". " << endl;
        
        // if libcurl download internet file failure,
        // the next retry will append data to local file.
        // so, I must clear the filestream by freopen(),
        // and, neither rewind() nor fseek(fs, 0L, SEEK_SET) works.
        fs = freopen(filename.c_str(), "w+", fs);
        if (nullptr == fs) {
            cerr << "ERROR! Webpage::download() something happened. Fail to reopen file " << filename << endl;
            fclose(fs);
            return(false);
        }
        sleep(retry_sleep_second);
    }
    fclose(fs);


    return(b_downloaded);
}

bool
Webpage::submitMultiPost ( const string& url,
                           const string& filename,
                           const vector<pair<string, string>>& post_sections_list,
                           const unsigned timeout_second,
                           const unsigned retry_times,
                           const unsigned retry_sleep_second)
{
    // construct the all sections for multipart/formdata style HTTP post
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    struct curl_httppost* p_first_section = nullptr;
    struct curl_httppost* p_last_section = nullptr;

    for (const auto& e : post_sections_list) {
        const string& name = e.first;
        const string& content = e.second;
        
        if (curl_formadd( &p_first_section, &p_last_section,
                          CURLFORM_PTRNAME, name.c_str(),
                          CURLFORM_PTRCONTENTS, content.c_str(),
                          CURLFORM_END )) {
            //cerr << "ERROR! RmdownSeedDownloadWebpage::downloadSeed() call curl_formadd() failure! " << endl;
            return(false);
        }
    }

    if (!checkErrLibcurl(curl_easy_setopt(p_curl_, CURLOPT_HTTPPOST, p_first_section), libcurl_err_info_buff_)) {
        //cerr << "ERROR! RmdownSeedDownloadWebpage::downloadSeed() call curl_easy_setopt() failure! " << endl;
        return(false);
    }
    // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    bool b_success = download_(url, filename, url_, timeout_second, retry_times, retry_sleep_second);

    // TODO. reset CURLOPT_HTTPPOST, are you sure it works?
    static struct curl_httppost empty_httppost;
    curl_easy_setopt(p_curl_, CURLOPT_HTTPPOST, &empty_httppost);


    return(b_success);
}

const string&
Webpage::getTxt (void) const
{
    return(txt_);
}

bool
Webpage::isLoaded (void) const
{
    return(b_loaded_ok_);
}

bool
Webpage::saveasFile (const string& filename) const
{
    ofstream ofs_webpage(filename);
    istringstream iss_webpage_txt(txt_);

    string line;
    while (getline(iss_webpage_txt, line)) {
        ofs_webpage << line << "\n";
    }
    
    ofs_webpage.close();

    return(true);
}

size_t
Webpage::convertCharset (const string& src_charset, const string& dest_charset)
{
    string dest_charset_str;

    istringstream iss_webpage_txt(txt_);
    string line;
    iconv_t cd = iconv_open((dest_charset + "//IGNORE").c_str(), src_charset.c_str()); // why "//IGNORE"? When the string "//IGNORE" is
                                                                                       // appended to dest char set, some char that cannot
                                                                                       // be represented in the target character set will 
                                                                                       // be silently discarded, ohterwise iconv() will
                                                                                       // stop at this char
    while (getline(iss_webpage_txt, line)) {
        line += "\n";
        size_t inbytes_left = line.size();
        char* p_inbuff = (char*)line.c_str();
        size_t outbytes_left = 2 * inbytes_left; // TODO. why 2? utf8 use 3 bytes for one asia character, 1 byte for one west wcharacter; gbk use 2 bytes for everyone character, so double is the guard value
        char* outbuff = new char [outbytes_left];
        memset(outbuff, '\0', outbytes_left);
        char* p_outbuff = outbuff;
        
        if ((size_t)-1 == iconv(cd, &p_inbuff, &inbytes_left, &p_outbuff, &outbytes_left)) {
            //cerr << "WARNING! iconv() "<< strerror(errno) << endl;
            ;
        }
        dest_charset_str += outbuff;
        
        delete [] outbuff;
    }
    iconv_close(cd);

    txt_ = dest_charset_str;

    static const string title_keyword_begin("<title>"), title_keyword_end("</title>");
    title_ = unescapeHtml(fetchStringBetweenKeywords(txt_, title_keyword_begin, title_keyword_end).first);

    return(txt_.size());
}

const string&
Webpage::getTitle (void) const
{
    return(title_);
}


