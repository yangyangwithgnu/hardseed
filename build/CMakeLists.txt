PROJECT(main)


SET(SRC_LIST ../src/main.cpp
             ../src/lib/self/TopicsListWebpage.cpp ../src/lib/self/AichengTopicsListWebpage.cpp ../src/lib/self/CaoliuTopicsListWebpage.cpp
             ../src/lib/self/TopicWebpage.cpp ../src/lib/self/AichengTopicWebpage.cpp ../src/lib/self/CaoliuTopicWebpage.cpp
             ../src/lib/self/SeedWebpage.cpp ../src/lib/self/JandownSeedWebpage.cpp ../src/lib/self/RmdownSeedWebpage.cpp
             ../src/lib/self/Aicheng.cpp ../src/lib/self/Caoliu.cpp
             ../src/lib/helper/Webpage.cpp
             ../src/lib/helper/Time.cpp ../src/lib/helper/CmdlineOption.cpp ../src/lib/helper/Misc.cpp
             ../src/lib/3rd/json11/json11.cpp)

# linux
#>>>>>>>>>>>>>>>>>>>>>>

## debug
#SET(CMAKE_CXX_COMPILER "clang++")
#SET(CMAKE_CXX_FLAGS "-std=c++11 -Werror -Weverything -Wno-documentation -Wno-disabled-macro-expansion -Wno-float-equal -Wno-c++98-compat -Wno-c++98-compat-pedantic -Wno-global-constructors -Wno-exit-time-destructors -Wno-missing-prototypes -Wno-padded -Wno-old-style-cast -Wno-weak-vtables")
#SET(CMAKE_BUILD_TYPE debug)
#ADD_EXECUTABLE(main ${SRC_LIST})
#TARGET_LINK_LIBRARIES(main curl pthread)

# release
SET(CMAKE_CXX_COMPILER "g++")
SET(CMAKE_CXX_FLAGS "-std=c++11 -O3")
SET(CMAKE_BUILD_TYPE release)
ADD_EXECUTABLE(hardseed ${SRC_LIST})
TARGET_LINK_LIBRARIES(hardseed curl pthread)
INSTALL(PROGRAMS hardseed DESTINATION /usr/local/bin)

#<<<<<<<<<<<<<<<<<<<<<<


## cygwin
##>>>>>>>>>>>>>>>>>>>>>>

#SET(CMAKE_CXX_COMPILER "g++")
#SET(CMAKE_CXX_FLAGS "-std=c++11 -O3 -s -DCYGWIN")
#SET(CMAKE_BUILD_TYPE release)
#ADD_EXECUTABLE(hardseed ${SRC_LIST})
#target_link_libraries(hardseed /bin/cygcurl-4.dll)
#target_link_libraries(hardseed /lib/libiconv.a)

##<<<<<<<<<<<<<<<<<<<<<<


## osX
##>>>>>>>>>>>>>>>>>>>>>>

#SET(CMAKE_CXX_COMPILER "g++")
#SET(CMAKE_CXX_FLAGS "-std=c++11 -O3")
#SET(CMAKE_BUILD_TYPE release)
#ADD_EXECUTABLE(hardseed ${SRC_LIST})
#TARGET_LINK_LIBRARIES(hardseed curl pthread iconv)
#INSTALL(PROGRAMS hardseed DESTINATION /usr/local/bin)

##<<<<<<<<<<<<<<<<<<<<<<
