// last modified 

#pragma once

#include <string>
#include <vector>
#include "TopicWebpage.h"

using std::string;
using std::vector;


class AichengTopicWebpage : public TopicWebpage
{
    public:
        AichengTopicWebpage (const string& url, const string& proxy_addr);
        virtual ~AichengTopicWebpage ();
};

