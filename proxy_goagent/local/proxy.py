#!/usr/bin/env python
# coding:utf-8
# Based on GAppProxy 2.0.0 by Du XiaoGang <dugang.2008@gmail.com>
# Based on WallProxy 0.4.0 by Hust Moon <www.ehust@gmail.com>
# Contributor:
#      Phus Lu           <phus.lu@gmail.com>
#      Hewig Xu          <hewigovens@gmail.com>
#      Ayanamist Yang    <ayanamist@gmail.com>
#      V.E.O             <V.E.O@tom.com>
#      Max Lv            <max.c.lv@gmail.com>
#      AlsoTang          <alsotang@gmail.com>
#      Christopher Meng  <i@cicku.me>
#      Yonsm Guo         <YonsmGuo@gmail.com>
#      Parkman           <cseparkman@gmail.com>
#      Ming Bai          <mbbill@gmail.com>
#      Bin Yu            <yubinlove1991@gmail.com>
#      lileixuan         <lileixuan@gmail.com>
#      Cong Ding         <cong@cding.org>
#      Zhang Youfu       <zhangyoufu@gmail.com>
#      Lu Wei            <luwei@barfoo>
#      Harmony Meow      <harmony.meow@gmail.com>
#      logostream        <logostream@gmail.com>
#      Rui Wang          <isnowfy@gmail.com>
#      Wang Wei Qiang    <wwqgtxx@gmail.com>
#      Felix Yan         <felixonmars@gmail.com>
#      Sui Feng          <suifeng.me@qq.com>
#      QXO               <qxodream@gmail.com>
#      Geek An           <geekan@foxmail.com>
#      Poly Rabbit       <mcx_221@foxmail.com>
#      oxnz              <yunxinyi@gmail.com>
#      Shusen Liu        <liushusen.smart@gmail.com>
#      Yad Smood         <y.s.inside@gmail.com>
#      Chen Shuang       <cs0x7f@gmail.com>
#      cnfuyu            <cnfuyu@gmail.com>
#      cuixin            <steven.cuixin@gmail.com>
#      s2marine0         <s2marine0@gmail.com>
#      Toshio Xiang      <snachx@gmail.com>
#      Bo Tian           <dxmtb@163.com>
#      Virgil            <variousvirgil@gmail.com>
#      hub01             <miaojiabumiao@yeah.net>
#      v3aqb             <sgzz.cj@gmail.com>
#      Oling Cat         <olingcat@gmail.com>
#      Meng Zhuo         <mengzhuo1203@gmail.com>
#      zwhfly            <zwhfly@163.com>
#      Hubertzhang       <hubert.zyk@gmail.com>
#      arrix             <arrixzhou@gmail.com>

__version__ = '3.1.21'

import sys
import os
import sysconfig

reload(sys).setdefaultencoding('UTF-8')
sys.dont_write_bytecode = True
sys.path += [os.path.abspath(os.path.join(__file__, '../packages.egg/%s' % x)) for x in ('noarch', sysconfig.get_platform().split('-')[0])]

import gevent
import gevent.socket
import gevent.server
import gevent.queue
import gevent.monkey
gevent.monkey.patch_all()

import errno
import time
import struct
import collections
import zlib
import httplib
import re
import io
import traceback
import random
import base64
import uuid
import urlparse
import threading
import thread
import socket
import ssl
import Queue
import ConfigParser
import urllib2

import OpenSSL

NetWorkIOError = (socket.error, ssl.SSLError, OpenSSL.SSL.Error, OSError)

