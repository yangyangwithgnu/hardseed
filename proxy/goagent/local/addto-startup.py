#!/usr/bin/env python
# coding:utf-8

from __future__ import with_statement

__version__ = '1.0'

import sys
import os
import re
import time
import ctypes
import platform

python2 = os.popen('python2 -V 2>&1').read().startswith('Python 2.') and 'python2' or 'python'

def addto_startup_linux():
    filename = os.path.abspath(__file__)
    dirname = os.path.dirname(filename)
    #you can change it to 'proxy.py' if you like :)
    scriptname = 'goagent-gtk.py'
    DESKTOP_FILE = '''\
[Desktop Entry]
Type=Application
Categories=Network;Proxy;
Exec=/usr/bin/env %s "%s/%s"
Icon=%s/goagent-logo.png
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=GoAgent GTK
Comment=GoAgent GTK Launcher
''' % (python2, dirname , scriptname , dirname)
    #sometimes maybe  /etc/xdg/autostart , ~/.kde/Autostart/ , ~/.config/openbox/autostart
    for dirname in map(os.path.expanduser, ['~/.config/autostart']):
        if os.path.isdir(dirname):
            filename = os.path.join(dirname, 'goagent-gtk.desktop')
            with open(filename, 'w') as fp:
                fp.write(DESKTOP_FILE)
           # os.chmod(filename, 0755)


def addto_startup_osx():
    if os.getuid() != 0:
        print 'please use sudo run this script'
        sys.exit()
    import plistlib
    plist = dict(
            GroupName = 'wheel',
            Label = 'org.goagent.macos',
            ProgramArguments = list([
                '/usr/bin/%s' % python2,
                os.path.join(os.path.abspath(os.path.dirname(__file__)), 'proxy.py')
                ]),
            RunAtLoad = True,
            UserName = 'root',
            WorkingDirectory = os.path.dirname(__file__),
            StandardOutPath = '/var/log/goagent.log',
            StandardErrorPath = '/var/log/goagent.log',
            KeepAlive = dict(
                SuccessfulExit = False,
                )
            )
    filename = '/Library/LaunchDaemons/org.goagent.macos.plist'
    print 'write plist to %s' % filename
    plistlib.writePlist(plist, filename)
    print 'write plist to %s done' % filename
    print 'Adding CA.crt to system keychain, You may need to input your password...'
    cmd = 'sudo security add-trusted-cert -d -r trustRoot -k "/Library/Keychains/System.keychain" "%s/CA.crt"' % os.path.abspath(os.path.dirname(__file__))
    if os.system(cmd) != 0:
        print 'Adding CA.crt to system keychain Failed!'
        sys.exit(0)
    print 'Adding CA.crt to system keychain Done'
    print 'To start goagent right now, try this command: sudo launchctl load /Library/LaunchDaemons/org.goagent.macos.plist'
    print 'To checkout log file: using Console.app to locate /var/log/goagent.log'

    install_sharp_osx()


def install_sharp_osx():
    # extracted from SwitchySharp.crx
    extension_id = 'dpplabbmogkhghncfbfdeeokoefdjegm'
    extension_version = '1.10.2'
    extension_path = '%s/SwitchySharp.crx' % os.path.abspath(os.path.dirname(__file__))

    dest_path = '/Library/Application Support/Google/Chrome/External Extensions'
    dest_file = '%s/%s.json' % (dest_path, extension_id)
    print 'Installing SwitchySharp for Chrome...'
    cmd = 'mkdir -p "%s"' % dest_path
    if os.system(cmd) != 0:
        print 'Create Chrome External Extensions folder Failed!'
        sys.exit(0)

    json_dict = {'external_crx': extension_path,
                 'external_version': extension_version}
    with open(dest_file, 'w') as fp:
        import json
        json.dump(json_dict, fp)
        print 'Installing SwitchySharp done.'


def addto_startup_windows():
    if 1 == ctypes.windll.user32.MessageBoxW(None, u'是否将goagent.exe加入到启动项？', u'GoAgent 对话框', 1):
        if 1 == ctypes.windll.user32.MessageBoxW(None, u'是否显示托盘区图标？', u'GoAgent 对话框', 1):
            pass


def addto_startup_unknown():
    print '*** error: Unknown system'


def main():
    addto_startup_funcs = {
            'Darwin'    : addto_startup_osx,
            'Windows'   : addto_startup_windows,
            'Linux'     : addto_startup_linux,
            }
    addto_startup_funcs.get(platform.system(), addto_startup_unknown)()


if __name__ == '__main__':
   try:
       main()
   except KeyboardInterrupt:
       pass
