// last modified 

#include "Misc.h"
#include <algorithm>
#include <iostream>
#include <iterator>
#include <cstdlib>
#include <cstdio>
#include <bitset>
#include <ctime>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

using std::bitset;
using std::cout;
using std::cerr;
using std::endl;
using std::make_pair;
using std::ostream_iterator;

// split raw string to more sub-str by token-chars.
// note:
// 0) case sensitive;
// 1) if there are consecutive two token-chars in raw string, splitStr()
// will make a empty sub-str into splited_substr_list.
void
splitStr ( const string& str,
           const string& tokens_list,
           vector<string>& splited_substr_list,
           vector<char>& appeared_tokens_list )
{
    size_t begin_pos = 0, end_pos;
    while (begin_pos < str.size()) {
        const auto iter_token = find_first_of( str.cbegin() + (int)begin_pos, str.cend(),
                                               tokens_list.cbegin(), tokens_list.cend() );
        if (str.cend() == iter_token) {
            splited_substr_list.push_back(str.substr(begin_pos));
            break;
        }
        
        appeared_tokens_list.push_back(*iter_token);
        end_pos = (unsigned)(iter_token - str.cbegin());
        splited_substr_list.push_back(str.substr(begin_pos, end_pos - begin_pos));
        
        begin_pos = end_pos + 1;
    }

    if (splited_substr_list[0].empty()) {
        splited_substr_list.erase(splited_substr_list.begin());
    }
}

// first return is the string between keyword_begin and keyword_end;
// second return is end_pos + keyword_end.size().
pair<string, size_t>
fetchStringBetweenKeywords ( const string& txt,
                             const string& keyword_begin,
                             const string& keyword_end,
                             size_t from_pos )
{
    const auto begin_pos = txt.find(keyword_begin, from_pos);
    if (string::npos == begin_pos) {
        //cerr << "WARNING! fetchStringBetweenKeywords() CANNOT find the keyword \"" << kyeword_begin << "\"" << endl;
        return(make_pair("", 0));
    }
    const auto end_pos = txt.find(keyword_end, begin_pos + keyword_begin.size());
    if (string::npos == end_pos) {
        //cerr << "WARNING! fetchStringBetweenKeywords() CANNOT find the keyword \"" << kyeword_end << "\"" << endl;
        return(make_pair("", 0));
    }


    return(make_pair( txt.substr(begin_pos + keyword_begin.size(), end_pos - begin_pos - keyword_begin.size()),
                      end_pos + keyword_end.size() ));
}

// get file size by FILE*.
// return -1 if failure
long
getFileSize (FILE* fs)
{
    // backup current offset
    long offset_bak = ftell(fs);

    // get the filesize
    fseek(fs, 0, SEEK_END);
    long file_size = ftell(fs);

    // restore last offset
    fseek(fs, offset_bak, SEEK_SET);


    return(file_size);
}

// process_name + process_id + thread_id + rand
extern char *__progname;
string
makeRandomFilename (void) 
{
    static bool b_first = true;
    if (b_first) {
        srand((unsigned)time(NULL));
        b_first = false;
    }

    const string& filename = string(__progname) + "_" +
                             convNumToStr(getpid()) + "_"
                             + convNumToStr(pthread_self()) + "_"
                             + convNumToStr(rand());

#ifdef CYGWIN
    return("c:\\" + filename);
#else
    return("/tmp/" + filename);
#endif
}

