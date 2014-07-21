#include <iostream>
#include <string>
#include <algorithm>
#include <iterator>
#include <sstream>
#include <cstring>
#include <cstdlib>
#include <cerrno>
#include <unistd.h>
#include <limits.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "lib/self/Webpage.h"
#include "lib/self/Aicheng.h"
#include "lib/self/Caoliu.h"
#include "lib/helper/Time.h"
#include "lib/helper/CmdlineOption.h"
#include "lib/helper/RichTxt.h"
#include "lib/helper/Misc.h"


using namespace std;


static const string g_softname(RichTxt::bold_on + "hardseed" + RichTxt::bold_off);
static const string g_version("0.1.1");
static const string g_myemail("yangyang.gnu@gmail.com");
static const string g_myemail_color(RichTxt::bold_on + RichTxt::foreground_green + g_myemail + RichTxt::reset_all);
static const string g_mywebspace("http://www.yangyangwithgnu.net/");
static const string g_mywebspace_color(RichTxt::bold_on + RichTxt::foreground_green + g_mywebspace + RichTxt::reset_all);


static void
showSexyGirl (void)
{
    cout    << endl << 
            ".================================================================." << endl << 
          //"||                        *hardseed* vx.y.z                     ||" << endl << 
            "||                         " << g_softname << " v" << g_version << "                      ||" << endl << 
            "|'--------------------------------------------------------------'|" << endl << 
            "||       -- SEX IS ZERO (0), so, who wanna be the ONE (1), aha? ||" << endl << 
            "|'=============================================================='|" << endl << 
            "||                                .::::.                        ||" << endl << 
            "||                              .::::::::.                      ||" << endl << 
            "||                              :::::::::::                     ||" << endl << 
            "||                              ':::::::::::..                  ||" << endl << 
            "||                              .:::::::::::::::'               ||" << endl << 
            "||                                '::::::::::::::.`             ||" << endl << 
            "||                                  .::::::::::::::::.'         ||" << endl << 
            "||                                .::::::::::::..               ||" << endl << 
            "||                              .::::::::::::::''               ||" << endl << 
            "||                   .:::.       '::::::::''::::                ||" << endl << 
            "||                 .::::::::.      ':::::'  '::::               ||" << endl << 
            "||                .::::':::::::.    :::::    '::::.             ||" << endl << 
            "||              .:::::' ':::::::::. :::::.     ':::.            ||" << endl << 
            "||            .:::::'     ':::::::::.::::::.      '::.          ||" << endl << 
            "||          .::::''         ':::::::::::::::'       '::.        ||" << endl << 
            "||         .::''              '::::::::::::::'        ::..      ||" << endl << 
            "||      ..::::                  ':::::::::::'         :'''`     ||" << endl << 
            "||   ..''''':'                    '::::::.'                     ||" << endl << 
            "|'=============================================================='|" << endl << 
          //"||                                       yangyang.gnu@gmail.com ||" << endl << 
            "||                                       " << g_myemail_color << " ||" << endl << 
            //"||                              http://www.yangyangwithgnu.net/ ||" << endl << 
            "||                              " << g_mywebspace_color << " ||" << endl << 
            "'================================================================'" << endl;
}

