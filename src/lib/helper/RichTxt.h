// last modified 

#pragma once
#include <string>

using std::string;

namespace RichTxt
{
    // bold
    static const string bold_on("\x1b[1m");
    static const string bold_off("\x1b[21m");

    // italic
    static const string italic_on("\x1b[3m");
    static const string italic_off("\x1b[23m");

    // underline
    static const string underline_on("\x1b[4m");
    static const string underline_off("\x1b[24m");

    // hide
    static const string hide_on("\x1b[8m");
    static const string hide_off("\x1b[28m");

    // deletline
    static const string deletline_on("\x1b[9m");
    static const string deletline_off("\x1b[29m");

    // foreground
    static const string foreground_black("\x1b[30m");
    static const string foreground_red("\x1b[31m");
    static const string foreground_green("\x1b[32m");
    static const string foreground_yellow("\x1b[33m");
    static const string foreground_blue("\x1b[34m");
    static const string foreground_magenta("\x1b[35m");
    static const string foreground_cyan("\x1b[36m");
    static const string foreground_white("\x1b[37m");

    // background
    static const string background_black("\x1b[40m");
    static const string background_red("\x1b[41m");
    static const string background_green("\x1b[42m");
    static const string background_yellow("\x1b[43m");
    static const string background_blue("\x1b[44m");
    static const string background_magenta("\x1b[45m");
    static const string background_cyan("\x1b[46m");
    static const string background_white("\x1b[47m");

    // reset all
    static const string reset_all("\x1b[0m");
};

// normal usage:
// 0) cout << "email: " << RichTxt::bold_on << "yangyang.gnu@gmail.com" << RichTxt::bold_off << endl;
// 1) string name("yangyang.gnu"); string name_italic = RichTxt::italic_on + RichTxt::background_green + name + RichTxt::italic_off;
 
