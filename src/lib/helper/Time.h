// last modified 

#pragma once
#include <string>

using std::string;

class Time 
{
    public:
        Time ();
        virtual ~Time ();
        
        unsigned getYear (void) const;
        string getYear (unsigned digits) const;
        
        unsigned getMonth (void) const;
        string getMonth (unsigned digits) const;
        
        unsigned getDayInWeek (void) const;
        string getDayInWeek (bool b_abbr) const;
        unsigned getDayInMonth (void) const;
        string getDayInMonth (unsigned digits) const;
        unsigned getDayInYear (void) const;
        string getDayInYear (unsigned digits) const;
        
        unsigned getHour (void) const;
        string getHour (unsigned digits) const;
        
        unsigned getMinute (void) const;
        string getMinute (unsigned digits) const;
        
        unsigned getSecond (void) const;
        string getSecond (unsigned digits) const;

    private:
        unsigned year_;
        unsigned month_;
        unsigned day_in_month_;
        unsigned day_in_week_;
        unsigned day_in_year_;
        unsigned hour_;
        unsigned minute_;
        unsigned second_;
};

