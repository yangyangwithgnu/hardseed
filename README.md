#给不了你梦中情人，至少还有硬盘女神：hardseed
yangyangwithgnu@yeah.net  
http://yangyangwithgnu.github.io/  
2015-01-21 14:24:08


##公告
----------------

* **捐赠：支付宝 yangyangwithgnu@yeah.net 。支付宝链接 https://shenghuo.alipay.com/send/payment/fill.htm?optEmail=yangyangwithgnu@yeah.net ，支付宝二维码 $_$**
<div align="center">
<img src="https://raw.githubusercontent.com/yangyangwithgnu/yangyangwithgnu.github.io/master/pics/donate_qr.png" alt=""/><br>
</div>

**讨论**：任何意见建议移步 http://www.v2ex.com/t/123175  

**声明**：我本人绝对尊重各大爱的论坛，提供的资源不仅优质而且免费，我只是懒、足够的懒。请大家支持这些论坛，多用页面访问、多点击广告、多解囊捐赠。*我..在..干..嘛  @_@#*

**注意**  
+ 代理是一切的先决条件。你可以使用自己的代理工具，用 hardseed 的命令行选项 --proxy 指定本地中转地址及端口，也可以用我为你预配置的 goagent 代理工具，位于 https://github.com/yangyangwithgnu/goagent_out_of_box_yang
+ windows 用户需赋予 hardseed\bin\windows\hardseed.exe 管理员运行权限。具体请右键，选中 properties - compatibility - privilege level - run this program as an admin


##版本
----------------

**[v0.2.10，修正，2014-12-7]**：caoliu 地址变更，shit :-P  
**[v0.2.09，修正，2014-11-30]**：caoliu 地址变更。  
**[v0.2.08，修正，2014-10-21]**：0）仅解析主贴的图片而不再解析回帖，以避免下载无关图片；1）aicheng 论坛地址变更；2）部分用户有自己的代理工具，为缩短下载时长，将预配置的 goagent 独立成一个 github 项目。  
**[v0.2.07，修正，2014-9-25]**：windows 禁止文件名中含有 /:\*?\\<>"| 等字符，否则将导致非法路径错误，修正 hardseed 生成的文件名中可能含有如上字符的问题。  
**[v0.2.06，优化，2014-9-9]**：caoliu 原地址无法访问，更新地址；取消 caoliu 自拍套图最多只能下载 256 张的限制。  
**[v0.2.05，优化，2014-8-17]**：程序功能无任何更新，仅更新代理工具 goagent 配置文件 proxy.ini：一是设置 obfuscate = 1 开启流量混淆以正确解析出可用 GGC IP，一是设置 pagespeed = 1 以提升 GAE 的下行速度。  
**[v0.2.05，修正，2014-8-13]**：0）修正帖子部分图片 URL 未解析的问题；1）修正图片序号错误的问题；2）优化图片下载等待时长算法，不再以 --timeout-download-picture 作为绝对等待时长，而是将其作为指导值，一旦图片下载失败 hardseed 将自动计算下次重新下载所需的等待时长，同时，与“速度过低视为下载失败”的机制结合，提升图片下载等待耗时；3）升级 goagent 至 3.1.21，采用 goagent 默认 proxy.ini，而不再使用自定义 iplist （很多朋友反应采用先前我自定义 iplist 版本的 goagent 速度不理想，这是由于 GGC IP 与不同网络环境有关，我用 checkgoogleip 跑出来 GGC IP 最适合我的网络环境，不见得适合你，所以，权衡之下，还是用 goagent 自带的 GGC IP，至少这合适于大多数人）。  
**[v0.2.04，修正，2014-8-10]**：0）由于对 % 进行 URL 转义使得部分图片的 URL 生成错误，导致图片下载失败，本版本已修正；1）剔除长年显示异常的图床网站 iceimg.com；2）引入均速过低视为下载失败的机制，持续（8s）低速（4KB/s）终止当次下载，重新向服务端发起新请求，开启新一次的下载，以缩短下载错误 URL 图片等待时长；3）修正 aicheng 帖子列表页面中帖子名解析错误的问题；4）取消单个代理服务器并行下载上限数 8 的限制。  
**[v0.2.03，修正，2014-8-8]**：0）修正部分图片缺失扩展名的问题；1）默认下载帖子数量从 128 调整为 64；2）更换新的 GGC IP 进代理工具 goagent 的 proxy.ini 中以提升代理速度。  
**[v0.2.02，优化，2014-8-6]**：程序无任何功能变更，仅是优化代码，合并部分通用代码至公共库、增加用于验证代理出口 IP 和伪装浏览器的 user-agent 的接口。  
**[v0.2.01，修正，2014-7-28]**：修正临时文件未删除的错误。  
**[v0.2.00，新增，2014-7-23]**：应 @sigmadog 需求，增加抓取 caoliu 上自拍套图（江湖人称“達蓋爾的旗幟”）的功能。  
**[v0.1.00，修正，2014-7-21]**：caoliu 论坛增加了反机器人机制，若翻页过快则视为机器人行为，下载页面为空白页。此版本可应对它的反机器人机制。


