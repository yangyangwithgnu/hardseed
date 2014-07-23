// last modified 

#include "CmdlineOption.h"
#include <unordered_map>
#include <vector>
#include <string>
#include <iostream>
#include <iterator>

using namespace std;

static bool
isOption (const string& str)
{
    return( str.size() >= 3 && // the shortest option "--x"
            '-' == str[0] &&
            '-' == str[1] &&
            '-' != str[2] );
}

// cmdname --foo aa, for example, --foo is an option, aa is an argument.
// convention about command line option: 
// 0) option must begin with -- (so, the shortest option --x has three characters), and the argument cannot begin with --;
// 1) an argument must follow after an option;
// 2) an option can follow as an argument or not, E.G., some option for true or false.
// one option by one more arguments? E.G., --bar a b c d. It's ok.
CmdlineOption::CmdlineOption (unsigned argc, char* argv[])
{
    if (argc < 2) {
        return;
    }

    vector<string> raw_options_list(argv + 1, argv + argc);

    string last_option;
    for (const auto& e : raw_options_list) {
        if (isOption(e)) {
            options_and_arguments_list_[e];
            last_option = e;
        } else {
            if (!last_option.empty()) {
                options_and_arguments_list_[last_option].push_back(e);
            }
        }
    }

//// DEBUG. show the result of parsing command options
//for (const auto& e : options_and_arguments_list_) {
    //const vector<string>& arguments_list = e.second;
    //cout << e.first << "(" << arguments_list.size() << "): ";
    //copy(e.second.cbegin(), e.second.cend(), ostream_iterator<string>(cout, ","));
    //cout << endl;
//}
}

CmdlineOption::~CmdlineOption ()
{
    ;
}

bool
CmdlineOption::hasOption (const string& option) const
{
    return(options_and_arguments_list_.cend() != options_and_arguments_list_.find(option));
}

const vector<string>&
CmdlineOption::getArgumentsList (const string& option)
{
    static const vector<string> empty_arguments_list;
    return(hasOption(option) ? options_and_arguments_list_[option] : empty_arguments_list);
}

