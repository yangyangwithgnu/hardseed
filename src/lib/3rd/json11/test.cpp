#include <string>
#include <cstdio>
#include <iostream>
#include <sstream>
#include "json11.hpp"
#include <cassert>
#include <list>
#include <set>
#include <unordered_map>

using namespace json11;
using std::string;

// Check that Json has the properties we want.
#include <type_traits>
#define CHECK_TRAIT(x) static_assert(std::x::value, #x)
CHECK_TRAIT(is_nothrow_constructible<Json>);
CHECK_TRAIT(is_nothrow_default_constructible<Json>);
CHECK_TRAIT(is_copy_constructible<Json>);
CHECK_TRAIT(is_nothrow_move_constructible<Json>);
CHECK_TRAIT(is_copy_assignable<Json>);
CHECK_TRAIT(is_nothrow_move_assignable<Json>);
CHECK_TRAIT(is_nothrow_destructible<Json>);

void parse_from_stdin() {
    string buf;
    while (!std::cin.eof()) buf += std::cin.get();

    string err;
    auto json = Json::parse(buf, err);
    if (!err.empty()) {
        printf("Failed: %s\n", err.c_str());
    } else {
        printf("Result: %s\n", json.dump().c_str());
    }
}

int main(int argc, char **argv) {
    if (argc == 2 && argv[1] == string("--stdin")) {
        parse_from_stdin();
        return 0;
    }

    const string simple_test =
        R"({"k1":"v1", "k2":42, "k3":["a",123,true,false,null]})";

    string err;
    auto json = Json::parse(simple_test, err);

    std::cout << "k1: " << json["k1"].string_value() << "\n";
    std::cout << "k3: " << json["k3"].dump() << "\n";

    for (auto &k : json["k3"].array_items()) {
        std::cout << "    - " << k.dump() << "\n";
    }

    std::list<int> l1 { 1, 2, 3 };
    std::vector<int> l2 { 1, 2, 3 };
    std::set<int> l3 { 1, 2, 3 };
    assert(Json(l1) == Json(l2));
    assert(Json(l2) == Json(l3));

    std::map<string, string> m1 { { "k1", "v1" }, { "k2", "v2" } };
    std::unordered_map<string, string> m2 { { "k1", "v1" }, { "k2", "v2" } };
    assert(Json(m1) == Json(m2));

    // Json literals
    Json obj = Json::object({
        { "k1", "v1" },
        { "k2", 42.0 },
        { "k3", Json::array({ "a", 123.0, true, false, nullptr }) },
    });

    std::cout << "obj: " << obj.dump() << "\n";

    assert(Json("a").number_value() == 0);
    assert(Json("a").string_value() == "a");
    assert(Json().number_value() == 0);

    assert(obj == json);
    assert(Json(42) == Json(42.0));
    assert(Json(42) != Json(42.1));

    const string unicode_escape_test =
        R"([ "blah\ud83d\udca9blah\ud83dblah\udca9blah\u0000blah\u1234" ])";

    const char utf8[] = "blah" "\xf0\x9f\x92\xa9" "blah" "\xed\xa0\xbd" "blah"
                        "\xed\xb2\xa9" "blah" "\0" "blah" "\xe1\x88\xb4";

    Json uni = Json::parse(unicode_escape_test, err);
    assert(uni[0].string_value().size() == (sizeof utf8) - 1);
    assert(memcmp(uni[0].string_value().data(), utf8, sizeof utf8) == 0);

    Json my_json = Json::object {
        { "key1", "value1" },
        { "key2", false },
        { "key3", Json::array { 1, 2, 3 } },
    };
    std::string json_str = my_json.dump();
    printf("%s\n", json_str.c_str());

    class Point {
    public:
        int x;
        int y;
        Point (int x, int y) : x(x), y(y) {}
        Json to_json() const { return Json::array { x, y }; }
    };

    std::vector<Point> points = { { 1, 2 }, { 10, 20 }, { 100, 200 } };
    std::string points_json = Json(points).dump();
    printf("%s\n", points_json.c_str());
}
