// last modified 

#pragma once

#include <string>
#include "SeedWebpage.h"

using std::string;


class JandownSeedWebpage : public SeedWebpage
{
    public:
        JandownSeedWebpage (const string& url, const string& proxy_addr);
        virtual ~JandownSeedWebpage ();
};