class Logging(type(sys)):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self, *args, **kwargs):
        self.level = self.__class__.INFO
        self.__set_error_color = lambda: None
        self.__set_warning_color = lambda: None
        self.__set_debug_color = lambda: None
        self.__reset_color = lambda: None
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            if os.name == 'nt':
                import ctypes
                SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute
                GetStdHandle = ctypes.windll.kernel32.GetStdHandle
                self.__set_error_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x04)
                self.__set_warning_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x06)
                self.__set_debug_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x002)
                self.__reset_color = lambda: SetConsoleTextAttribute(GetStdHandle(-11), 0x07)
            elif os.name == 'posix':
                self.__set_error_color = lambda: sys.stderr.write('\033[31m')
                self.__set_warning_color = lambda: sys.stderr.write('\033[33m')
                self.__set_debug_color = lambda: sys.stderr.write('\033[32m')
                self.__reset_color = lambda: sys.stderr.write('\033[0m')

    @classmethod
    def getLogger(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def basicConfig(self, *args, **kwargs):
        self.level = int(kwargs.get('level', self.__class__.INFO))
        if self.level > self.__class__.DEBUG:
            self.debug = self.dummy

    def log(self, level, fmt, *args, **kwargs):
        sys.stderr.write('%s - [%s] %s\n' % (level, time.ctime()[4:-5], fmt % args))

    def dummy(self, *args, **kwargs):
        pass

    def debug(self, fmt, *args, **kwargs):
        self.__set_debug_color()
        self.log('DEBUG', fmt, *args, **kwargs)
        self.__reset_color()

    def info(self, fmt, *args, **kwargs):
        self.log('INFO', fmt, *args)

    def warning(self, fmt, *args, **kwargs):
        self.__set_warning_color()
        self.log('WARNING', fmt, *args, **kwargs)
        self.__reset_color()

    def warn(self, fmt, *args, **kwargs):
        self.warning(fmt, *args, **kwargs)

    def error(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('ERROR', fmt, *args, **kwargs)
        self.__reset_color()

    def exception(self, fmt, *args, **kwargs):
        self.error(fmt, *args, **kwargs)
        sys.stderr.write(traceback.format_exc() + '\n')

    def critical(self, fmt, *args, **kwargs):
        self.__set_error_color()
        self.log('CRITICAL', fmt, *args, **kwargs)
        self.__reset_color()
logging = sys.modules['logging'] = Logging('logging')


from proxylib import AuthFilter
from proxylib import AutoRangeFilter
from proxylib import BaseFetchPlugin
from proxylib import BaseProxyHandlerFilter
from proxylib import BlackholeFilter
from proxylib import CertUtil
from proxylib import CipherFileObject
from proxylib import deflate
from proxylib import DirectFetchPlugin
from proxylib import DirectRegionFilter
from proxylib import dnslib_record2iplist
from proxylib import dnslib_resolve_over_tcp
from proxylib import dnslib_resolve_over_udp
from proxylib import FakeHttpsFilter
from proxylib import ForceHttpsFilter
from proxylib import CRLFSitesFilter
from proxylib import get_dnsserver_list
from proxylib import get_process_list
from proxylib import get_uptime
from proxylib import inflate
from proxylib import JumpLastFilter
from proxylib import LocalProxyServer
from proxylib import message_html
from proxylib import MockFetchPlugin
from proxylib import MultipleConnectionMixin
from proxylib import ProxyConnectionMixin
from proxylib import ProxyUtil
from proxylib import RC4Cipher
from proxylib import SimpleProxyHandler
from proxylib import spawn_later
from proxylib import SSLConnection
from proxylib import StaticFileFilter
from proxylib import StripPlugin
from proxylib import URLRewriteFilter
from proxylib import UserAgentFilter
from proxylib import XORCipher


def is_google_ip(ipaddr):
    if ipaddr in ('74.125.127.102', '74.125.155.102', '74.125.39.102', '74.125.39.113', '209.85.229.138'):
        return False
    if ipaddr.startswith(('173.194.', '207.126.', '209.85.', '216.239.', '64.18.', '64.233.', '66.102.', '66.249.', '72.14.', '74.125.')):
        return True
    return False


class RangeFetch(object):
    """Range Fetch Class"""

    threads = 2
    maxsize = 1024*1024*4
    bufsize = 8192
    waitsize = 1024*512

    def __init__(self, handler, plugin, response, fetchservers, **kwargs):
        assert isinstance(plugin, BaseFetchPlugin) and hasattr(plugin, 'fetch')
        self.handler = handler
        self.url = handler.path
        self.plugin = plugin
        self.response = response
        self.fetchservers = fetchservers
        self.kwargs = kwargs
        self._stopped = None
        self._last_app_status = {}
        self.expect_begin = 0

    def fetch(self):
        response_status = self.response.status
        response_headers = dict((k.title(), v) for k, v in self.response.getheaders())
        content_range = response_headers['Content-Range']
        #content_length = response_headers['Content-Length']
        start, end, length = tuple(int(x) for x in re.search(r'bytes (\d+)-(\d+)/(\d+)', content_range).group(1, 2, 3))
        if start == 0:
            response_status = 200
            response_headers['Content-Length'] = str(length)
            del response_headers['Content-Range']
        else:
            response_headers['Content-Range'] = 'bytes %s-%s/%s' % (start, end, length)
            response_headers['Content-Length'] = str(length-start)

        logging.info('>>>>>>>>>>>>>>> RangeFetch started(%r) %d-%d', self.url, start, end)
        self.handler.send_response(response_status)
        for key, value in response_headers.items():
            self.handler.send_header(key, value)
        self.handler.end_headers()

        data_queue = Queue.PriorityQueue()
        range_queue = Queue.PriorityQueue()
        range_queue.put((start, end, self.response))
        self.expect_begin = start
        for begin in range(end+1, length, self.maxsize):
            range_queue.put((begin, min(begin+self.maxsize-1, length-1), None))
        for i in xrange(0, self.threads):
            range_delay_size = i * self.maxsize
            spawn_later(float(range_delay_size)/self.waitsize, self.__fetchlet, range_queue, data_queue, range_delay_size)
        has_peek = hasattr(data_queue, 'peek')
        peek_timeout = 120
        while self.expect_begin < length - 1:
            try:
                if has_peek:
                    begin, data = data_queue.peek(timeout=peek_timeout)
                    if self.expect_begin == begin:
                        data_queue.get()
                    elif self.expect_begin < begin:
                        time.sleep(0.1)
                        continue
                    else:
                        logging.error('RangeFetch Error: begin(%r) < expect_begin(%r), quit.', begin, self.expect_begin)
                        break
                else:
                    begin, data = data_queue.get(timeout=peek_timeout)
                    if self.expect_begin == begin:
                        pass
                    elif self.expect_begin < begin:
                        data_queue.put((begin, data))
                        time.sleep(0.1)
                        continue
                    else:
                        logging.error('RangeFetch Error: begin(%r) < expect_begin(%r), quit.', begin, self.expect_begin)
                        break
            except Queue.Empty:
                logging.error('data_queue peek timeout, break')
                break
            try:
                self.handler.wfile.write(data)
                self.expect_begin += len(data)
                del data
            except StandardError as e:
                logging.info('RangeFetch client connection aborted(%s).', e)
                break
        self._stopped = True

    def __fetchlet(self, range_queue, data_queue, range_delay_size):
        headers = dict((k.title(), v) for k, v in self.handler.headers.items())
        headers['Connection'] = 'close'
        while 1:
            try:
                if self._stopped:
                    return
                try:
                    start, end, response = range_queue.get(timeout=1)
                    if self.expect_begin < start and data_queue.qsize() * self.bufsize + range_delay_size > 30*1024*1024:
                        range_queue.put((start, end, response))
                        time.sleep(10)
                        continue
                    headers['Range'] = 'bytes=%d-%d' % (start, end)
                    fetchserver = ''
                    if not response:
                        fetchserver = random.choice(self.fetchservers)
                        if self._last_app_status.get(fetchserver, 200) >= 500:
                            time.sleep(5)
                        response = self.plugin.fetch(self.handler, self.handler.command, self.url, headers, self.handler.body, timeout=self.handler.connect_timeout, fetchserver=fetchserver, **self.kwargs)
                except Queue.Empty:
                    continue
                except StandardError as e:
                    logging.warning("Response %r in __fetchlet", e)
                    range_queue.put((start, end, None))
                    continue
                if not response:
                    logging.warning('RangeFetch %s return %r', headers['Range'], response)
                    range_queue.put((start, end, None))
                    continue
                if fetchserver:
                    self._last_app_status[fetchserver] = response.app_status
                if response.app_status != 200:
                    logging.warning('Range Fetch "%s %s" %s return %s', self.handler.command, self.url, headers['Range'], response.app_status)
                    response.close()
                    range_queue.put((start, end, None))
                    continue
                if response.getheader('Location'):
                    self.url = urlparse.urljoin(self.url, response.getheader('Location'))
                    logging.info('RangeFetch Redirect(%r)', self.url)
                    response.close()
                    range_queue.put((start, end, None))
                    continue
                if 200 <= response.status < 300:
                    content_range = response.getheader('Content-Range')
                    if not content_range:
                        logging.warning('RangeFetch "%s %s" return Content-Range=%r: response headers=%r', self.handler.command, self.url, content_range, response.getheaders())
                        response.close()
                        range_queue.put((start, end, None))
                        continue
                    content_length = int(response.getheader('Content-Length', 0))
                    logging.info('>>>>>>>>>>>>>>> [thread %s] %s %s', threading.currentThread().ident, content_length, content_range)
                    while 1:
                        try:
                            if self._stopped:
                                response.close()
                                return
                            data = response.read(self.bufsize)
                            if not data:
                                break
                            data_queue.put((start, data))
                            start += len(data)
                        except StandardError as e:
                            logging.warning('RangeFetch "%s %s" %s failed: %s', self.handler.command, self.url, headers['Range'], e)
                            break
                    if start < end + 1:
                        logging.warning('RangeFetch "%s %s" retry %s-%s', self.handler.command, self.url, start, end)
                        response.close()
                        range_queue.put((start, end, None))
                        continue
                    logging.info('>>>>>>>>>>>>>>> Successfully reached %d bytes.', start - 1)
                else:
                    logging.error('RangeFetch %r return %s', self.url, response.status)
                    response.close()
                    range_queue.put((start, end, None))
                    continue
            except StandardError as e:
                logging.exception('RangeFetch._fetchlet error:%s', e)
                raise


class GAEFetchPlugin(BaseFetchPlugin):
    """direct fetch plugin"""
    connect_timeout = 4
    max_retry = 2

    def __init__(self, appids, password, path, mode, cachesock, keepalive, obfuscate, pagespeed, validate, options):
        BaseFetchPlugin.__init__(self)
        self.appids = appids
        self.password = password
        self.path = path
        self.mode = mode
        self.cachesock = cachesock
        self.keepalive = keepalive
        self.obfuscate = obfuscate
        self.pagespeed = pagespeed
        self.validate = validate
        self.options = options

    def handle(self, handler, **kwargs):
        assert handler.command != 'CONNECT'
        method = handler.command
        headers = dict((k.title(), v) for k, v in handler.headers.items())
        body = handler.body
        if handler.path[0] == '/':
            url = '%s://%s%s' % (handler.scheme, handler.headers['Host'], handler.path)
        elif handler.path.lower().startswith(('http://', 'https://', 'ftp://')):
            url = handler.path
        else:
            raise ValueError('URLFETCH %r is not a valid url' % handler.path)
        errors = []
        response = None
        for i in xrange(self.max_retry):
            try:
                response = self.fetch(handler, method, url, headers, body, self.connect_timeout)
                if response.app_status < 400:
                    break
                else:
                    if response.app_status == 503:
                        # appid over qouta, switch to next appid
                        if len(self.appids) > 1:
                            self.appids.append(self.appids.pop(0))
                            logging.info('gae over qouta, switch next appid=%r', self.appids[0])
                    if i < self.max_retry - 1 and len(self.appids) > 1:
                        self.appids.append(self.appids.pop(0))
                        logging.info('URLFETCH return %d, trying next appid=%r', response.app_status, self.appids[0])
                    response.close()
            except StandardError as e:
                errors.append(e)
                logging.info('GAE "%s %s" appid=%r %r, retry...', handler.command, handler.path, self.appids[0], e)
        if len(errors) == self.max_retry:
            if response and response.app_status >= 500:
                status = response.app_status
                headers = dict(response.getheaders())
                content = response.read()
                response.close()
            else:
                status = 502
                headers = {'Content-Type': 'text/html'}
                content = message_html('502 URLFetch failed', 'Local URLFetch %r failed' % handler.path, '<br>'.join(repr(x) for x in errors))
            return handler.handler_plugins['mock'].handle(handler, status, headers, content)
        logging.info('%s "GAE %s %s %s" %s %s', handler.address_string(), handler.command, handler.path, handler.protocol_version, response.status, response.getheader('Content-Length', '-'))
        try:
            if response.status == 206:
                fetchservers = ['%s://%s.appspot.com%s' % (self.mode, x, self.path) for x in self.appids]
                return RangeFetch(handler, self, response, fetchservers).fetch()
            handler.close_connection = not response.getheader('Content-Length')
            handler.send_response(response.status)
            for key, value in response.getheaders():
                if key.title() == 'Transfer-Encoding':
                    continue
                handler.send_header(key, value)
            handler.end_headers()
            bufsize = 8192
            while True:
                data = response.read(bufsize)
                if data:
                    handler.wfile.write(data)
                if not data:
                    cache_sock = getattr(response, 'cache_sock', None)
                    if cache_sock:
                        cache_sock.close()
                        del response.cache_sock
                    response.close()
                    break
                del data
        except NetWorkIOError as e:
            if e[0] in (errno.ECONNABORTED, errno.EPIPE) or 'bad write retry' in repr(e):
                return

    def fetch(self, handler, method, url, headers, body, timeout, **kwargs):
        rc4crypt = lambda s, k: RC4Cipher(k).encrypt(s) if k else s
        if isinstance(body, basestring) and body:
            if len(body) < 10 * 1024 * 1024 and 'Content-Encoding' not in headers:
                zbody = deflate(body)
                if len(zbody) < len(body):
                    body = zbody
                    headers['Content-Encoding'] = 'deflate'
            headers['Content-Length'] = str(len(body))
        # GAE donot allow set `Host` header
        if 'Host' in headers:
            del headers['Host']
        kwargs = {}
        if self.password:
            kwargs['password'] = self.password
        if self.options:
            kwargs['options'] = self.options
        if self.validate:
            kwargs['validate'] = self.validate
        metadata = 'G-Method:%s\nG-Url:%s\n%s' % (method, url, ''.join('G-%s:%s\n' % (k, v) for k, v in kwargs.items() if v))
        skip_headers = handler.skip_headers
        metadata += ''.join('%s:%s\n' % (k.title(), v) for k, v in headers.items() if k not in skip_headers)
        # prepare GAE request
        request_method = 'POST'
        fetchserver = kwargs.get('fetchserver') or '%s://%s.appspot.com%s' % (self.mode, self.appids[0], self.path)
        request_headers = {}
        if common.GAE_OBFUSCATE:
            request_method = 'GET'
            fetchserver += '/ps/%s.gif' % uuid.uuid1()
            request_headers['X-GOA-PS1'] = base64.b64encode(deflate(metadata)).strip()
            if body:
                request_headers['X-GOA-PS2'] = base64.b64encode(deflate(body)).strip()
                body = ''
            if common.GAE_PAGESPEED:
                fetchserver = re.sub(r'^(\w+://)', r'\g<1>1-ps.googleusercontent.com/h/', fetchserver)
        else:
            metadata = deflate(metadata)
            body = '%s%s%s' % (struct.pack('!h', len(metadata)), metadata, body)
            if 'rc4' in common.GAE_OPTIONS:
                request_headers['X-GOA-Options'] = 'rc4'
                body = rc4crypt(body, kwargs.get('password'))
            request_headers['Content-Length'] = str(len(body))
        # post data
        need_crlf = 0 if common.GAE_MODE == 'https' else 1
        need_validate = common.GAE_VALIDATE
        cache_key = '%s:%d' % (common.HOST_POSTFIX_MAP['.appspot.com'], 443 if common.GAE_MODE == 'https' else 80)
        response = handler.create_http_request(request_method, fetchserver, request_headers, body, timeout, crlf=need_crlf, validate=need_validate, cache_key=cache_key)
        response.app_status = response.status
        response.app_options = response.getheader('X-GOA-Options', '')
        if response.status != 200:
            return response
        data = response.read(4)
        if len(data) < 4:
            response.status = 502
            response.fp = io.BytesIO(b'connection aborted. too short leadbyte data=' + data)
            response.read = response.fp.read
            return response
        response.status, headers_length = struct.unpack('!hh', data)
        data = response.read(headers_length)
        if len(data) < headers_length:
            response.status = 502
            response.fp = io.BytesIO(b'connection aborted. too short headers data=' + data)
            response.read = response.fp.read
            return response
        if 'rc4' not in response.app_options:
            response.msg = httplib.HTTPMessage(io.BytesIO(inflate(data)))
        else:
            response.msg = httplib.HTTPMessage(io.BytesIO(inflate(rc4crypt(data, kwargs.get('password')))))
            if kwargs.get('password') and response.fp:
                response.fp = CipherFileObject(response.fp, RC4Cipher(kwargs['password']))
        return response


class PHPFetchPlugin(BaseFetchPlugin):
    """direct fetch plugin"""
    connect_timeout = 4
    def __init__(self, fetchservers, password, validate):
        BaseFetchPlugin.__init__(self)
        self.fetchservers = fetchservers
        self.password = password
        self.validate = validate

    def handle(self, handler, **kwargs):
        method = handler.command
        url = handler.path
        headers = dict((k.title(), v) for k, v in handler.headers.items())
        body = handler.body
        if body:
            if len(body) < 10 * 1024 * 1024 and 'Content-Encoding' not in headers:
                zbody = deflate(body)
                if len(zbody) < len(body):
                    body = zbody
                    headers['Content-Encoding'] = 'deflate'
            headers['Content-Length'] = str(len(body))
        skip_headers = handler.skip_headers
        if self.password:
            kwargs['password'] = self.password
        if self.validate:
            kwargs['validate'] = self.validate
        metadata = 'G-Method:%s\nG-Url:%s\n%s%s' % (method, url, ''.join('G-%s:%s\n' % (k, v) for k, v in kwargs.items() if v), ''.join('%s:%s\n' % (k, v) for k, v in headers.items() if k not in skip_headers))
        metadata = deflate(metadata)
        app_body = b''.join((struct.pack('!h', len(metadata)), metadata, body))
        app_headers = {'Content-Length': len(app_body), 'Content-Type': 'application/octet-stream'}
        fetchserver = '%s?%s' % (self.fetchservers[0], random.random())
        crlf = 0
        cache_key = '%s//:%s' % urlparse.urlsplit(fetchserver)[:2]
        response = handler.create_http_request('POST', fetchserver, app_headers, app_body, self.connect_timeout, crlf=crlf, cache_key=cache_key)
        if not response:
            raise socket.error(errno.ECONNRESET, 'urlfetch %r return None' % url)
        response.app_status = response.status
        need_decrypt = self.password and response.app_status == 200 and response.getheader('Content-Type', '') == 'image/gif' and response.fp
        if need_decrypt:
            response.fp = CipherFileObject(response.fp, XORCipher(self.password[0]))
        logging.info('%s "PHP %s %s %s" %s %s', handler.address_string(), handler.command, url, handler.protocol_version, response.status, response.getheader('Content-Length', '-'))
        handler.close_connection = bool(response.getheader('Transfer-Encoding'))
        while True:
            data = response.read(8192)
            if not data:
                break
            handler.wfile.write(data)
            del data


class HostsFilter(BaseProxyHandlerFilter):
    """hosts filter"""
    def __init__(self, iplist_map, host_map, host_postfix_map, hostport_map, hostport_postfix_map, urlre_map):
        self.iplist_map = iplist_map
        self.host_map = host_map
        self.host_postfix_map = host_postfix_map
        self.host_postfix_endswith = tuple(host_postfix_map)
        self.hostport_map = hostport_map
        self.hostport_postfix_map = hostport_postfix_map
        self.hostport_postfix_endswith = tuple(hostport_postfix_map)
        self.urlre_map = urlre_map

    def gethostbyname2(self, handler, hostname):
        hostport = '%s:%d' % (hostname, handler.port)
        hosts = ''
        if hostname in self.host_map:
            hosts = self.host_map[hostname]
        elif hostname.endswith(self.host_postfix_endswith):
            hosts = next(self.host_postfix_map[x] for x in self.host_postfix_map if hostname.endswith(x))
        if hostport in self.hostport_map:
            hosts = self.hostport_map[hostname]
        elif hostport.endswith(self.hostport_postfix_endswith):
            hosts = next(self.hostport_postfix_map[x] for x in self.hostport_postfix_map if hostport.endswith(x))
        if handler.command != 'CONNECT' and self.urlre_map:
            try:
                hosts = next(self.urlre_map[x] for x in self.urlre_map if x(handler.path))
            except StopIteration:
                pass
        if hosts not in ('', 'direct'):
            return self.iplist_map.get(hosts) or hosts.split('|')
        return None

    def filter(self, handler):
        host, port = handler.host, handler.port
        hostport = handler.path if handler.command == 'CONNECT' else '%s:%d' % (host, port)
        if host in self.host_map:
            return 'direct', {'cache_key': '%s:%d' % (self.host_map[host], port)}
        elif host.endswith(self.host_postfix_endswith):
            self.host_map[host] = next(self.host_postfix_map[x] for x in self.host_postfix_map if host.endswith(x))
            return 'direct', {'cache_key': '%s:%d' % (self.host_map[host], port)}
        elif hostport in self.hostport_map:
            return 'direct', {'cache_key': '%s:%d' % (self.hostport_map[hostport], port)}
        elif hostport.endswith(self.hostport_postfix_endswith):
            self.hostport_map[hostport] = next(self.hostport_postfix_map[x] for x in self.hostport_postfix_map if hostport.endswith(x))
            return 'direct', {'cache_key': '%s:%d' % (self.hostport_map[hostport], port)}
        if handler.command != 'CONNECT' and self.urlre_map and any(x(handler.path) for x in self.urlre_map):
            return 'direct', {}


class GAEFetchFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter(self, handler):
        """https://developers.google.com/appengine/docs/python/urlfetch/"""
        if handler.command == 'CONNECT':
            do_ssl_handshake = 440 <= handler.port <= 450 or 1024 <= handler.port <= 65535
            return 'strip', {'do_ssl_handshake': do_ssl_handshake}
        elif handler.command in ('GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'PATCH'):
            return 'gae', {}
        else:
            if 'php' in handler.handler_plugins:
                return 'php', {}
            else:
                logging.warning('"%s %s" not supported by GAE, please enable PHP mode!', handler.command, handler.host)
                return 'direct', {}


class GAEProxyHandler(MultipleConnectionMixin, SimpleProxyHandler):
    """GAE Proxy Handler"""
    handler_filters = [GAEFetchFilter()]
    handler_plugins = {'direct': DirectFetchPlugin(),
                       'mock': MockFetchPlugin(),
                       'strip': StripPlugin(),}
    hosts_filter = None

    def __init__(self, *args, **kwargs):
        SimpleProxyHandler.__init__(self, *args, **kwargs)

    def first_run(self):
        """GAEProxyHandler setup, init domain/iplist map"""
        if not common.PROXY_ENABLE:
            logging.info('resolve common.IPLIST_MAP names=%s to iplist', list(common.IPLIST_MAP))
            common.resolve_iplist()
        random.shuffle(common.GAE_APPIDS)
        self.__class__.handler_plugins['gae'] = GAEFetchPlugin(common.GAE_APPIDS, common.GAE_PASSWORD, common.GAE_PATH, common.GAE_MODE, common.GAE_CACHESOCK, common.GAE_KEEPALIVE, common.GAE_OBFUSCATE, common.GAE_PAGESPEED, common.GAE_VALIDATE, common.GAE_OPTIONS)
        try:
            self.__class__.hosts_filter = next(x for x in self.__class__.handler_filters if isinstance(x, HostsFilter))
        except StopIteration:
            pass

    def gethostbyname2(self, hostname):
        iplist = self.hosts_filter.gethostbyname2(self, hostname) if self.hosts_filter else None
        return iplist or MultipleConnectionMixin.gethostbyname2(self, hostname)


class ProxyGAEProxyHandler(ProxyConnectionMixin, GAEProxyHandler):

    def __init__(self, *args, **kwargs):
        ProxyConnectionMixin.__init__(self, common.PROXY_HOST, common.PROXY_PORT, common.PROXY_USERNAME, common.PROXY_PASSWROD)
        GAEProxyHandler.__init__(self, *args, **kwargs)

    def gethostbyname2(self, hostname):
        for postfix in ('.appspot.com', '.googleusercontent.com'):
            if hostname.endswith(postfix):
                host = common.HOST_MAP.get(hostname) or common.HOST_POSTFIX_MAP.get(postfix) or 'www.google.com'
                return common.IPLIST_MAP.get(host) or host.split('|')
        return ProxyConnectionMixin.gethostbyname2(self, hostname)


class PHPFetchFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter(self, handler):
        if handler.command == 'CONNECT':
            return 'strip', {}
        else:
            return 'php', {}


class PHPProxyHandler(MultipleConnectionMixin, SimpleProxyHandler):
    """GAE Proxy Handler"""
    handler_filters = [PHPFetchFilter()]
    handler_plugins = {'direct': DirectFetchPlugin(),
                       'mock': MockFetchPlugin(),
                       'strip': StripPlugin(),}

    def __init__(self, *args, **kwargs):
        SimpleProxyHandler.__init__(self, *args, **kwargs)


class ProxyPHPProxyHandler(ProxyConnectionMixin, PHPProxyHandler):

    def __init__(self, *args, **kwargs):
        PHPProxyHandler.__init__(self, *args, **kwargs)

    def gethostbyname2(self, hostname):
        return [hostname]


class PacUtil(object):
    """GoAgent Pac Util"""

    @staticmethod
    def update_pacfile(filename):
        listen_ip = '127.0.0.1'
        autoproxy = '%s:%s' % (listen_ip, common.LISTEN_PORT)
        blackhole = '%s:%s' % (listen_ip, common.PAC_PORT)
        default = 'PROXY %s:%s' % (common.PROXY_HOST, common.PROXY_PORT) if common.PROXY_ENABLE else 'DIRECT'
        opener = urllib2.build_opener(urllib2.ProxyHandler({'http': autoproxy, 'https': autoproxy}))
        content = ''
        need_update = True
        with open(filename, 'rb') as fp:
            content = fp.read()
        try:
            placeholder = '// AUTO-GENERATED RULES, DO NOT MODIFY!'
            content = content[:content.index(placeholder)+len(placeholder)]
            content = re.sub(r'''blackhole\s*=\s*['"]PROXY [\.\w:]+['"]''', 'blackhole = \'PROXY %s\'' % blackhole, content)
            content = re.sub(r'''autoproxy\s*=\s*['"]PROXY [\.\w:]+['"]''', 'autoproxy = \'PROXY %s\'' % autoproxy, content)
            content = re.sub(r'''defaultproxy\s*=\s*['"](DIRECT|PROXY [\.\w:]+)['"]''', 'defaultproxy = \'%s\'' % default, content)
            content = re.sub(r'''host\s*==\s*['"][\.\w:]+['"]\s*\|\|\s*isPlainHostName''', 'host == \'%s\' || isPlainHostName' % listen_ip, content)
            if content.startswith('//'):
                line = '// Proxy Auto-Config file generated by autoproxy2pac, %s\r\n' % time.strftime('%Y-%m-%d %H:%M:%S')
                content = line + '\r\n'.join(content.splitlines()[1:])
        except ValueError:
            need_update = False
        try:
            if common.PAC_ADBLOCK:
                admode = common.PAC_ADMODE
                logging.info('try download %r to update_pacfile(%r)', common.PAC_ADBLOCK, filename)
                adblock_content = opener.open(common.PAC_ADBLOCK).read()
                logging.info('%r downloaded, try convert it with adblock2pac', common.PAC_ADBLOCK)
                if 'gevent' in sys.modules and time.sleep is getattr(sys.modules['gevent'], 'sleep', None) and hasattr(gevent.get_hub(), 'threadpool'):
                    jsrule = gevent.get_hub().threadpool.apply_e(Exception, PacUtil.adblock2pac, (adblock_content, 'FindProxyForURLByAdblock', blackhole, default, admode))
                else:
                    jsrule = PacUtil.adblock2pac(adblock_content, 'FindProxyForURLByAdblock', blackhole, default, admode)
                content += '\r\n' + jsrule + '\r\n'
                logging.info('%r downloaded and parsed', common.PAC_ADBLOCK)
            else:
                content += '\r\nfunction FindProxyForURLByAdblock(url, host) {return "DIRECT";}\r\n'
        except StandardError as e:
            need_update = False
            logging.exception('update_pacfile failed: %r', e)
        try:
            logging.info('try download %r to update_pacfile(%r)', common.PAC_GFWLIST, filename)
            autoproxy_content = base64.b64decode(opener.open(common.PAC_GFWLIST).read())
            logging.info('%r downloaded, try convert it with autoproxy2pac_lite', common.PAC_GFWLIST)
            if 'gevent' in sys.modules and time.sleep is getattr(sys.modules['gevent'], 'sleep', None) and hasattr(gevent.get_hub(), 'threadpool'):
                jsrule = gevent.get_hub().threadpool.apply_e(Exception, PacUtil.autoproxy2pac_lite, (autoproxy_content, 'FindProxyForURLByAutoProxy', autoproxy, default))
            else:
                jsrule = PacUtil.autoproxy2pac_lite(autoproxy_content, 'FindProxyForURLByAutoProxy', autoproxy, default)
            content += '\r\n' + jsrule + '\r\n'
            logging.info('%r downloaded and parsed', common.PAC_GFWLIST)
        except StandardError as e:
            need_update = False
            logging.exception('update_pacfile failed: %r', e)
        if need_update:
            with open(filename, 'wb') as fp:
                fp.write(content)
            logging.info('%r successfully updated', filename)

    @staticmethod
    def autoproxy2pac(content, func_name='FindProxyForURLByAutoProxy', proxy='127.0.0.1:8087', default='DIRECT', indent=4):
        """Autoproxy to Pac, based on https://github.com/iamamac/autoproxy2pac"""
        jsLines = []
        for line in content.splitlines()[1:]:
            if line and not line.startswith("!"):
                use_proxy = True
                if line.startswith("@@"):
                    line = line[2:]
                    use_proxy = False
                return_proxy = 'PROXY %s' % proxy if use_proxy else default
                if line.startswith('/') and line.endswith('/'):
                    jsLine = 'if (/%s/i.test(url)) return "%s";' % (line[1:-1], return_proxy)
                elif line.startswith('||'):
                    domain = line[2:].lstrip('.')
                    if len(jsLines) > 0 and ('host.indexOf(".%s") >= 0' % domain in jsLines[-1] or 'host.indexOf("%s") >= 0' % domain in jsLines[-1]):
                        jsLines.pop()
                    jsLine = 'if (dnsDomainIs(host, ".%s") || host == "%s") return "%s";' % (domain, domain, return_proxy)
                elif line.startswith('|'):
                    jsLine = 'if (url.indexOf("%s") == 0) return "%s";' % (line[1:], return_proxy)
                elif '*' in line:
                    jsLine = 'if (shExpMatch(url, "*%s*")) return "%s";' % (line.strip('*'), return_proxy)
                elif '/' not in line:
                    jsLine = 'if (host.indexOf("%s") >= 0) return "%s";' % (line, return_proxy)
                else:
                    jsLine = 'if (url.indexOf("%s") >= 0) return "%s";' % (line, return_proxy)
                jsLine = ' ' * indent + jsLine
                if use_proxy:
                    jsLines.append(jsLine)
                else:
                    jsLines.insert(0, jsLine)
        function = 'function %s(url, host) {\r\n%s\r\n%sreturn "%s";\r\n}' % (func_name, '\n'.join(jsLines), ' '*indent, default)
        return function

    @staticmethod
    def autoproxy2pac_lite(content, func_name='FindProxyForURLByAutoProxy', proxy='127.0.0.1:8087', default='DIRECT', indent=4):
        """Autoproxy to Pac, based on https://github.com/iamamac/autoproxy2pac"""
        direct_domain_set = set([])
        proxy_domain_set = set([])
        for line in content.splitlines()[1:]:
            if line and not line.startswith(('!', '|!', '||!')):
                use_proxy = True
                if line.startswith("@@"):
                    line = line[2:]
                    use_proxy = False
                domain = ''
                if line.startswith('/') and line.endswith('/'):
                    line = line[1:-1]
                    if line.startswith('^https?:\\/\\/[^\\/]+') and re.match(r'^(\w|\\\-|\\\.)+$', line[18:]):
                        domain = line[18:].replace(r'\.', '.')
                    else:
                        logging.warning('unsupport gfwlist regex: %r', line)
                elif line.startswith('||'):
                    domain = line[2:].lstrip('*').rstrip('/')
                elif line.startswith('|'):
                    domain = urlparse.urlsplit(line[1:]).hostname.lstrip('*')
                elif line.startswith(('http://', 'https://')):
                    domain = urlparse.urlsplit(line).hostname.lstrip('*')
                elif re.search(r'^([\w\-\_\.]+)([\*\/]|$)', line):
                    domain = re.split(r'[\*\/]', line)[0]
                else:
                    pass
                if '*' in domain:
                    domain = domain.split('*')[-1]
                if not domain or re.match(r'^\w+$', domain):
                    logging.debug('unsupport gfwlist rule: %r', line)
                    continue
                if use_proxy:
                    proxy_domain_set.add(domain)
                else:
                    direct_domain_set.add(domain)
        proxy_domain_list = sorted(set(x.lstrip('.') for x in proxy_domain_set))
        autoproxy_host = ',\r\n'.join('%s"%s": 1' % (' '*indent, x) for x in proxy_domain_list)
        template = '''\
                    var autoproxy_host = {
                    %(autoproxy_host)s
                    };
                    function %(func_name)s(url, host) {
                        var lastPos;
                        do {
                            if (autoproxy_host.hasOwnProperty(host)) {
                                return 'PROXY %(proxy)s';
                            }
                            lastPos = host.indexOf('.') + 1;
                            host = host.slice(lastPos);
                        } while (lastPos >= 1);
                        return '%(default)s';
                    }'''
        template = re.sub(r'(?m)^\s{%d}' % min(len(re.search(r' +', x).group()) for x in template.splitlines()), '', template)
        template_args = {'autoproxy_host': autoproxy_host,
                         'func_name': func_name,
                         'proxy': proxy,
                         'default': default}
        return template % template_args

    @staticmethod
    def urlfilter2pac(content, func_name='FindProxyForURLByUrlfilter', proxy='127.0.0.1:8086', default='DIRECT', indent=4):
        """urlfilter.ini to Pac, based on https://github.com/iamamac/autoproxy2pac"""
        jsLines = []
        for line in content[content.index('[exclude]'):].splitlines()[1:]:
            if line and not line.startswith(';'):
                use_proxy = True
                if line.startswith("@@"):
                    line = line[2:]
                    use_proxy = False
                return_proxy = 'PROXY %s' % proxy if use_proxy else default
                if '*' in line:
                    jsLine = 'if (shExpMatch(url, "%s")) return "%s";' % (line, return_proxy)
                else:
                    jsLine = 'if (url == "%s") return "%s";' % (line, return_proxy)
                jsLine = ' ' * indent + jsLine
                if use_proxy:
                    jsLines.append(jsLine)
                else:
                    jsLines.insert(0, jsLine)
        function = 'function %s(url, host) {\r\n%s\r\n%sreturn "%s";\r\n}' % (func_name, '\n'.join(jsLines), ' '*indent, default)
        return function

    @staticmethod
    def adblock2pac(content, func_name='FindProxyForURLByAdblock', proxy='127.0.0.1:8086', default='DIRECT', admode=1, indent=4):
        """adblock list to Pac, based on https://github.com/iamamac/autoproxy2pac"""
        white_conditions = {'host': [], 'url.indexOf': [], 'shExpMatch': []}
        black_conditions = {'host': [], 'url.indexOf': [], 'shExpMatch': []}
        for line in content.splitlines()[1:]:
            if not line or line.startswith('!') or '##' in line or '#@#' in line:
                continue
            use_proxy = True
            use_start = False
            use_end = False
            use_domain = False
            use_postfix = []
            if '$' in line:
                posfixs = line.split('$')[-1].split(',')
                if any('domain' in x for x in posfixs):
                    continue
                if 'image' in posfixs:
                    use_postfix += ['.jpg', '.gif']
                elif 'script' in posfixs:
                    use_postfix += ['.js']
                else:
                    continue
            line = line.split('$')[0]
            if line.startswith("@@"):
                line = line[2:]
                use_proxy = False
            if '||' == line[:2]:
                line = line[2:]
                if '/' not in line:
                    use_domain = True
                else:
                    use_start = True
            elif '|' == line[0]:
                line = line[1:]
                use_start = True
            if line[-1] in ('^', '|'):
                line = line[:-1]
                if not use_postfix:
                    use_end = True
            line = line.replace('^', '*').strip('*')
            conditions = black_conditions if use_proxy else white_conditions
            if use_start and use_end:
                conditions['shExpMatch'] += ['*%s*' % line]
            elif use_start:
                if '*' in line:
                    if use_postfix:
                        conditions['shExpMatch'] += ['*%s*%s' % (line, x) for x in use_postfix]
                    else:
                        conditions['shExpMatch'] += ['*%s*' % line]
                else:
                    conditions['url.indexOf'] += [line]
            elif use_domain and use_end:
                if '*' in line:
                    conditions['shExpMatch'] += ['%s*' % line]
                else:
                    conditions['host'] += [line]
            elif use_domain:
                if line.split('/')[0].count('.') <= 1:
                    if use_postfix:
                        conditions['shExpMatch'] += ['*.%s*%s' % (line, x) for x in use_postfix]
                    else:
                        conditions['shExpMatch'] += ['*.%s*' % line]
                else:
                    if '*' in line:
                        if use_postfix:
                            conditions['shExpMatch'] += ['*%s*%s' % (line, x) for x in use_postfix]
                        else:
                            conditions['shExpMatch'] += ['*%s*' % line]
                    else:
                        if use_postfix:
                            conditions['shExpMatch'] += ['*%s*%s' % (line, x) for x in use_postfix]
                        else:
                            conditions['url.indexOf'] += ['http://%s' % line]
            else:
                if use_postfix:
                    conditions['shExpMatch'] += ['*%s*%s' % (line, x) for x in use_postfix]
                else:
                    conditions['shExpMatch'] += ['*%s*' % line]
        templates = ['''\
                    function %(func_name)s(url, host) {
                        return '%(default)s';
                    }''',
                    '''\
                    var blackhole_host = {
                    %(blackhole_host)s
                    };
                    function %(func_name)s(url, host) {
                        // untrusted ablock plus list, disable whitelist until chinalist come back.
                        if (blackhole_host.hasOwnProperty(host)) {
                            return 'PROXY %(proxy)s';
                        }
                        return '%(default)s';
                    }''',
                    '''\
                    var blackhole_host = {
                    %(blackhole_host)s
                    };
                    var blackhole_url_indexOf = [
                    %(blackhole_url_indexOf)s
                    ];
                    function %s(url, host) {
                        // untrusted ablock plus list, disable whitelist until chinalist come back.
                        if (blackhole_host.hasOwnProperty(host)) {
                            return 'PROXY %(proxy)s';
                        }
                        for (i = 0; i < blackhole_url_indexOf.length; i++) {
                            if (url.indexOf(blackhole_url_indexOf[i]) >= 0) {
                                return 'PROXY %(proxy)s';
                            }
                        }
                        return '%(default)s';
                    }''',
                    '''\
                    var blackhole_host = {
                    %(blackhole_host)s
                    };
                    var blackhole_url_indexOf = [
                    %(blackhole_url_indexOf)s
                    ];
                    var blackhole_shExpMatch = [
                    %(blackhole_shExpMatch)s
                    ];
                    function %(func_name)s(url, host) {
                        // untrusted ablock plus list, disable whitelist until chinalist come back.
                        if (blackhole_host.hasOwnProperty(host)) {
                            return 'PROXY %(proxy)s';
                        }
                        for (i = 0; i < blackhole_url_indexOf.length; i++) {
                            if (url.indexOf(blackhole_url_indexOf[i]) >= 0) {
                                return 'PROXY %(proxy)s';
                            }
                        }
                        for (i = 0; i < blackhole_shExpMatch.length; i++) {
                            if (shExpMatch(url, blackhole_shExpMatch[i])) {
                                return 'PROXY %(proxy)s';
                            }
                        }
                        return '%(default)s';
                    }''']
        template = re.sub(r'(?m)^\s{%d}' % min(len(re.search(r' +', x).group()) for x in templates[admode].splitlines()), '', templates[admode])
        template_kwargs = {'blackhole_host': ',\r\n'.join("%s'%s': 1" % (' '*indent, x) for x in sorted(black_conditions['host'])),
                           'blackhole_url_indexOf': ',\r\n'.join("%s'%s'" % (' '*indent, x) for x in sorted(black_conditions['url.indexOf'])),
                           'blackhole_shExpMatch': ',\r\n'.join("%s'%s'" % (' '*indent, x) for x in sorted(black_conditions['shExpMatch'])),
                           'func_name': func_name,
                           'proxy': proxy,
                           'default': default}
        return template % template_kwargs


class PacFileFilter(BaseProxyHandlerFilter):
    """pac file filter"""

    def filter(self, handler):
        is_local_client = handler.client_address[0] in ('127.0.0.1', '::1')
        pacfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), common.PAC_FILE)
        urlparts = urlparse.urlsplit(handler.path)
        if handler.command == 'GET' and urlparts.path.lstrip('/') == common.PAC_FILE:
            if urlparts.query == 'flush':
                if is_local_client:
                    thread.start_new_thread(PacUtil.update_pacfile, (pacfile,))
                else:
                    return 'mock', {'status': 403, 'headers': {'Content-Type': 'text/plain'}, 'body': 'client address %r not allowed' % handler.client_address[0]}
            if time.time() - os.path.getmtime(pacfile) > common.PAC_EXPIRED:
                # check system uptime > 30 minutes
                uptime = get_uptime()
                if uptime and uptime > 1800:
                    thread.start_new_thread(lambda: os.utime(pacfile, (time.time(), time.time())) or PacUtil.update_pacfile(pacfile), tuple())
            with open(pacfile, 'rb') as fp:
                content = fp.read()
                if not is_local_client:
                    serving_addr = urlparts.hostname or ProxyUtil.get_listen_ip()
                    content = content.replace('127.0.0.1', serving_addr)
                headers = {'Content-Type': 'text/plain'}
                if 'gzip' in handler.headers.get('Accept-Encoding', ''):
                    headers['Content-Encoding'] = 'gzip'
                    compressobj = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
                    dataio = io.BytesIO()
                    dataio.write('\x1f\x8b\x08\x00\x00\x00\x00\x00\x02\xff')
                    dataio.write(compressobj.compress(content))
                    dataio.write(compressobj.flush())
                    dataio.write(struct.pack('<LL', zlib.crc32(content) & 0xFFFFFFFFL, len(content) & 0xFFFFFFFFL))
                    content = dataio.getvalue()
                return 'mock', {'status': 200, 'headers': headers, 'body': content}


class PACProxyHandler(SimpleProxyHandler):
    """pac proxy handler"""
    handler_filters = [PacFileFilter(), StaticFileFilter(), BlackholeFilter()]


class Common(object):
    """Global Config Object"""

    ENV_CONFIG_PREFIX = 'GOAGENT_'

    def __init__(self):
        """load config from proxy.ini"""
        ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>\S+)\s+(?P<vi>[=])\s+(?P<value>.*)$')
        self.CONFIG = ConfigParser.ConfigParser()
        self.CONFIG_FILENAME = os.path.splitext(os.path.abspath(__file__))[0]+'.ini'
        self.CONFIG_USER_FILENAME = re.sub(r'\.ini$', '.user.ini', self.CONFIG_FILENAME)
        self.CONFIG.read([self.CONFIG_FILENAME, self.CONFIG_USER_FILENAME])

        for key, value in os.environ.items():
            m = re.match(r'^%s([A-Z]+)_([A-Z\_\-]+)$' % self.ENV_CONFIG_PREFIX, key)
            if m:
                self.CONFIG.set(m.group(1).lower(), m.group(2).lower(), value)

        self.LISTEN_IP = self.CONFIG.get('listen', 'ip')
        self.LISTEN_PORT = self.CONFIG.getint('listen', 'port')
        self.LISTEN_USERNAME = self.CONFIG.get('listen', 'username') if self.CONFIG.has_option('listen', 'username') else ''
        self.LISTEN_PASSWORD = self.CONFIG.get('listen', 'password') if self.CONFIG.has_option('listen', 'password') else ''
        self.LISTEN_VISIBLE = self.CONFIG.getint('listen', 'visible')
        self.LISTEN_DEBUGINFO = self.CONFIG.getint('listen', 'debuginfo')

        self.GAE_ENABLE = self.CONFIG.getint('gae', 'enable')
        self.GAE_APPIDS = re.findall(r'[\w\-\.]+', self.CONFIG.get('gae', 'appid').replace('.appspot.com', ''))
        self.GAE_PASSWORD = self.CONFIG.get('gae', 'password').strip()
        self.GAE_PATH = self.CONFIG.get('gae', 'path')
        self.GAE_MODE = self.CONFIG.get('gae', 'mode')
        self.GAE_PROFILE = self.CONFIG.get('gae', 'profile').strip()
        self.GAE_WINDOW = self.CONFIG.getint('gae', 'window')
        self.GAE_KEEPALIVE = self.CONFIG.getint('gae', 'keepalive')
        self.GAE_CACHESOCK = self.CONFIG.getint('gae', 'cachesock')
        self.GAE_OBFUSCATE = self.CONFIG.getint('gae', 'obfuscate')
        self.GAE_VALIDATE = self.CONFIG.getint('gae', 'validate')
        self.GAE_TRANSPORT = self.CONFIG.getint('gae', 'transport') if self.CONFIG.has_option('gae', 'transport') else 0
        self.GAE_OPTIONS = self.CONFIG.get('gae', 'options')
        self.GAE_REGIONS = set(x.upper() for x in self.CONFIG.get('gae', 'regions').split('|') if x.strip())
        self.GAE_SSLVERSION = self.CONFIG.get('gae', 'sslversion')
        self.GAE_PAGESPEED = self.CONFIG.getint('gae', 'pagespeed') if self.CONFIG.has_option('gae', 'pagespeed') else 0

        if self.GAE_PROFILE == 'auto':
            try:
                socket.create_connection(('2001:4860:4860::8888', 53), timeout=1).close()
                logging.info('Use profile ipv6')
                self.GAE_PROFILE = 'ipv6'
            except socket.error as e:
                logging.info('Fail try profile ipv6 %r, fallback ipv4', e)
                self.GAE_PROFILE = 'ipv4'

        if 'USERDNSDOMAIN' in os.environ and re.match(r'^\w+\.\w+$', os.environ['USERDNSDOMAIN']):
            self.CONFIG.set('profile/%s' % self.GAE_PROFILE, '.' + os.environ['USERDNSDOMAIN'], '')

        urlrewrite_map = collections.OrderedDict()
        host_map = collections.OrderedDict()
        host_postfix_map = collections.OrderedDict()
        hostport_map = collections.OrderedDict()
        hostport_postfix_map = collections.OrderedDict()
        urlre_map = collections.OrderedDict()
        withgae_sites = []
        crlf_sites = []
        nocrlf_sites = []
        forcehttps_sites = []
        noforcehttps_sites = []
        fakehttps_sites = []
        nofakehttps_sites = []
        dns_servers = []

        for site, rule in self.CONFIG.items('profile/%s' % self.GAE_PROFILE):
            rules = [x.strip() for x in re.split(r'[,\|]', rule) if x.strip()]
            if site == 'dns':
                dns_servers = rules
                continue
            if rule.startswith(('file://', 'http://', 'https://')) or '$1' in rule:
                urlrewrite_map[site] = rule
                continue
            for name, sites in [('withgae', withgae_sites),
                                ('crlf', crlf_sites),
                                ('nocrlf', nocrlf_sites),
                                ('forcehttps', forcehttps_sites),
                                ('noforcehttps', noforcehttps_sites),
                                ('fakehttps', fakehttps_sites),
                                ('nofakehttps', nofakehttps_sites)]:
                if name in rules:
                    sites.append(site)
                    rules.remove(name)
            hostname = rules and rules[0]
            if not hostname:
                continue
            if ':' in site and '\\' not in site:
                if site.startswith('.'):
                    hostport_postfix_map[site] = hostname
                else:
                    hostport_map[site] = hostname
            elif '\\' in site:
                urlre_map[re.compile(site).match] = hostname
            else:
                if site.startswith('.'):
                    host_postfix_map[site] = hostname
                else:
                    host_map[site] = hostname

        self.HTTP_DNS = dns_servers
        self.WITHGAE_SITES = set(withgae_sites)
        self.CRLF_SITES = tuple(crlf_sites)
        self.NOCRLF_SITES = set(nocrlf_sites)
        self.FORCEHTTPS_SITES = tuple(forcehttps_sites)
        self.NOFORCEHTTPS_SITES = set(noforcehttps_sites)
        self.FAKEHTTPS_SITES = tuple(fakehttps_sites)
        self.NOFAKEHTTPS_SITES = set(nofakehttps_sites)
        self.URLREWRITE_MAP = urlrewrite_map
        self.HOSTPORT_MAP = hostport_map
        self.HOSTPORT_POSTFIX_MAP = hostport_postfix_map
        self.URLRE_MAP = urlre_map
        self.HOST_MAP = host_map
        self.HOST_POSTFIX_MAP = host_postfix_map

        self.IPLIST_MAP = collections.OrderedDict((k, v.split('|') if v else []) for k, v in self.CONFIG.items('iplist'))
        self.IPLIST_MAP.update((k, [k]) for k, v in self.HOST_MAP.items() if k == v)

        self.PAC_ENABLE = self.CONFIG.getint('pac', 'enable')
        self.PAC_IP = self.CONFIG.get('pac', 'ip')
        self.PAC_PORT = self.CONFIG.getint('pac', 'port')
        self.PAC_FILE = self.CONFIG.get('pac', 'file').lstrip('/')
        self.PAC_GFWLIST = self.CONFIG.get('pac', 'gfwlist')
        self.PAC_ADBLOCK = self.CONFIG.get('pac', 'adblock')
        self.PAC_ADMODE = self.CONFIG.getint('pac', 'admode')
        self.PAC_EXPIRED = self.CONFIG.getint('pac', 'expired')

        self.PHP_ENABLE = self.CONFIG.getint('php', 'enable')
        self.PHP_LISTEN = self.CONFIG.get('php', 'listen')
        self.PHP_PASSWORD = self.CONFIG.get('php', 'password') if self.CONFIG.has_option('php', 'password') else ''
        self.PHP_CRLF = self.CONFIG.getint('php', 'crlf') if self.CONFIG.has_option('php', 'crlf') else 1
        self.PHP_VALIDATE = self.CONFIG.getint('php', 'validate') if self.CONFIG.has_option('php', 'validate') else 0
        self.PHP_FETCHSERVERS = self.CONFIG.get('php', 'fetchserver').split('|')

        self.PROXY_ENABLE = self.CONFIG.getint('proxy', 'enable')
        self.PROXY_AUTODETECT = self.CONFIG.getint('proxy', 'autodetect') if self.CONFIG.has_option('proxy', 'autodetect') else 0
        self.PROXY_HOST = self.CONFIG.get('proxy', 'host')
        self.PROXY_PORT = self.CONFIG.getint('proxy', 'port')
        self.PROXY_USERNAME = self.CONFIG.get('proxy', 'username')
        self.PROXY_PASSWROD = self.CONFIG.get('proxy', 'password')

        if not self.PROXY_ENABLE and self.PROXY_AUTODETECT:
            system_proxy = ProxyUtil.get_system_proxy()
            if system_proxy and self.LISTEN_IP not in system_proxy:
                _, username, password, address = ProxyUtil.parse_proxy(system_proxy)
                proxyhost, _, proxyport = address.rpartition(':')
                self.PROXY_ENABLE = 1
                self.PROXY_USERNAME = username
                self.PROXY_PASSWROD = password
                self.PROXY_HOST = proxyhost
                self.PROXY_PORT = int(proxyport)
        if self.PROXY_ENABLE:
            self.GAE_MODE = 'https'

        self.AUTORANGE_HOSTS = self.CONFIG.get('autorange', 'hosts').split('|')
        self.AUTORANGE_ENDSWITH = tuple(self.CONFIG.get('autorange', 'endswith').split('|'))
        self.AUTORANGE_NOENDSWITH = tuple(self.CONFIG.get('autorange', 'noendswith').split('|'))
        self.AUTORANGE_MAXSIZE = self.CONFIG.getint('autorange', 'maxsize')
        self.AUTORANGE_WAITSIZE = self.CONFIG.getint('autorange', 'waitsize')
        self.AUTORANGE_BUFSIZE = self.CONFIG.getint('autorange', 'bufsize')
        self.AUTORANGE_THREADS = self.CONFIG.getint('autorange', 'threads')

        self.FETCHMAX_LOCAL = self.CONFIG.getint('fetchmax', 'local') if self.CONFIG.get('fetchmax', 'local') else 3
        self.FETCHMAX_SERVER = self.CONFIG.get('fetchmax', 'server')

        self.DNS_ENABLE = self.CONFIG.getint('dns', 'enable')
        self.DNS_LISTEN = self.CONFIG.get('dns', 'listen')
        self.DNS_SERVERS = self.HTTP_DNS or self.CONFIG.get('dns', 'servers').split('|')
        self.DNS_BLACKLIST = set(self.CONFIG.get('dns', 'blacklist').split('|'))
        self.DNS_TCPOVER = tuple(self.CONFIG.get('dns', 'tcpover').split('|')) if self.CONFIG.get('dns', 'tcpover').strip() else tuple()

        self.USERAGENT_ENABLE = self.CONFIG.getint('useragent', 'enable')
        self.USERAGENT_STRING = self.CONFIG.get('useragent', 'string')

        self.LOVE_ENABLE = self.CONFIG.getint('love', 'enable')
        self.LOVE_TIP = self.CONFIG.get('love', 'tip').encode('utf8').decode('unicode-escape').split('|')

    def extend_iplist(self, iplist_name, hosts):
        logging.info('extend_iplist start for hosts=%s', hosts)
        new_iplist = []
        def do_remote_resolve(host, dnsserver, queue):
            assert isinstance(dnsserver, basestring)
            for dnslib_resolve in (dnslib_resolve_over_udp, dnslib_resolve_over_tcp):
                try:
                    time.sleep(random.random())
                    iplist = dnslib_record2iplist(dnslib_resolve(host, [dnsserver], timeout=4, blacklist=self.DNS_BLACKLIST))
                    queue.put((host, dnsserver, iplist))
                except (socket.error, OSError) as e:
                    logging.info('%s remote host=%r failed: %s', str(dnslib_resolve).split()[1], host, e)
                    time.sleep(1)
        result_queue = Queue.Queue()
        for host in hosts:
            for dnsserver in self.DNS_SERVERS:
                logging.debug('remote resolve host=%r from dnsserver=%r', host, dnsserver)
                thread.start_new_thread(do_remote_resolve, (host, dnsserver, result_queue))
        for _ in xrange(len(self.DNS_SERVERS) * len(hosts) * 2):
            try:
                host, dnsserver, iplist = result_queue.get(timeout=16)
                logging.debug('%r remote host=%r return %s', dnsserver, host, iplist)
                if host.endswith('.google.com'):
                    iplist = [x for x in iplist if is_google_ip(x)]
                new_iplist += iplist
            except Queue.Empty:
                break
        logging.info('extend_iplist finished, added %s', len(set(self.IPLIST_MAP[iplist_name])-set(new_iplist)))
        self.IPLIST_MAP[iplist_name] = list(set(self.IPLIST_MAP[iplist_name] + new_iplist))

    def resolve_iplist(self):
        # https://support.google.com/websearch/answer/186669?hl=zh-Hans
        def do_local_resolve(host, queue):
            assert isinstance(host, basestring)
            for _ in xrange(3):
                try:
                    queue.put((host, socket.gethostbyname_ex(host)[-1]))
                except (socket.error, OSError) as e:
                    logging.warning('socket.gethostbyname_ex host=%r failed: %s', host, e)
                    time.sleep(0.1)
        google_blacklist = ['216.239.32.20'] + list(self.DNS_BLACKLIST)
        for name, need_resolve_hosts in list(self.IPLIST_MAP.items()):
            if all(re.match(r'\d+\.\d+\.\d+\.\d+', x) or ':' in x for x in need_resolve_hosts):
                continue
            need_resolve_remote = [x for x in need_resolve_hosts if ':' not in x and not re.match(r'\d+\.\d+\.\d+\.\d+', x)]
            resolved_iplist = [x for x in need_resolve_hosts if x not in need_resolve_remote]
            result_queue = Queue.Queue()
            for host in need_resolve_remote:
                logging.debug('local resolve host=%r', host)
                thread.start_new_thread(do_local_resolve, (host, result_queue))
            for _ in xrange(len(need_resolve_remote)):
                try:
                    host, iplist = result_queue.get(timeout=8)
                    if host.endswith('.google.com'):
                        iplist = [x for x in iplist if is_google_ip(x)]
                    resolved_iplist += iplist
                except Queue.Empty:
                    break
            if name == 'google_hk' and need_resolve_remote:
                for delay in (1, 60, 150, 240, 300, 450, 600, 900):
                    spawn_later(delay, self.extend_iplist, name, need_resolve_remote)
            if name.startswith('google_') and name not in ('google_cn', 'google_hk') and resolved_iplist:
                iplist_prefix = re.split(r'[\.:]', resolved_iplist[0])[0]
                resolved_iplist = list(set(x for x in resolved_iplist if x.startswith(iplist_prefix)))
            else:
                resolved_iplist = list(set(resolved_iplist))
            if name.startswith('google_'):
                resolved_iplist = list(set(resolved_iplist) - set(google_blacklist))
            if len(resolved_iplist) == 0 and name in ('google_hk', 'google_cn'):
                logging.error('resolve %s host return empty! please retry!', name)
                sys.exit(-1)
            logging.info('resolve name=%s host to iplist=%r', name, resolved_iplist)
            common.IPLIST_MAP[name] = resolved_iplist

    def info(self):
        info = ''
        info += '------------------------------------------------------\n'
        info += 'GoAgent Version    : %s (python/%s gevent/%s pyopenssl/%s)\n' % (__version__, sys.version[:5], gevent.__version__, OpenSSL.__version__)
        info += 'Uvent Version      : %s (pyuv/%s libuv/%s)\n' % (__import__('uvent').__version__, __import__('pyuv').__version__, __import__('pyuv').LIBUV_VERSION) if all(x in sys.modules for x in ('pyuv', 'uvent')) else ''
        info += 'Listen Address     : %s:%d\n' % (self.LISTEN_IP, self.LISTEN_PORT)
        info += 'Local Proxy        : %s:%s\n' % (self.PROXY_HOST, self.PROXY_PORT) if self.PROXY_ENABLE else ''
        info += 'Debug INFO         : %s\n' % self.LISTEN_DEBUGINFO if self.LISTEN_DEBUGINFO else ''
        info += 'GAE Mode           : %s\n' % self.GAE_MODE
        info += 'GAE Profile        : %s\n' % self.GAE_PROFILE if self.GAE_PROFILE else ''
        info += 'GAE APPID          : %s\n' % '|'.join(self.GAE_APPIDS)
        info += 'GAE Validate       : %s\n' % self.GAE_VALIDATE if self.GAE_VALIDATE else ''
        info += 'GAE Obfuscate      : %s\n' % self.GAE_OBFUSCATE if self.GAE_OBFUSCATE else ''
        if common.PAC_ENABLE:
            info += 'Pac Server         : http://%s:%d/%s\n' % (self.PAC_IP if self.PAC_IP and self.PAC_IP != '0.0.0.0' else ProxyUtil.get_listen_ip(), self.PAC_PORT, self.PAC_FILE)
            info += 'Pac File           : file://%s\n' % os.path.abspath(self.PAC_FILE)
        if common.PHP_ENABLE:
            info += 'PHP Listen         : %s\n' % common.PHP_LISTEN
            info += 'PHP FetchServers   : %s\n' % common.PHP_FETCHSERVERS
        if common.DNS_ENABLE:
            info += 'DNS Listen         : %s\n' % common.DNS_LISTEN
            info += 'DNS Servers        : %s\n' % '|'.join(common.DNS_SERVERS)
        info += '------------------------------------------------------\n'
        return info

