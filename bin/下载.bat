@echo off
REM ________________________________________________________________
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo 请求管理员权限...
    goto UACPrompt
) else ( goto gotAdmin )
:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B
:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"
REM ________________________________________________________________

@echo ------------------》HardSeed《---------------------
@echo                by yangyangwithgnu
@echo Github：https://github.com/yangyangwithgnu/hardseed
@echo      this  script is writed by xuzhenglun

@echo off
@echo *****************有以下这些种类：*******************  
@echo --------》1.   草榴_西方_转贴
@echo --------》2.   草榴_卡通_转贴
@echo --------》3.   草榴_亚洲_有码_转贴
@echo --------》4.   草榴_亚洲_无码_转贴
@echo --------》5.   草榴_西方_原创
@echo --------》6.   草榴_卡通_原创
@echo --------》7.   草榴_亚洲_有码_原创
@echo --------》8.   草榴_亚洲_无码_原创
@echo --------》9.   草榴_自拍
@echo --------》10.  爱城_西方
@echo --------》11.  爱城_卡通
@echo --------》12.  爱城_亚洲_有码
@echo --------》13.  爱城_亚洲_无码


set var=4
set timeout=-2
set trange=-2
set thate=-2
set tlike=-2
set tproxy=""
set task=-2
set path=-2

set /p var=请输入AV种类的序号:
cls
set /p timeout=请输入超时时间（默认16秒）：
cls
set /p task=输入线程数（1～8，适当加大可以加速，但是过大会可能被服务器认为不正常被屏蔽一段时间，默认8）：
cls
set /p trange=请输入要下载的范围（默认64，若输入-1则为所有）:
cls
set /p thate=输入一些过滤关键词，下载的将不包括所输入的关键词：
cls
set /p tlike=输入一些感兴趣的词：
cls
@echo 代理服务器设置：
@echo 支持Goanent，Shadowsocks，SSH，和VPN
@echo GoAgent：    形如  http://127.0.0.1:8087
@echo shadowsocks：形如socks5://127.0.0.1:1080 或 socks5h://127.0.0.1:1080
@echo SSH          形如socks4://127.0.0.1:7070
set /p tproxy=请输入代理服务器(默认不启用代理服务器):
cls
set /p path=输入保存路径（默认C根目录）：


if %var%==1 set class=caoliu_west_reposted
if %var%==2 set class=caoliu_cartoon_reposted
if %var%==3 set class=caoliu_asia_mosaicked_reposted
if %var%==4 set class=caoliu_asia_non_mosaicked_reposted
if %var%==5 set class=caoliu_west_original
if %var%==6 set class=caoliu_cartoon_original
if %var%==7 set class=caoliu_asia_mosaicked_original
if %var%==8 set class=caoliu_asia_non_mosaicked_original
if %var%==9 set class=caoliu_selfie
if %var%==10 set class=aicheng_west
if %var%==11 set class=aicheng_cartoon
if %var%==12 set class=aicheng_asia_mosaicked
if %var%==13 set class=aicheng_asia_non_mosaicked


set av-class= 
set timeout-download-picture= 
set range= 
set hate= 
set like= 
set proxy=--proxy %tproxy%
set concurrent-tasks= 
set saveas-path= 

set av-class=--av-class %class%
if %timeout% neq -2 (set timeout-download-picture=--timeout-download-picture %timeout%)
if %trange% neq -2 (set range=--range %trange%)
if %thate% neq -2 (set hate=--hate %thate%)
if %tlike% neq -2 (set like=--like %tlike%)
if %tlike% neq -2 (set concurrent-tasks=--concurrent-tasks %task%)
if %path% neq -2 (set saveas-path=--saveas-path %path%)
cls

.\windows\hardseed %concurrent-tasks% %av-class% %timeout-download-picture% %range% %like% %hate% %proxy% %saveas-path%
cls 
@echo 下载完毕，默认下载的文件保存在C根目录下，请及时查收
pause