// last modified 

#pragma once

#include <string>
#include <vector>
#include "TopicWebpage.h"

using std::string;
using std::vector;


class CaoliuTopicWebpage : public TopicWebpage
{
    public:
        CaoliuTopicWebpage (const string& url, const string& proxy_addr);
        virtual ~CaoliuTopicWebpage ();
};

