#!/usr/bin/env python2
# coding:utf-8
# Contributor:
#      Phus Lu        <phus.lu@gmail.com>

__version__ = '1.6'

GOAGENT_LOGO_DATA = """\
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
AAAASUVORK5CYII="""

import sys
import os
import re
import thread
import base64
import platform

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    gtk.gdk.threads_init()
except Exception:
    sys.exit(os.system(u'gdialog --title "GoAgent GTK" --msgbox "\u8bf7\u5b89\u88c5 python-gtk2" 15 60'.encode(sys.getfilesystemencoding() or sys.getdefaultencoding(), 'replace')))
try:
    import pynotify
    pynotify.init('GoAgent Notify')
except ImportError:
    pynotify = None
try:
    import appindicator
except ImportError:
    appindicator = None
try:
    import vte
except ImportError:
    sys.exit(gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, u'请安装 python-vte').run())


def spawn_later(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        import time
        time.sleep(seconds)
        return target(*args, **kwargs)
    return thread.start_new_thread(wrap, args, kwargs)


def drop_desktop():
    filename = os.path.abspath(__file__)
    dirname = os.path.dirname(filename)
    DESKTOP_FILE = '''\
#!/usr/bin/env xdg-open
[Desktop Entry]
Type=Application
Name=GoAgent GTK
Comment=GoAgent GTK Launcher
Categories=Network;Proxy;
Exec=/usr/bin/env python "%s"
Icon=%s/goagent-logo.png
Terminal=false
StartupNotify=true
''' % (filename, dirname)
    for dirname in map(os.path.expanduser, ['~/Desktop', u'~/桌面']):
        if os.path.isdir(dirname):
            filename = os.path.join(dirname, 'goagent-gtk.desktop')
            with open(filename, 'w') as fp:
                fp.write(DESKTOP_FILE)
            os.chmod(filename, 0755)


def should_visible():
    import ConfigParser
    ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
    config = ConfigParser.ConfigParser()
    config.read(['proxy.ini', 'proxy.user.ini'])
    visible = config.has_option('listen', 'visible') and config.getint('listen', 'visible')
    return visible

#gtk.main_quit = lambda: None
#appindicator = None


class GoAgentGTK:

    command = ['/usr/bin/env', 'python', 'proxy.py']
    message = u'GoAgent已经启动，单击托盘图标可以最小化'
    fail_message = u'GoAgent启动失败，请查看控制台窗口的错误信息。'

    def __init__(self, window, terminal):
        self.window = window
        self.window.set_size_request(652, 447)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect('delete-event',self.delete_event)
        self.terminal = terminal

        for cmd in ('python2.7', 'python27', 'python2'):
            if os.system('which %s' % cmd) == 0:
                self.command[1] = cmd
                break

        self.window.add(terminal)
        self.childpid = self.terminal.fork_command(self.command[0], self.command, os.getcwd())
        if self.childpid > 0:
            self.childexited = self.terminal.connect('child-exited', self.on_child_exited)
            self.window.connect('delete-event', lambda w, e: gtk.main_quit())
        else:
            self.childexited = None

        spawn_later(0.5, self.show_startup_notify)

        if should_visible():
            self.window.show_all()

        logo_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'goagent-logo.png')
        if not os.path.isfile(logo_filename):
            with open(logo_filename, 'wb') as fp:
                fp.write(base64.b64decode(GOAGENT_LOGO_DATA))
        self.window.set_icon_from_file(logo_filename)

        if appindicator:
            self.trayicon = appindicator.Indicator('GoAgent', 'indicator-messages', appindicator.CATEGORY_APPLICATION_STATUS)
            self.trayicon.set_status(appindicator.STATUS_ACTIVE)
            self.trayicon.set_attention_icon('indicator-messages-new')
            self.trayicon.set_icon(logo_filename)
            self.trayicon.set_menu(self.make_menu())
        else:
            self.trayicon = gtk.StatusIcon()
            self.trayicon.set_from_file(logo_filename)
            self.trayicon.connect('popup-menu', lambda i, b, t: self.make_menu().popup(None, None, gtk.status_icon_position_menu, b, t, self.trayicon))
            self.trayicon.connect('activate', self.show_hide_toggle)
            self.trayicon.set_tooltip('GoAgent')
            self.trayicon.set_visible(True)

    def make_menu(self):
        menu = gtk.Menu()
        itemlist = [(u'\u663e\u793a', self.on_show),
                    (u'\u9690\u85cf', self.on_hide),
                    (u'\u505c\u6b62', self.on_stop),
                    (u'\u91cd\u65b0\u8f7d\u5165', self.on_reload),
                    (u'\u9000\u51fa', self.on_quit)]
        for text, callback in itemlist:
            item = gtk.MenuItem(text)
            item.connect('activate', callback)
            item.show()
            menu.append(item)
        menu.show()
        return menu

    def show_notify(self, message=None, timeout=None):
        if pynotify and message:
            notification = pynotify.Notification('GoAgent Notify', message)
            notification.set_hint('x', 200)
            notification.set_hint('y', 400)
            if timeout:
                notification.set_timeout(timeout)
            notification.show()

    def show_startup_notify(self):
        if self.check_child_exists():
            self.show_notify(self.message, timeout=3)

    def check_child_exists(self):
        if self.childpid <= 0:
            return False
        cmd = 'ps -p %s' % self.childpid
        lines = os.popen(cmd).read().strip().splitlines()
        if len(lines) < 2:
            return False
        return True

    def on_child_exited(self, term):
        if self.terminal.get_child_exit_status() == 0:
            gtk.main_quit()
        else:
            self.show_notify(self.fail_message)

    def on_show(self, widget, data=None):
        self.window.show_all()
        self.window.present()
        self.terminal.feed('\r')

    def on_hide(self, widget, data=None):
        self.window.hide_all()

    def on_stop(self, widget, data=None):
        if self.childexited:
            self.terminal.disconnect(self.childexited)
        os.system('kill -9 %s' % self.childpid)

    def on_reload(self, widget, data=None):
        if self.childexited:
            self.terminal.disconnect(self.childexited)
        os.system('kill -9 %s' % self.childpid)
        self.on_show(widget, data)
        self.childpid = self.terminal.fork_command(self.command[0], self.command, os.getcwd())
        self.childexited = self.terminal.connect('child-exited', lambda term: gtk.main_quit())

    def show_hide_toggle(self, widget, data= None):
        if self.window.get_property('visible'):
            self.on_hide(widget, data)
        else:
            self.on_show(widget, data)

    def delete_event(self, widget, data=None):
        self.on_hide(widget, data)
        # 默认最小化至托盘
        return True

    def on_quit(self, widget, data=None):
        gtk.main_quit()


def main():
    global __file__
    __file__ = os.path.abspath(__file__)
    if os.path.islink(__file__):
        __file__ = getattr(os, 'readlink', lambda x: x)(__file__)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if not os.path.exists('goagent-logo.png'):
        # first run and drop shortcut to desktop
        drop_desktop()

    window = gtk.Window()
    terminal = vte.Terminal()
    GoAgentGTK(window, terminal)
    gtk.main()

if __name__ == '__main__':
    main()