##演示  
----------------
*hardseed*  
![hardseed gif demo](https://raw.githubusercontent.com/yangyangwithgnu/hardseed/master/pic/hardseed.gif)  
*running*  
![hardseed gif demo](https://raw.githubusercontent.com/yangyangwithgnu/hardseed/master/pic/running.gif)  
*more seeds and pictures*  
![hardseed gif demo](https://raw.githubusercontent.com/yangyangwithgnu/hardseed/master/pic/seeds_and_pics.gif)  

http://v.youku.com/v_show/id_XNzQxOTk0NTE2.html


##man
----------------

**hardseed** is a batch seeds and pictures download utiltiy from CaoLiu and AiCheng forum. It's easy and simple to use. Usually, you could issue it as follow:
```
$ hardseed  
```
or  
```
$ hardseed --saveas-path ~/downloads --topics-range 8 64 --av-class aicheng_west --timeout-download-picture 32 --hate X-Art --proxy http://127.0.0.1:8087  
```

--help  
Show this help infomation what you are seeing.   

--version  
Show current version.   

--av-class  
There are 13 av classes: 
- caoliu_west_reposted
- caoliu_cartoon_reposted
- caoliu_asia_mosaicked_reposted
- caoliu_asia_non_mosaicked_reposted
- caoliu_west_original
- caoliu_cartoon_original
- caoliu_asia_mosaicked_original
- caoliu_asia_non_mosaicked_original
- caoliu_selfie
- aicheng_west
- aicheng_cartoon
- aicheng_asia_mosaicked
- aicheng_asia_non_mosaicked  

As the name implies, "caoliu" stands for CaoLiu forum, "aicheng" for AiCheng forum, "reposted" and "original" are clearity, you konw which one is your best lover (yes, only one).   
The default is aicheng_asia_mosaicked.   

--concurrent-tasks  
You can set more than one proxy, each proxy could more than one concurrent tasks. This option set the number of concurrent tasks of each proxy.   
The max and default number is 8.   

--timeout-download-picture  
Some pictures too big to download in few seconds. So, you should set the download picture timeout seconds.   
The default timeout is 32 seconds.  

--topics-range  
Set the range of to download topics. E.G.:
- topics-range 2 16
- topics-range 8 (I.E., --topics-range 1 8)
- topics-range -1 (I.E., all topics of this av class)  

The default topics range is 64.

--saveas-path  
Set the path to save seeds and pictures. The rule of dir: [avclass][range]@hhmmss. E.G., [aicheng_west][2~32]@124908/. 
The default directory is home directory (or windows is C:\\).   

--hate  
If you hate some subject topics, you can ignore them by setting this option with keywords in topic title, split by space-char ' ', and case sensitive. E.G., --hate 孕妇 重口味. When --hate keywords list conflict with --like, --hate first.   

--like  
If you like some subject topics, you can grab them by setting this option with keywords in topic title, split by space-char ' ', and case sensitive. E.G., --like 苍井空 小泽玛利亚. When --like keywords list conflict with --hate, --hate first.   

--proxy  
As you know, the government likes blocking adult websites, so, I do suggest you to set --proxy option. Hardseed supports more proxys:   
- GoAgent (STRONGLY recommended), --proxy http://127.0.0.1:8087
- shadowsocks, --proxy socks5://127.0.0.1:1080, or socks5h://127.0.0.1:1080
- SSH, --proxy socks4://127.0.0.1:7070
- VPN (PPTP and openVPN), --proxy ""  

It is important that you should know, you can set more proxys at the same time, split by space-char ' '. As the --concurrent-tasks option says, each proxy could more than one concurrent tasks, now, what about more proxys? Yes, yes, the speed of downloading seed and pictures is very very fast. E.G., --concurrent-tasks 8 --proxy http://127.0.0.1:8087 socks5://127.0.0.1:1080 socks4://127.0.0.1:7070, the number of concurrent tasks is 8\*3.   
If you wanna how to install and configure various kinds of proxy, please access my homepage "3.2 搭梯翻墙" https://github.com/yangyangwithgnu/the_new_world_linux#3.2   
If you are not good at computer, there is a newest goagent for floks who are not good at computer by me, yes, out of box. see https://github.com/yangyangwithgnu/goagent_out_of_box_yang  

The default http://127.0.0.1:8087.   

That's all. Any suggestions let me know by yangyangwithgnu@yeah.net or http://yangyangwithgnu.github.io/, big thanks to you. Kiddo, take care of your body. :-)  


##中文
--------

硬盘女神，你懂嘀！hardseed 是个种子下载工具，它从浓（ai）情（cheng）蜜（she）意（qu）和爱（cao）意（liu）无（she）限（qu）的地方获取女神种子、图片。  

###【翻墙】  
你知道，这一切的一切都在墙外，所以你得具备翻墙环境，hardseed 才能帮你拉女神。hardseed 支持 goagent、shadowsocks、SSH、VPN （PPTP 和 openVPN）等各类代理模式，甚至你可以同时使用多种代理以极速下载。从普及度、稳定性、高效性来看，goagent 最优。“我一小白，平时工作压力本来就大，就想看看女神轻松下，你还让我折腾代理！没人性！”，嘚，亲，咱是做服务的。我帮你配置了一份开箱即用的 goagent，位于 https://github.com/yangyangwithgnu/goagent_out_of_box_yang ，下载后，linux 用户，命令行中运行
```
$ python proxy.py
```
windows 亲，双击运行 goagent.exe （**管理员权限**）。  

###【下载】

####『windows』
亲，往右上看，找到“download ZIP”，点击下载。

####『linux』
```
$ git clone https://github.com/yangyangwithgnu/hardseed.git
```

###【源码安装】

####『windows』  
这基本没 windows 用户什么事儿，除非你有 cygwin，否则你没法编译源码，没事，帮你弄好了，我的定位是牙医界的服务人员，服务很重要，二进制执行程序位于 hardseed\bin\windows\hardseed.exe。
 
####『linux』
0）唯一依赖 libcurl，请自行安装；  
1）代码采用 C++11 编写，gcc 版本不低于 4.7.1。  
2）命令行下运行：  
```
$ cd hardseed/build/
$ cmake .
$ make && make install
```
 
####『osX』
先将 build/CMakeLists.txt 中的  
```
TARGET_LINK_LIBRARIES(hardseed curl pthread)
```
替换成
```
TARGET_LINK_LIBRARIES(hardseed curl pthread iconv)
```
其他同 linux 构建方法。



###【使用】  
**亲，听好了，运行 hardseed 前务必确保代理程序已正常运行，否则，别说女神，蚊子都碰不到。**

####『windows』  
先进入 hardseed\bin\windows\，找到并选中 hardseed.exe，右键设置**以管理员权限运行该程序**，接着键入 alt-d 将光标定位到文件管理器的地址栏中，键入 CMD 启动命令行窗口，再在 CMD 中键入
```
X:\hardseed\bin\windows> hardseed.exe
```
这时，hardseed 开始玩命儿地为你下载女神图片和种子，经过 2 分 8 秒，找到类似 C:\\[aicheng_asia_mosaicked][1~128]@20140822\ 的目录，女神们那儿等你！

####『linux』  
同 windows 下运行一样，全用默认命令行参数运行
```
$ hardseed
```
执行完成后，你会看到 ~/[aicheng_asia_mosaicked][1~128]@014822/，你要的都在那儿。或者，玩点高级的
```
$ hardseed --saveas-path ~/downloads --topics-range 256 --av-class aicheng_west
```
其中，--saveas-path 指定存放路径为 ~/downloads/；--topics-range 指定解析的帖子范围从第 1 张到第 256 张帖子；--av-class 指定女神类型为欧美。完整命令行选项请 --hlep 查看。

###【FQA】  

**Q1**：为何 windows 版的可执行文件目录 hardseed\bin\windows\ 下有一堆 cyg\*.dll 文件？  
**A1**：hardseed 是用 C++ 编写的遵循 SUS（单一 unix 规范）的原生 linux 程序，理论上，在任何 unix-like（linux、BSD、osX） 系统上均可正常源码编译，唯独不支持 windows，为让 hardseed 具备跨平台能力，须借由某种工具（或环境）将 hardseed 转换成 windows 下的执行程序。cygwin 就是这种环境，我把 hardseed 源码纳入 cygwin 环境中重新编译，即可生成 windows 下的可执行程序 hardseed.exe，在这个过程中，cygwin 会加入些自己的代码和中转库到 hardseed.exe 中，cyg\*.dll 就是各类中转库。

**Q2**：为何运行 windows 版的执行程序总有如下警告
```
Preferred POSIX equivalent is: /cygdrive/c/xxxx, CYGWIN environment variable option "nodosfilewarning" turns off this warning. Consult the user's guide for more details about POSIX paths ...
```
影响正常运行么？  
**A2**：linux 与 windows 有很多基础设施的差异，路径表示方式就算其一，如，前者是 /this/is/linux/path/，后者 C:\this\is\windows\path\，A1 中提过 hardseed 是 linux 下的原生程序，代码中全采用的 linux 路径规则，运行 hardseed.exe 时， cygwin 自动进行路径规则转换，所以出现本问题中的警告信息以告知用户路径可能有变化。这完全不影响 hardseed.exe 正常运行。如果厌恶这些提示，可以在环境变量中增加 CYGWIN=nodosfilewarning （win7 用户：computer - properties - advanced system settings - advanced - environment variables - new，variable name 填入 CYGWIN，variable value 中填入 nodosfilewarning，保存即可）。

**Q3**：运行 hardseed 后啥都没下载呢？还提示 There is no topic which you like？  
**A3**：有几种可能：  
* 未成功翻墙。请自行参阅你的翻墙工具帮助文档，修正即可。windows 用户注意检查是否以**管理员权限运行翻墙工具**；  
* 网页翻墙已成功但仍无法下载。请检查你的代理工具是否成功接收 hardseed 的代理请求（如，goagent 窗口中可查看），windows 用户注意检查是否以**管理员权限运行 hardseed.exe**；  
* hardseed 翻墙已成功但仍无法下载。你指定了 --like xxxx 命令行选项，hardseed 将查找标题中是否含有关键字 xxxx，若没有则忽略相关帖子。更换其他关键字。

**Q4**：我已经在墙外，为何仍下载失败？  
**A4**：hardseed 默认采用 goagent 作为代理工具，即，默认本地代理中转地址为 http://127.0.0.1:8087 。如果你已在墙外无须代理即可访问 caoliu 和 aicheng 论坛，那么需要告知 hardseed 不再走本地代理中转而应直接访问，即：
```
--proxy ""
```

**Q5**：如何加快下载速度？  
**A5**：最直接会想到多线程下载，一条线程负责下载一个页面，逻辑上，线程数越多、下载速度越快，实际上，存在代理服务器和被访服务器两方面的限制：
* 代理服务器方面的限制，代理服务器为不同用户提供代理服务，为避免相互影响，通常它会限制单个用户的流量和请求频率，所以，hardseed 在指定代理服务器上的线程数一定是有个上限；
* 被访服务器方面到限制，你访问的论坛不会低能到不控制请求频率，举个例，正常情况你 4 秒钟可以打开 4 张 caoliu 论坛的帖子，一旦 caoliu 服务器发现你 1 秒钟打开了 32 张帖子那一定将此视为机器人行为，从而拒绝响应。

正由于存在代理服务器和被访服务器两方面的限制，线程数不能无限大，从我多次测试的经验来看，**单个代理服务器**访问被访服务器的并行线程数设定为 8 条最为稳定，否则容易引起代理服务器和被访服务器停服。同个时刻有大量用户在访问 caoliu 论坛，肯定远超 1 秒钟打开了 32 张帖子的频率，为何 caoliu 没对所有用户拒绝请求？显然，这些请求来自不同 IP 的电脑终端，按这个思路，如果 hardseed 若能通过多个不同 IP 访问 caoliu，对于代理服务器和被访服务器来说请求数量都变少了，那完全可以绕开 caoliu 对单个 IP 请求频率过快的限制。由于我们采用代理访问，发起访问请求的 IP 就是代理服务器的 IP，显然，只要 hardseed 支持同时使用多个代理服务器，那么一切问题就简单了。所以，我**赋予了 hardseed 多路代理的能力**。hardseed 支持 4 种代理模式：
* goagent (STRONGLY recommended), --proxy http://127.0.0.1:8087
* shadowsocks, --proxy socks5://127.0.0.1:1080, or socks5h://127.0.0.1:1080
* SSH, --proxy socks4://127.0.0.1:7070
* VPN (PPTP and openVPN), --proxy ""

其中，除 VPN 外（这是种全局代理模式），其他三种代理模式可混用，也就是说，你可以同时指定 goagent、shadowsocks、SSH 等三种代理模式
```
--proxy http://127.0.0.1:8087 socks5://127.0.0.1:1080 socks4://127.0.0.1:7070
```
这样，hardseed 就能用 8 * 3 条线程并行下载。另外，goagent 都是通过 GAE 集群发起到网络请求，所以不存在同个机器上配置多个 goagent 的做法；SSH（获取免费帐号 http://www.fastssh.com/ ） 和 shadowsocks（获取免费帐号 https://shadowsocks.net/get ） 代理，你可以获取多个不同的代理服务器（不同的 SSH 或者 shadowsocks 代理的本地端口必须自行设置成不同的），因此可以实现多个不同 IP 发起网络请求。换言之，你可以同时拥有 1 个 goagent、n 个 SSH、m 个 shadowsocks 个代理出口 IP，每个 IP 本来允许使用 8 条线程，那么共计就有 (1 + n + m) * 8 条线程并行下载，速度自然上去了。  
我个人偏爱 shadowsocks，以此举例来说：先在 https://shadowsocks.net/get 获取了 4 个 shadowsocks 帐号，本地端口分别配置成 1080、1081、1082、1083，运行此 4 个 shadowsocks 代理程序；同时，运行 goagent 代理程序；然后，在 hardseed 的命令行参数设定
```
--proxy http://127.0.0.1:8087 socks5://127.0.0.1:1080 socks5://127.0.0.1:1081 socks5://127.0.0.1:1082 socks5://127.0.0.1:1083
```
这时，如果你的 --concurrent-tasks 设定为 8（默认值），那么，hardseed 将启用 (4 + 1) * 8 条线程并行下载。那速度，飞快、快 ... *（注，有些 shadowsocks 代理服务器禁止下载，若有异常，将其从 --proxy 代理列表中剔除之。若求稳定，只用 goagent）*

**Q6**：如何搜索喜欢的视频？  
**A6**：--like 选项可以指定多个关键字（空格隔开）参数，帖子标题中出现相关关键字之一便纳入下载范围，否则不下载。通常来说，帖子标题中文字有简体、繁体、日文等三种可能，所以你应该都指定，比如，喜欢“护士”和“情侣”系列，先简译繁 http://www.aies.cn/ ，简译日 http://fanyi.baidu.com/#zh/jp/ ，再由 --topics-range 指定搜索的帖子数量，由 --like 指定搜索关键字：
```
--topics-range 1024 --like 护士 護士 看護婦 情侣 情侶 カップル
```

**Q7**：如何下载高清？  
**A7**：hardseed 并不直接支持高清类型下载，只能间接实现，由 --topics-range 指定搜索的帖子数量，由 --like 指定“高清”相关关键字进行下载，比如：
```
--topics-range 1024 --like 1080P 720P HD 高清 ハイビジョン
```

**Q8**：为何有些种子和图片名是无意义字符，类似 (rename)bltouujdrbwcrrcg.torrent？  
**A8**：OS 对文件名长度是有限制的，hardseed 是以帖子名作为种子和图片的文件名，一旦帖子名超长将导致文件名超长。由于 hardseed 是采用 ASCII 而非 UNICODE 作为字符存储方式，一个文字可能占一个字节（如，字母“a”）也可能占两个字节（如，汉字“好”），假如文件名最后一个文字是“好”，且刚好文件名超长了一个字节，如果 hardseed 简单地截断“好”的第二个字节，那将导致整个文件名变成乱码。所以，hardseed 用了另外种变通方式，取 16 个 a-z 间的随机字母以及前缀“(rename)”作为文件基础名。

**Q9**：为何相同的图片要下载两次？  
**A9**：有些发帖者担心单一图床挂掉，一般将同个图片上传到两个不同图床上，在帖子中同时发布两个图床的不同地址，hardseed 无法判断图片是否相同（其实非要弄也是可以实现的，只请求 HTTP 头，判断下两个图片的大小及最后更新时间，我觉得没这个必要），所以都下载。

**Q10**：为何常有类似下面的图片下载报错
```
failure (download error from http://cl.man.lv/htm_data/2/1407/1174338.html. pictures error: http://p1.imageab.com/2014/07/24/902135bff7a83cd71836764b795c0879.jpg, http://p1.imageab.com/2014/07/24/6cea50f80bba80536ba6cd9da7ba17df.jpg )
```
**A10**：几张图片下载失败无伤大雅。具体原因很多，常见如下：
* 图床挂了，hardseed 无能为力；
* 发帖者发布的图片 URL 有误，hardseed 无能为力；
* 图片太大、网速太慢，hardseed 在 --timeout-download-picture 指定时间内（默认 32 秒）未下载完整，这时，你可以将 --timeout-download-picture 指定为更大的下载等待时长（如，64），但这会增加整个下载时长；
* 代理服务器限制下载，禁用其他代理只用 goagent。

**Q11**：我没指定任何忽略关键字，为什么 hardseed 强制取消下载“连发, 連发, 连發, 連發, 连弹, ★㊣, 合辑, 合集, 合輯, nike, 最新の美女骑兵㊣, 精選, 精选”这类合集帖子？  
**A11**：两方面原因。一方面，合集均是把以往的单个帖子合并一起再发布，完全重复；一方面，虽然帖子中有多部不同片子的图片，但实际上帖子中的种子只是其中一部片子的，没有意义。

**Q12**：很多片子迅雷报违规资源，下载速度奇慢，如何破？  
**A12**：迅雷通过 URI 唯一确定资源，即便用 bencode 更改种子目录内的文件名也无济于事，所以仍然用迅雷的骚年，戒爱吧。首先，你得改用 QQ 旋风，其优势有三：一是大部分迅雷报违规的资源旋风中正常，二是旋风有个网页版支持跨平台（所以 linux 下诞生了 xfdown），三是资源消耗奇低；其次，对于旋风也报违规的资源，你可以先用各大网盘（比如，115 网盘、百度网盘）离线下载，然后再用旋风从网盘中下载回本地。结合这两种方式，下载速度慢的资源，基本上，不存在了。

**Q13**：hardseed 在 windows 环境下载的文件部分无法删除？  
**A13**：hardseed 正在写文件时被 ctrl-c 强制退出，文件锁未被 cyg\*.dll 释放，而 cyg\*.dll 已加载至 CMD 进程空间，所以，请先关闭所有 CMD 窗口，尝试删除相关文件，若不行，请再开新 CMD 窗口后执行
```
X:\> rd /S C:\[aicheng_west][1~128]@010825\
```

**Q14**：为何出现类似如下报错？
```
"" - failure (download error from http://cl.man.lv/htm_data/4/1408/1189943.html. seed error: )
```
**A14**：代理工具的问题。尝试：
* 设定 --concurrent-tasks 减少单个代理的并行下载数量；
* 如果使用 goagent 代理，重启之；若仍存在类似问题，请更换 GGC IP，即 proxy.ini 中的 iplist。可借助 checkgoogleip 查找你网络环境下速度最快的 GGC IP。
* 如果使用 SSH 或 shadowsocks 代理，请更换同类的其他服务器。


##忠告
-------------

你，党之栋梁、国之人才，注意身体，千万！