common = Common()


def pre_start():
    if sys.platform == 'cygwin':
        logging.info('cygwin is not officially supported, please continue at your own risk :)')
        #sys.exit(-1)
    elif os.name == 'posix':
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (8192, -1))
        except ValueError:
            pass
    elif os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(u'GoAgent v%s' % __version__)
        if not common.LISTEN_VISIBLE:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        else:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
        if common.LOVE_ENABLE and random.randint(1, 100) <= 5:
            title = ctypes.create_unicode_buffer(1024)
            ctypes.windll.kernel32.GetConsoleTitleW(ctypes.byref(title), len(title)-1)
            ctypes.windll.kernel32.SetConsoleTitleW('%s %s' % (title.value, random.choice(common.LOVE_TIP)))
        blacklist = {'360safe': False,
                     'QQProtect': False, }
        softwares = [k for k, v in blacklist.items() if v]
        if softwares:
            tasklist = '\n'.join(x.name for x in get_process_list()).lower()
            softwares = [x for x in softwares if x.lower() in tasklist]
            if softwares:
                title = u'GoAgent 建议'
                error = u'某些安全软件(如 %s)可能和本软件存在冲突，造成 CPU 占用过高。\n如有此现象建议暂时退出此安全软件来继续运行GoAgent' % ','.join(softwares)
                ctypes.windll.user32.MessageBoxW(None, error, title, 0)
                #sys.exit(0)
    if os.path.isfile('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'rb') as fp:
            m = re.search(r'(?im)(BogoMIPS|cpu MHz)\s+:\s+([\d\.]+)', fp.read())
            if m and float(m.group(2)) < 1000:
                logging.warning("*NOTE*, if you want to fix high cpu usage, please decrease [gae]window")
    if gevent.__version__ < '1.0':
        logging.warning("*NOTE*, please upgrade to gevent 1.1 as possible")
    if GAEProxyHandler.max_window != common.GAE_WINDOW:
        GAEProxyHandler.max_window = common.GAE_WINDOW
    if common.GAE_CACHESOCK:
        GAEProxyHandler.tcp_connection_cachesock = True
        GAEProxyHandler.ssl_connection_cachesock = True
    if common.GAE_KEEPALIVE:
        GAEProxyHandler.tcp_connection_cachesock = True
        GAEProxyHandler.tcp_connection_keepalive = True
        GAEProxyHandler.ssl_connection_cachesock = True
        GAEProxyHandler.ssl_connection_keepalive = True
    if common.GAE_PAGESPEED and not common.GAE_OBFUSCATE:
        logging.critical("*NOTE*, [gae]pagespeed=1 requires [gae]obfuscate=1")
        sys.exit(-1)
    if common.GAE_SSLVERSION and not sysconfig.get_platform().startswith('macosx-'):
        GAEProxyHandler.ssl_version = getattr(ssl, 'PROTOCOL_%s' % common.GAE_SSLVERSION)
        GAEProxyHandler.openssl_context = SSLConnection.context_builder(common.GAE_SSLVERSION)
    if common.GAE_ENABLE and common.GAE_APPIDS[0] == 'goagent':
        logging.warning('please edit %s to add your appid to [gae] !', common.CONFIG_FILENAME)
    if common.GAE_ENABLE and common.GAE_MODE == 'http' and common.GAE_PASSWORD == '':
        logging.critical('to enable http mode, you should set %r [gae]password = <your_pass> and [gae]options = rc4', common.CONFIG_FILENAME)
        sys.exit(-1)
    if common.GAE_TRANSPORT:
        GAEProxyHandler.disable_transport_ssl = False
    if common.PAC_ENABLE:
        pac_ip = ProxyUtil.get_listen_ip() if common.PAC_IP in ('', '::', '0.0.0.0') else common.PAC_IP
        url = 'http://%s:%d/%s' % (pac_ip, common.PAC_PORT, common.PAC_FILE)
        spawn_later(600, urllib2.build_opener(urllib2.ProxyHandler({})).open, url)
    if not common.DNS_ENABLE:
        if not common.HTTP_DNS:
            common.HTTP_DNS = common.DNS_SERVERS[:]
        for dnsservers_ref in (common.HTTP_DNS, common.DNS_SERVERS):
            any(dnsservers_ref.insert(0, x) for x in [y for y in get_dnsserver_list() if y not in dnsservers_ref])
        GAEProxyHandler.dns_servers = common.HTTP_DNS
        GAEProxyHandler.dns_blacklist = common.DNS_BLACKLIST
    else:
        GAEProxyHandler.dns_servers = common.HTTP_DNS or common.DNS_SERVERS
        GAEProxyHandler.dns_blacklist = common.DNS_BLACKLIST
    RangeFetch.threads = common.AUTORANGE_THREADS
    RangeFetch.maxsize = common.AUTORANGE_MAXSIZE
    RangeFetch.bufsize = common.AUTORANGE_BUFSIZE
    RangeFetch.waitsize = common.AUTORANGE_WAITSIZE
    if True:
        GAEProxyHandler.handler_filters.insert(0, AutoRangeFilter(common.AUTORANGE_HOSTS, common.AUTORANGE_ENDSWITH, common.AUTORANGE_NOENDSWITH, common.AUTORANGE_MAXSIZE))
    if common.GAE_REGIONS:
        GAEProxyHandler.handler_filters.insert(0, DirectRegionFilter(common.GAE_REGIONS))
    if common.HOST_MAP or common.HOST_POSTFIX_MAP or common.HOSTPORT_MAP or common.HOSTPORT_POSTFIX_MAP or common.URLRE_MAP:
        GAEProxyHandler.handler_filters.insert(0, HostsFilter(common.IPLIST_MAP, common.HOST_MAP, common.HOST_POSTFIX_MAP, common.HOSTPORT_MAP, common.HOSTPORT_POSTFIX_MAP, common.URLRE_MAP))
    if common.CRLF_SITES:
        GAEProxyHandler.handler_filters.insert(0, CRLFSitesFilter(common.CRLF_SITES, common.NOCRLF_SITES))
    if common.URLREWRITE_MAP:
        GAEProxyHandler.handler_filters.insert(0, URLRewriteFilter(common.URLREWRITE_MAP))
    if common.FAKEHTTPS_SITES:
        GAEProxyHandler.handler_filters.insert(0, FakeHttpsFilter(common.FAKEHTTPS_SITES, common.NOFAKEHTTPS_SITES))
    if common.FORCEHTTPS_SITES:
        GAEProxyHandler.handler_filters.insert(0, ForceHttpsFilter(common.FORCEHTTPS_SITES, common.NOFORCEHTTPS_SITES))
    if common.WITHGAE_SITES:
        GAEProxyHandler.handler_filters.insert(0, JumpLastFilter(common.WITHGAE_SITES))
    if common.USERAGENT_ENABLE:
        GAEProxyHandler.handler_filters.insert(0, UserAgentFilter(common.USERAGENT_STRING))
    if common.LISTEN_USERNAME:
        GAEProxyHandler.handler_filters.insert(0, AuthFilter(common.LISTEN_USERNAME, common.LISTEN_PASSWORD))


def main():
    global __file__
    __file__ = os.path.abspath(__file__)
    if os.path.islink(__file__):
        __file__ = getattr(os, 'readlink', lambda x: x)(__file__)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(level=logging.DEBUG if common.LISTEN_DEBUGINFO else logging.INFO, format='%(levelname)s - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    pre_start()
    sys.stderr.write(common.info())

    if common.PAC_ENABLE:
        thread.start_new_thread(LocalProxyServer((common.PAC_IP, common.PAC_PORT), PACProxyHandler).serve_forever, tuple())

    if common.DNS_ENABLE:
        try:
            from dnsproxy import DNSServer
            host, port = common.DNS_LISTEN.split(':')
            dns_server = DNSServer((host, int(port)), dns_servers=common.DNS_SERVERS, dns_blacklist=common.DNS_BLACKLIST, dns_tcpover=common.DNS_TCPOVER)
            thread.start_new_thread(dns_server.serve_forever, tuple())
        except ImportError:
            logging.exception('GoAgent DNSServer requires dnslib and gevent 1.0')
            sys.exit(-1)

    if common.GAE_ENABLE or common.PHP_ENABLE:
        CertUtil.check_ca()

    php_server = None
    if common.PHP_ENABLE:
        host, port = common.PHP_LISTEN.split(':')
        HandlerClass = PHPProxyHandler if not common.PROXY_ENABLE else ProxyPHPProxyHandler
        HandlerClass.handler_plugins['php'] = PHPFetchPlugin(common.PHP_FETCHSERVERS, common.PHP_PASSWORD, common.PHP_VALIDATE)
        php_server = LocalProxyServer((host, int(port)), HandlerClass)
        thread.start_new_thread(php_server.serve_forever, tuple())

    if common.GAE_ENABLE:
        HandlerClass = GAEProxyHandler if not common.PROXY_ENABLE else ProxyGAEProxyHandler
        if common.PHP_ENABLE:
            HandlerClass.handler_plugins['php'] = php_server.RequestHandlerClass.handler_plugins['php']
        gae_server = LocalProxyServer((common.LISTEN_IP, common.LISTEN_PORT), HandlerClass)
        gae_server.serve_forever()
    else:
        gevent.sleep(sys.maxint)

if __name__ == '__main__':
    main()
