@echo off
REM ________________________________________________________________
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo �������ԱȨ��...
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

@echo ------------------��HardSeed��---------------------
@echo                by yangyangwithgnu
@echo Github��https://github.com/yangyangwithgnu/hardseed
@echo      this  script is writed by xuzhenglun

@echo off
@echo *****************��������Щ���ࣺ*******************  
@echo --------��1.   ����_����_ת��
@echo --------��2.   ����_��ͨ_ת��
@echo --------��3.   ����_����_����_ת��
@echo --------��4.   ����_����_����_ת��
@echo --------��5.   ����_����_ԭ��
@echo --------��6.   ����_��ͨ_ԭ��
@echo --------��7.   ����_����_����_ԭ��
@echo --------��8.   ����_����_����_ԭ��
@echo --------��9.   ����_����
@echo --------��10.  ����_����
@echo --------��11.  ����_��ͨ
@echo --------��12.  ����_����_����
@echo --------��13.  ����_����_����


set var=4
set timeout=-2
set trange=-2
set thate=-2
set tlike=-2
set tproxy=""
set task=-2
set path=-2

set /p var=������AV��������:
cls
set /p timeout=�����볬ʱʱ�䣨Ĭ��16�룩��
cls
set /p task=�����߳�����1��8���ʵ��Ӵ���Լ��٣����ǹ������ܱ���������Ϊ������������һ��ʱ�䣬Ĭ��8����
cls
set /p trange=������Ҫ���صķ�Χ��Ĭ��64��������-1��Ϊ���У�:
cls
set /p thate=����һЩ���˹ؼ��ʣ����صĽ�������������Ĺؼ��ʣ�
cls
set /p tlike=����һЩ����Ȥ�Ĵʣ�
cls
@echo ������������ã�
@echo ֧��Goanent��Shadowsocks��SSH����VPN
@echo GoAgent��    ����  http://127.0.0.1:8087
@echo shadowsocks������socks5://127.0.0.1:1080 �� socks5h://127.0.0.1:1080
@echo SSH          ����socks4://127.0.0.1:7070
set /p tproxy=��������������(Ĭ�ϲ����ô��������):
cls
set /p path=���뱣��·����Ĭ��C��Ŀ¼����


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
@echo ������ϣ�Ĭ�����ص��ļ�������C��Ŀ¼�£��뼰ʱ����
pause