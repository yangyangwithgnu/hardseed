// last modified 

#pragma once
#include <string>
#include <vector>
#include <unordered_map>

using std::string;
using std::pair;
using std::vector;
using std::unordered_map;

class CmdlineOption 
{
    public:
        CmdlineOption (unsigned argc, char* argv[]);
        virtual ~CmdlineOption ();
        bool hasOption (const string& option) const;
        const vector<string>& getArgumentsList (const string& option);

    private:
        unordered_map<string, vector<string>> options_and_arguments_list_;
};