static void
showHelpInfo (void)
{
    cout << endl;
    cout << g_softname
         << " is a batch seeds and pictures download utiltiy from CaoLiu and AiCheng forum. "
         << "It's easy and simple to use. Usually, you could issue it as follow: " << endl
         << "  $ hardseed" << endl
         << "or" << endl
         << "  $ hardseed --saveas-path ~/downloads --multi-threads 4 --topics-range 8 64"
         << " --av-class aicheng_west --timeout-download-picture 32 --hate X-Art --proxy http://127.0.0.1:8087" << endl;

    cout << endl;
    cout << "  --help" << endl
         << "  Show this help infomation what you are seeing. " << endl;

    cout << endl;
    cout << "  --version" << endl
         << "  Show current version. " << endl;

    cout << endl;
    cout << "  --av-class" << endl
         << "  There are twelve av classes: caoliu_west_reposted, caoliu_cartoon_reposted, "
         << "caoliu_asia_mosaicked_reposted, caoliu_asia_non_mosaicked_reposted, caoliu_west_original, "
         << "caoliu_cartoon_original, caoliu_asia_mosaicked_original, caoliu_asia_non_mosaicked_original, "
         << "aicheng_west, aicheng_cartoon, aicheng_asia_mosaicked and aicheng_asia_non_mosaicked. " << endl
         << "  As the name implies, \"caoliu\" stands for CaoLiu forum, \"aicheng\" for AiCheng forum, "
         << "\"reposted\" and \"original\" is clearity, you konw which one is your best lover (yes, only one). " << endl
         << "  The default is aicheng_asia_mosaicked. " << endl;

    cout << endl;
    cout << "  --concurrent-tasks" << endl
         << "  You can set more than one proxy, each proxy could more than one concurrent tasks. This option "
         << "set the number of concurrent tasks of each prox. " << endl
         << "  The max and default number is 8. " << endl;

    cout << endl;
    cout << "  --timeout-download-picture" << endl
         << "  Some pictures too big to download in few seconds. So, you should set the download picture "
         << "timeout seconds. " << endl
         << "  The default timeout is 32 seconds." << endl;

    cout << endl;
    cout << "  --topics-range" << endl
         << "  Set the range of to download topics. E.G.: " << endl
         << "    --topics-range 2 16" << endl
         << "    --topics-range 8 (I.E., --topics-range 1 8)" << endl
         << "    --topics-range -1 (I.E., all topics of this av class)" << endl
         << "  The default topics range is 128" << endl;

    cout << endl;
    cout << "  --saveas-path" << endl
         << "  Set the path to save seeds and pictures. The rule of dir: [avclass][range]@hhmmss. E.G., "
         << "[aicheng_west][2~32]@124908/. " << endl
         << "  The default directory is home directory (or windows is C:\\). " << endl;

    cout << endl;
    cout << "  --hate" << endl
         << "  If you hate some subject topics, you can ignore them by setting this option with keywords "
         << "in topic title, split by space-char ' ', and case sensitive. E.G., --hate 孕妇 重口味. "
         << "When --hate keywords list conflict with --like, --hate first. " << endl;

    cout << endl;
    cout << "  --like" << endl
         << "  If you like some subject topics, you can grab them by setting this option with keywords "
         << "in topic title, split by space-char ' ', and case sensitive. E.G., --like 苍井空 小泽玛利亚. "
         << "When --like keywords list conflict with --hate, --hate first. " << endl;

    cout << endl;
    cout << "  --proxy" << endl
         << "  As you know, the government likes blocking adult websites, so, I do suggest you to set "
         << "--proxy option. Hardseed supports more proxys: " << endl
         << "    a) GoAgent (STRONGLY recommended), --proxy http://127.0.0.1:8087" << endl
         << "    b) shadowsocks, --proxy socks5://127.0.0.1:1080, or socks5h://127.0.0.1:1080" << endl
         << "    c) SSH, --proxy socks4://127.0.0.1:7070" << endl
         << "    d) VPN (PPTP and openVPN), --proxy \"\"" << endl
         << "  It is important that you should know, you can set more proxys at the same time, split by "
         << "space-char ' '. As the --concurrent-tasks option says, each proxy could more than one concurrent "
         << "tasks, now, what about more proxys? Yes, yes, the speed of downloading seed and pictures is "
         << "very very fast. E.G., --concurrent-tasks 8 --proxy http://127.0.0.1:8087 socks5://127.0.0.1:1080 "
         << "socks4://127.0.0.1:7070, the number of concurrent tasks is 8*3. " << endl
         << "  If you wanna how to install and configure various kinds of proxy, please access my homepage "
         << "\"3.3 搭梯翻墙\" http://www.yangyangwithgnu.net/the_new_world_linux/#index_3_3 " << endl
         << "  The default http://127.0.0.1:8087. " << endl;

    cout << endl;
    cout << "  That's all. Any suggestions let me know by "
         << g_myemail_color
         << " or "
         << g_mywebspace_color
         << ", big thanks to you. Kiddo, take care of your body. :-)" << endl << endl;
}