// unicode 与 UTF8 间转换规则：
// =================================================================================
//   |  unicode 符号范围     |  UTF8编码方式  
// n |  (十六进制)           | (二进制)  
// --+-----------------------+------------------------------------------------------  
// 1 | 0000 0000 - 0000 007F |                                              0xxxxxxx  
// 2 | 0000 0080 - 0000 07FF |                                     110xxxxx 10xxxxxx  
// 3 | 0000 0800 - 0000 FFFF |                            1110xxxx 10xxxxxx 10xxxxxx  
// 4 | 0001 0000 - 0010 FFFF |                   11110xxx 10xxxxxx 10xxxxxx 10xxxxxx  
// 5 | 0020 0000 - 03FF FFFF |          111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx  
// 6 | 0400 0000 - 7FFF FFFF | 1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 
// =================================================================================
// UTF8 中剩余的 x 用其 unicode 中各位从右向左填充，若还有多余的位则 0 填。如，"严"
// 的 unicode 是 4E25（100111000100101），根据上表，可以发现 4E25 处在第三行的范围内
// （0000 0800-0000 FFFF），"严"的 UTF8 编码需要三个字节，即格式是
// "1110xxxx 10xxxxxx 10xxxxxx"，然后，从"严"的最后一个二进制位开始，依次从后向前填
// 入格式中的 x，多出的位补 0。这样就得到了，"严"的 UTF8 编码是
// "11100100 10111000 10100101"，转换成十六进制就是 E4B8A5。
// 
// 返回值：由于 UTF8 是变长编码格式，所以，需要返回转换后的 UTF8 编码有效字节数，以
//     具体值。
//     
// 注意：
//     0）假定小尾存储；
//     1）unicode 最多需要 4 个字节，UTF8 最多需要 6 个字节，所以，这就决定了型参类
//     型必须为 unsigned int，返回值类型为 unsigned long long； 
// 
// 更多细节参见：http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html
pair<size_t, unsigned long long>
convertUnicodeToUtf8 (unsigned int unicode)
{
    if (unicode <= 0x0000007F) {
        return(make_pair(1, unicode));
    } else if (0x00000080 <= unicode && unicode <= 0x000007FF) {
        bitset<16> unicode_bits(unicode);
        const string unicode_bits_str = unicode_bits.to_string<char, string::traits_type, string::allocator_type>();
        string unicode_bits_str_reverse(unicode_bits_str.crbegin(), unicode_bits_str.crend());
        unicode_bits_str_reverse.insert(6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 5, "000");
        unicode_bits_str_reverse.resize(16);
        const bitset<16> masker(string(unicode_bits_str_reverse.crbegin(), unicode_bits_str_reverse.crend()));
        
        bitset<16> utf8_lower("1100000010000000");
       
        bitset<16> utf8_bits = utf8_lower | masker;
       
        return(make_pair(2, utf8_bits.to_ullong()));
    } else if (0x00000800 <= unicode && unicode <= 0x0000FFFF) {
        bitset<16> unicode_bits(unicode);
        const string unicode_bits_str = unicode_bits.to_string<char, string::traits_type, string::allocator_type>();
        string unicode_bits_str_reverse(unicode_bits_str.crbegin(), unicode_bits_str.crend());
        unicode_bits_str_reverse.insert(6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 4, "0000");
        unicode_bits_str_reverse.resize(24);
        const bitset<24> masker(string(unicode_bits_str_reverse.crbegin(), unicode_bits_str_reverse.crend()));
        
        bitset<24> utf8_lower("111000001000000010000000");
       
        bitset<24> utf8_bits = utf8_lower | masker;
       
        return(make_pair(3, utf8_bits.to_ullong()));
    } else if (0x00010000 <= unicode && unicode <= 0x0010FFFF) {
        bitset<32> unicode_bits(unicode);
        const string unicode_bits_str = unicode_bits.to_string<char, string::traits_type, string::allocator_type>();
        string unicode_bits_str_reverse(unicode_bits_str.crbegin(), unicode_bits_str.crend());
        unicode_bits_str_reverse.insert(6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 3, "000");
        unicode_bits_str_reverse.resize(32);
        const bitset<32> masker(string(unicode_bits_str_reverse.crbegin(), unicode_bits_str_reverse.crend()));
        
        bitset<32> utf8_lower("11110000100000001000000010000000");
       
        bitset<32> utf8_bits = utf8_lower | masker;
       
        return(make_pair(4, utf8_bits.to_ullong()));
    } else if (0x00200000 <= unicode && unicode <= 0x03FFFFFF) {
        bitset<32> unicode_bits(unicode);
        const string unicode_bits_str = unicode_bits.to_string<char, string::traits_type, string::allocator_type>();
        string unicode_bits_str_reverse(unicode_bits_str.crbegin(), unicode_bits_str.crend());
        unicode_bits_str_reverse.insert(6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 6 + 2 + 2, "00");
        unicode_bits_str_reverse.resize(40);
        const bitset<40> masker(string(unicode_bits_str_reverse.crbegin(), unicode_bits_str_reverse.crend()));
        
        bitset<40> utf8_lower("1111100010000000100000001000000010000000");
       
        bitset<40> utf8_bits = utf8_lower | masker;
       
        return(make_pair(5, utf8_bits.to_ullong()));
    } else if (0x04000000 <= unicode && unicode <= 0x7FFFFFFF) {
        bitset<64> unicode_bits(unicode);
        const string unicode_bits_str = unicode_bits.to_string<char, string::traits_type, string::allocator_type>();
        string unicode_bits_str_reverse(unicode_bits_str.crbegin(), unicode_bits_str.crend());
        unicode_bits_str_reverse.insert(6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 6 + 2 + 6, "00");
        unicode_bits_str_reverse.insert(6 + 2 + 6 + 2 + 6 + 2 + 6 + 2 + 6 + 2 + 1, "0");
        unicode_bits_str_reverse.resize(48);
        const bitset<48> masker(string(unicode_bits_str_reverse.crbegin(), unicode_bits_str_reverse.crend()));
        
        bitset<48> utf8_lower("111111001000000010000000100000001000000010000000");
       
        bitset<48> utf8_bits = utf8_lower | masker;
       
        return(make_pair(6, utf8_bits.to_ullong()));
    } else {
        cerr << "WARNING! " << unicode << "is not a vaild unicode. " << endl;
        return(make_pair(0, 0));
    }
}

bool
wait_cmd ( const string& cmd,
           const vector<string>& argv,
           int* p_exitCode,
           bool b_echo ) 
{	
	bool	b_executed_success = false;
	char**	argv_tmp;


	// 回显命令行
    if (b_echo) {
        copy(argv.cbegin(), argv.cend(), ostream_iterator<string>(cout, " "));
        cout << endl;
    }

    // 将vector<string>中的命令行参数转换为char* []
    argv_tmp = new char* [argv.size() + 1]; // ！！！子进程中是否产生内存泄漏？？
    for (size_t i = 0; i != argv.size(); ++i) {
        argv_tmp[i] = const_cast<char*>(argv[i].c_str());
    }
    argv_tmp[argv.size()] = NULL;

    // 运行并等待子进程
    pid_t   pid = fork();
    if (0 == pid) {         // 子进程
        execvp(cmd.c_str(), argv_tmp);
    } else if (pid > 0) {   // 父进程
        int status;
        waitpid(pid, &status, 0);
        // 命令正常结束。即通过exit()正常退出，而非通过kill异常结束，与exit()的返回值无关
        if (WIFEXITED(status)) {
            int exit_code = WEXITSTATUS(status); // 命令通过正常exit()结束时的返回值
            
            if (EXIT_SUCCESS == exit_code) { 
                b_executed_success = true;
            }
            
            if (NULL != p_exitCode) {
                *p_exitCode = exit_code;
            }
        }
    }

    delete [] argv_tmp;

    return (b_executed_success );
}

