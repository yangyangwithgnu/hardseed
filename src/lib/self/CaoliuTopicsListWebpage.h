// last modified 

#pragma once

#include <string>
#include <vector>
#include "TopicsListWebpage.h"

using std::string;
using std::vector;


class CaoliuTopicsListWebpage : public TopicsListWebpage
{
    public:
        CaoliuTopicsListWebpage (const string& url, const string& proxy_addr);
        virtual ~CaoliuTopicsListWebpage ();
};