static void
showVersionInfo (void)
{
    cout << "hardseed version " << g_version << endl
         << "email " << g_myemail << endl
         << "webspace " << g_mywebspace << endl << endl;
}

static bool
parseTopicsRangeArgument ( const vector<string>& topicsrange_arguments_list,
                           unsigned& topics_range_begin,
                           unsigned& topics_range_end )
{
    if (topicsrange_arguments_list.empty()) {
        return(false);
    }

    string begin_str = topicsrange_arguments_list[0];
    string end_str;
    if (topicsrange_arguments_list.size() < 2) {
        end_str = begin_str;
        begin_str = "1";
    } else {
        end_str = topicsrange_arguments_list[1];
    }

    unsigned begin_tmp;
    if ( 0 == (begin_tmp = strtoul(begin_str.c_str(), nullptr, 0)) &&
         '0' != begin_str[0] ) {
        return(false);
    }
    unsigned end_tmp;
    if ( 0 == (end_tmp = strtoul(end_str.c_str(), nullptr, 0)) &&
         '0' != end_str[0] ) {
        return(false);
    }

    if (begin_tmp > end_tmp) {
        return(false);
    }

    topics_range_begin = begin_tmp;
    topics_range_end = end_tmp;


    return(true);
}


int
main (int argc, char* argv[])
{
    // parse command line options
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    CmdlineOption cmdline_options((unsigned)argc, argv);
    vector<string> cmdline_arguments_list;

    // --help, first high priority, ignore other options
    if (cmdline_options.hasOption("--help")) {
        showHelpInfo();
        return(EXIT_SUCCESS);
    }

    // --version, second high priority, ignore other options
    if (cmdline_options.hasOption("--version")) {
        showVersionInfo();
        return(EXIT_SUCCESS);
    }

    // show the sexy girl ASCII art
    showSexyGirl();
    cout << endl;

    // prompt turn on the goagent
    cout << RichTxt::bold_on
         << "************************ !! IMPORTANCE !! ************************" << endl
         << "********  please make sure the proxy software is running  ********" << endl
         << "************************ !! IMPORTANCE !! ************************" << endl
         << RichTxt::bold_off << endl;

    // --av-class 
    // >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    cout << "Your command arguments: " << endl;
    string av_class_name("aicheng_asia_mosaicked");
    cmdline_arguments_list = cmdline_options.getArgumentsList("--av-class");
    if (!cmdline_arguments_list.empty()) {
        av_class_name = cmdline_arguments_list[0];
    }

    bool b_aicheng = true;
    Caoliu::AvClass caoliu_av_class = Caoliu::asia_mosaicked_original;
    Aicheng::AvClass aicheng_av_class = Aicheng::asia_mosaicked;
    if ("caoliu_west_original" == av_class_name) {
        caoliu_av_class = Caoliu::west_original;
        b_aicheng = false;
    } else if ("caoliu_cartoon_original" == av_class_name) {
        caoliu_av_class = Caoliu::cartoon_original;
        b_aicheng = false;
    } else if ("caoliu_asia_mosaicked_original" == av_class_name) {
        caoliu_av_class = Caoliu::asia_mosaicked_original;
        b_aicheng = false;
    } else if ("caoliu_asia_non_mosaicked_original" == av_class_name) {
        caoliu_av_class = Caoliu::asia_non_mosaicked_original;
        b_aicheng = false;
    } else if ("caoliu_west_reposted" == av_class_name) {
        caoliu_av_class = Caoliu::west_reposted;
        b_aicheng = false;
    } else if ("caoliu_cartoon_reposted" == av_class_name) {
        caoliu_av_class = Caoliu::cartoon_reposted;
        b_aicheng = false;
    } else if ("caoliu_asia_mosaicked_reposted" == av_class_name) {
        caoliu_av_class = Caoliu::asia_mosaicked_reposted;
        b_aicheng = false;
    } else if ("caoliu_asia_non_mosaicked_reposted" == av_class_name) {
        caoliu_av_class = Caoliu::asia_non_mosaicked_reposted;
        b_aicheng = false;
    } else if ("aicheng_west" == av_class_name) {
        aicheng_av_class = Aicheng::west;
    } else if ("aicheng_asia_mosaicked" == av_class_name) {
        aicheng_av_class = Aicheng::asia_mosaicked;
    } else if ("aicheng_cartoon" == av_class_name) {
        aicheng_av_class = Aicheng::cartoon;
    } else if ("aicheng_asia_non_mosaicked" == av_class_name) {
        aicheng_av_class = Aicheng::asia_non_mosaicked;
    } else {
        cerr << "ERROR! the --av-class argument invalid. More info please see --help. " << endl;
        return(EXIT_FAILURE);
    }

    cout << "  the av class \"" << RichTxt::bold_on << av_class_name << RichTxt::bold_off << "\"; " << endl;
    // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    // --timeout-download-picture
    unsigned timeout_download_pic = 32; // default timeout seconds
    cmdline_arguments_list = cmdline_options.getArgumentsList("--timeout-download-picture");
    if (!cmdline_arguments_list.empty()) {
        unsigned tmp = strtoul(cmdline_arguments_list[0].c_str(), nullptr, 0);
        if (tmp > 0) {
            timeout_download_pic = tmp;
        }
    }
    cout << "  the download picture timeout seconds "
         << "\"" << RichTxt::bold_on << timeout_download_pic << RichTxt::bold_off << "\"; " << endl;

    // --topics-range, E.G.:
    // --topics-range 2 16,
    // --topics-range 8 (I.E., --topics-range 1 8),
    // --topics-range 4 -1 (I.E., all topics of this class av)
    unsigned topics_range_begin = 1, topics_range_end = 128; // default range
    cmdline_arguments_list = cmdline_options.getArgumentsList("--topics-range");
    if (!cmdline_arguments_list.empty()) {
        if (!parseTopicsRangeArgument(cmdline_arguments_list, topics_range_begin, topics_range_end)) {
            cerr << "ERROR! --topics-range argument setting wrong! " << endl;
            return(EXIT_FAILURE);
        }
    }
    cout << "  the range of parsing topics "
         << RichTxt::bold_on << "[" << topics_range_begin << "~" << topics_range_end << "]" << RichTxt::bold_off
         << "; " << endl;

    // --saveas-path.
    // create dir to save seeds and pictures. the rule of dir: [avclass][range]@hhmmss.
    // E.G., [aicheng_west][8~16]@211159. default home directory.
    // >>>>>>>>>>>>>>>>>>
    string path;

    cmdline_arguments_list = cmdline_options.getArgumentsList("--saveas-path");
    if (cmdline_arguments_list.empty()) {
#ifdef CYGWIN
        const char* p_home = "C:\\";
#else
        const char* p_home = getenv("HOME");
#endif
        if (nullptr == p_home) {
            cerr << "ERROR! --saveas-path argument setting wrong! " << endl;
            return(EXIT_FAILURE);
        }
        path = p_home;
    } else {
        path = cmdline_arguments_list[0];
    }
    path += "/[";

    // 1st, av class
    path += av_class_name;
    path += "]";

    // 2nd, range
    path += "[" + convNumToStr(topics_range_begin) + "~" + convNumToStr(topics_range_end) + "]@";

    // 3rd, time
    Time current_time;
    path += current_time.getHour(2) + current_time.getMinute(2) + current_time.getSecond(2);
    path += "/";

#ifdef CYGWIN
    // windows path style
    replace(path.begin(), path.end(), '/', '\\');
#endif

    // create dir
    if (-1 == mkdir(path.c_str(), 0755)) {
        cerr << "ERROR! cannot create " << path << ", " << strerror(errno) << endl;
        return(EXIT_FAILURE);
    }

#ifndef CYGWIN
    // convert raw path to standard absolute path. To call realpath() success,
    // path must have created.
    char buffer[PATH_MAX];
    realpath(path.c_str(), buffer);
    path = buffer;
#endif

    cout << "  the path to save seeds and pictures \"" << RichTxt::bold_on << path << RichTxt::bold_off << "\"; " << endl;
    // <<<<<<<<<<<<<<<<<<

    // --concurrent-tasks
    unsigned threads_total = 8; // the default and the max number of threads
    cmdline_arguments_list = cmdline_options.getArgumentsList("--concurrent-tasks");
    if (!cmdline_arguments_list.empty()) {
        unsigned tmp = strtoul(cmdline_arguments_list[0].c_str(), nullptr, 0);
        if (tmp <= 0 || tmp > threads_total) {
            cerr << "ERROR! --concurrent-tasks argument setting wrong. The max and default number is 16. " << endl;
            return(EXIT_FAILURE);
        }
        threads_total = tmp;
    }
    cout << "  the number of concurrent tasks \"" << RichTxt::bold_on << threads_total << RichTxt::bold_off << "\"; " << endl;

    // --hate. ignore the topics by user setting keywords in topic title, split by space-char ' '.
    // for example: --ignore aa bb cc "d d".
    vector<string> hate_keywords_list = { "连发", "連发", "连發", "連發",
                                          "连弹", "★㊣", "合辑", "合集",
                                          "合輯", "nike", "最新の美女骑兵㊣",
                                          "精選" }; // force to ignore the all-in-one topics
    cmdline_arguments_list = cmdline_options.getArgumentsList("--hate");
    if (!cmdline_arguments_list.empty()) {
        hate_keywords_list.insert(hate_keywords_list.end(), cmdline_arguments_list.begin(), cmdline_arguments_list.end());
    }
    cout << "  ignore some topics which include the keywords as follow \"" << RichTxt::bold_on;
    if (hate_keywords_list.empty()) {
        cout << "  ";
    } else {
        copy(hate_keywords_list.cbegin(), hate_keywords_list.cend(), ostream_iterator<const string&>(cout, ", "));
    }
    cout << RichTxt::bold_off << "\b\b\"; " << endl;

    // --like. 
    vector<string> like_keywords_list;
    cmdline_arguments_list = cmdline_options.getArgumentsList("--like");
    if (!cmdline_arguments_list.empty()) {
        like_keywords_list.assign(cmdline_arguments_list.begin(), cmdline_arguments_list.end());
    }
    cout << "  just parse topics which include the kewords as follow \"" << RichTxt::bold_on;
    if (like_keywords_list.empty()) {
        cout << "  ";
    } else {
        copy(like_keywords_list.cbegin(), like_keywords_list.cend(), ostream_iterator<const string&>(cout, ", "));
    }
    cout << RichTxt::bold_off << "\b\b\"; " << endl;

    // --proxy. prompt user to use proxy, because the caoliu bbs maybe block IP
    vector<string> proxy_addrs_list = {"http://127.0.0.1:8087"}; // the default proxy is GoAgent
    cmdline_arguments_list = cmdline_options.getArgumentsList("--proxy");
    if (!cmdline_arguments_list.empty()) {
        proxy_addrs_list = cmdline_arguments_list;
    }
    cout << "  the proxy \"" << RichTxt::bold_on;
    copy(proxy_addrs_list.cbegin(), proxy_addrs_list.cend(), ostream_iterator<string>(cout, ", "));
    cout << "\b\b" << RichTxt::bold_off << "\". " << endl << endl;
    
    // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    // download pictures and seed
    if (b_aicheng) {
        Aicheng aicheng( aicheng_av_class,
                         proxy_addrs_list,
                         topics_range_begin, topics_range_end,
                         hate_keywords_list,
                         like_keywords_list,
                         threads_total * proxy_addrs_list.size(),
                         timeout_download_pic,
                         path );
    } else {
        Caoliu caoliu ( caoliu_av_class,
                        proxy_addrs_list,
                        topics_range_begin, topics_range_end,
                        hate_keywords_list,
                        like_keywords_list,
                        threads_total * proxy_addrs_list.size(),
                        timeout_download_pic,
                        path );
    }


    cout << endl;
    return(EXIT_SUCCESS);
}

