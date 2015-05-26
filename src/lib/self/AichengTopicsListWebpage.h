// last modified 

#pragma once

#include <string>
#include <vector>
#include "TopicsListWebpage.h"

using std::string;
using std::vector;


class AichengTopicsListWebpage : public TopicsListWebpage
{
    public:
        AichengTopicsListWebpage (const string& portal_url, const string& url, const string& proxy_addr);
        virtual ~AichengTopicsListWebpage ();
};
