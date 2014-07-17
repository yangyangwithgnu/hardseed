
#hardseed
yangyang.gnu@gmail.com

![hardseed gif demo](https://raw.githubusercontent.com/yangyangwithgnu/hardseed/master/pic/hardseed.gif)

----------------
##english


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
There are twelve av classes: 
- caoliu_west_reposted
- caoliu_cartoon_reposted
- caoliu_asia_mosaicked_reposted
- caoliu_asia_non_mosaicked_reposted
- caoliu_west_original
- caoliu_cartoon_original
- caoliu_asia_mosaicked_original
- caoliu_asia_non_mosaicked_original
- aicheng_west
- aicheng_cartoon
- aicheng_asia_mosaicked
- aicheng_asia_non_mosaicked  

As the name implies, "caoliu" stands for CaoLiu forum, "aicheng" for AiCheng forum, "reposted" and "original" is clearity, you konw which one is your best lover (yes, only one).   
The default is aicheng_asia_mosaicked.   

--concurrent-tasks  
You can set more than one proxy, each proxy could more than one concurrent tasks. This option set the number of concurrent tasks of each prox.   
The max and default number is 16.   

--timeout-download-picture  
Some pictures too big to download in few seconds. So, you should set the download picture timeout seconds.   
The default timeout is 32 seconds.  

--topics-range  
Set the range of to download topics. E.G.:
- topics-range 2 16
- topics-range 8 (I.E., --topics-range 1 8)
- topics-range -1 (I.E., all topics of this av class)  

The default topics range is 128.

--saveas-path  
Set the path to save seeds and pictures. The rule of dir: [avclass][range]@hhmmss. E.G., [aicheng_west][2~32]@124908/. 
The default directory is home directory.   

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
If you wanna how to install and configure various kinds of proxy, please access my homepage "3.3 搭梯翻墙" http://www.yangyangwithgnu.net/the_new_world_linux/#index_3_3   
The default http://127.0.0.1:8087.   

That's all. Any suggestions let me know by yangyang.gnu@gmail.com or http://www.yangyangwithgnu.net/, big thanks to you. Kiddo, take care of your body. :-)  


##中文
--------
硬盘女神，你懂嘀！hardseed 是个种子下载工具，它从浓（ai）情（cheng）蜜（she）意（qu）和爱（cao）意（liu）无（she）限（qu）的地方获取女神种子、图片。  

###【翻墙】  
你知道，这一切的一切都在墙外，所以你得具备翻墙环境，hardseed 才能正常帮你拉女神。hardseed 支持 GoAgent、shadowsocks、SSH、VPN （PPTP 和 openVPN）等各类代理模式，甚至你可以并行使用多种代理以极速下载。从普及度、稳定性、高效性来看，GoAgent 最优。“我一技术小白，工作压力大，就想看看女神轻松下，你还让我折腾代理？我恨你！”，嘚，亲，我错了。我帮你配置了一份开箱即用的 goagent，位于 hardseed/proxy/goagent/local/，linux 用户，命令行中运行
```
$ python proxy.py
```
windows 亲，双击运行 goagent.exe （**管理员权限**）。  


###【源码安装】  

####『windows』  
这基本没 windows 用户什么事儿，除非你有 cygwin，否则你没法编译源码，没事，我服务很到位的，帮你弄好了，二进制执行程序位于 hardseed/bin/windows/hardseed.exe
 
####『linux』  
0）唯一依赖 libcurl，请自行安装；  
1）代码采用 C++11 编写，gcc 版本不低于 4.7.1。  
2）命令行下运行：  
```
$ cd hardseed/build/
$ cmake .
$ make && make install
```

###【使用】  
**听好了，运行 hardseed 前务必确保代理程序已正常运行，否则，别说女神，蚊子都碰不到。**

####『windows』  
先进入 hardseed\bin\windows\，找到并选中 hardseed.exe，右键设置**以管理员权限运行该程序**，接着键入 ctrl-d 将光标定位到文件管理器的地址栏中，键入 CMD 启动命令行窗口，再在 CMD 中键入
```
X:\hardseed\bin\windows> hardseed.exe
```
这时，hardseed 开始玩命儿为你下载女神图片和种子，约 1 分钟左右，在你 home 目录下会生成类似 C:\Users\Administrator\[aicheng_asia_mosaicked][1~128]@014822\ 的目录，女神们在此！

####『linux』  
同 windows 下运行一样，全用默认命令行参数运行
```
$ hardseed
```
执行完成后，你会看到 ~/[aicheng_asia_mosaicked][1~128]@014822/，你要的都在那儿。或者，玩点高级的
```
$ hardseed --saveas-path ~/downloads --topics-range 256 --av-class aicheng_west
```
其中，--saveas-path 指定存放路径为 ~/downloads/；--topics-range 指定解析的帖子范围从第 1 张帖子到第 256 张帖子；--av-class 指定女神类型为欧美。

###【演示】  
http://v.youku.com/v_show/id_XNzQxOTk0NTE2.html


骚年，您可千万注意身体！

