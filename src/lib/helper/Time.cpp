// last modified 

#include "Time.h"
#include <algorithm>
#include <string>
#include <sstream>
#include <ctime>

using namespace std;


// why not std::to_string()? 
// you know, I have to port this linux code to win32 by cygwin, and there
// is a bug on cygwin case it cannot find to_string(), so, I must do it by myself
static string
convUnsignedToStr (unsigned num)
{
    ostringstream oss;
    oss << num;

    return(oss.str());
}

// string::resize() resize string from the first char to the last char,
// resizeStringByEndian() resize string from the last char to the first char
static string
resizeStringByEndian (const string& str, unsigned digits, char ch = '0')
{
    string strtmp(str.crbegin(), str.crend());
    strtmp.resize(digits, ch);
    reverse(strtmp.begin(), strtmp.end());

    return(strtmp);
}

Time::Time ()
{
    time_t raw_time = time(nullptr);
    const struct tm* p_st = localtime(&raw_time);

    year_ = (unsigned)p_st->tm_year + 1900;
    month_ = (unsigned)p_st->tm_mon + 1;
    day_in_month_ = (unsigned)p_st->tm_mday;
    day_in_year_ = (unsigned)p_st->tm_yday + 1;
    day_in_week_ = (unsigned)p_st->tm_wday;
    hour_ = (unsigned)p_st->tm_hour;
    minute_ = (unsigned)p_st->tm_min;
    second_ = (unsigned)p_st->tm_sec;
}

Time::~Time ()
{
    ;
}

unsigned
Time::getYear (void) const
{
    return(year_);
}

string
Time::getYear (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getYear()) : resizeStringByEndian(convUnsignedToStr(getYear()), digits) );
}

unsigned
Time::getMonth (void) const
{
    return(month_);
}

string
Time::getMonth (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getMonth()) : resizeStringByEndian(convUnsignedToStr(getMonth()), digits) );
}

unsigned
Time::getDayInWeek (void) const
{
    return(day_in_week_);
}

string
Time::getDayInWeek (bool b_abbr) const
{
    switch (getDayInWeek()) {
        case 1:
            return(b_abbr ? "mon" : "monday");
        case 2:
            return(b_abbr ? "tues" : "tuesday");
        case 3:
            return(b_abbr ? "wed" : "wednesday");
        case 4:
            return(b_abbr ? "thurs" : "thursday");
        case 5:
            return(b_abbr ? "fri" : "friday");
        case 6:
            return(b_abbr ? "sat" : "saturday");
        case 0:
            return(b_abbr ? "sun" : "sunday");
        default:
            return("");
    }
}

unsigned
Time::getDayInMonth (void) const
{
    return(day_in_month_);
}

string
Time::getDayInMonth (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getDayInMonth()) : resizeStringByEndian(convUnsignedToStr(getDayInMonth()), digits) );
}

unsigned
Time::getDayInYear (void) const
{
    return(day_in_year_);
}

string
Time::getDayInYear (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getDayInYear()) : resizeStringByEndian(convUnsignedToStr(getDayInYear()), digits) );
}
unsigned
Time::getHour (void) const
{
    return(hour_);
}

string
Time::getHour (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getHour()) : resizeStringByEndian(convUnsignedToStr(getHour()), digits) );
}

unsigned
Time::getMinute (void) const
{
    return(minute_);
}

string
Time::getMinute (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getMinute()) : resizeStringByEndian(convUnsignedToStr(getMinute()), digits) );
}

unsigned
Time::getSecond (void) const
{
    return(second_);
}

string
Time::getSecond (unsigned digits) const
{
    return( 0 == digits ?
            convUnsignedToStr(getSecond()) : resizeStringByEndian(convUnsignedToStr(getSecond()), digits) );
}

