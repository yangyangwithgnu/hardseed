// last modified 

#pragma once

#include <string>
#include "SeedWebpage.h"

using std::string;


class RmdownSeedWebpage : public SeedWebpage
{
    public:
        RmdownSeedWebpage (const string& url, const string& proxy_addr);
        virtual ~RmdownSeedWebpage ();
};
