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

__version__ = '3.1.19'

import sys
import os
import glob

reload(sys).setdefaultencoding('UTF-8')
sys.dont_write_bytecode = True
sys.path += glob.glob('%s/*.egg' % os.path.dirname(os.path.abspath(__file__)))

try:
    import gevent
    import gevent.socket
    import gevent.server
    import gevent.queue
    import gevent.monkey
    gevent.monkey.patch_all(subprocess=True)
except ImportError:
    gevent = None
except TypeError:
    gevent.monkey.patch_all()
    sys.stderr.write('\033[31m  Warning: Please update gevent to the latest 1.0 version!\033[0m\n')

import errno
import time
import struct
import collections
import binascii
import zlib
import itertools
import re
import io
import fnmatch
import traceback
import random
import base64
import string
import hashlib
import uuid
import threading
import thread
import socket
import ssl
import select
import Queue
import SocketServer
import ConfigParser
import BaseHTTPServer
import httplib
import urllib
import urllib2
import urlparse
try:
    import dnslib
except ImportError:
    dnslib = None
try:
    import OpenSSL
except ImportError:
    OpenSSL = None
try:
    import pygeoip
except ImportError:
    pygeoip = None


HAS_PYPY = hasattr(sys, 'pypy_version_info')
NetWorkIOError = (socket.error, ssl.SSLError, OSError) if not OpenSSL else (socket.error, ssl.SSLError, OpenSSL.SSL.Error, OSError)


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


class LRUCache(object):
    """http://pypi.python.org/pypi/lru/"""

    def __init__(self, max_items=100):
        self.cache = {}
        self.key_order = []
        self.max_items = max_items

    def __setitem__(self, key, value):
        self.cache[key] = value
        self._mark(key)

    def __getitem__(self, key):
        value = self.cache[key]
        self._mark(key)
        return value

    def __contains__(self, key):
        return key in self.cache

    def _mark(self, key):
        if key in self.key_order:
            self.key_order.remove(key)
        self.key_order.insert(0, key)
        if len(self.key_order) > self.max_items:
            index = self.max_items // 2
            delitem = self.cache.__delitem__
            key_order = self.key_order
            any(delitem(key_order[x]) for x in xrange(index, len(key_order)))
            self.key_order = self.key_order[:index]

    def clear(self):
        self.cache = {}
        self.key_order = []


class CertUtil(object):
    """CertUtil module, based on mitmproxy"""

    ca_vendor = 'GoAgent'
    ca_keyfile = 'CA.crt'
    ca_certdir = 'certs'
    ca_lock = threading.Lock()

    @staticmethod
    def create_ca():
        key = OpenSSL.crypto.PKey()
        key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)
        ca = OpenSSL.crypto.X509()
        ca.set_serial_number(0)
        ca.set_version(2)
        subj = ca.get_subject()
        subj.countryName = 'CN'
        subj.stateOrProvinceName = 'Internet'
        subj.localityName = 'Cernet'
        subj.organizationName = CertUtil.ca_vendor
        subj.organizationalUnitName = '%s Root' % CertUtil.ca_vendor
        subj.commonName = '%s CA' % CertUtil.ca_vendor
        ca.gmtime_adj_notBefore(0)
        ca.gmtime_adj_notAfter(24 * 60 * 60 * 3652)
        ca.set_issuer(ca.get_subject())
        ca.set_pubkey(key)
        ca.add_extensions([
            OpenSSL.crypto.X509Extension(b'basicConstraints', True, b'CA:TRUE'),
            # OpenSSL.crypto.X509Extension(b'nsCertType', True, b'sslCA'),
            OpenSSL.crypto.X509Extension(b'extendedKeyUsage', True, b'serverAuth,clientAuth,emailProtection,timeStamping,msCodeInd,msCodeCom,msCTLSign,msSGC,msEFS,nsSGC'),
            OpenSSL.crypto.X509Extension(b'keyUsage', False, b'keyCertSign, cRLSign'),
            OpenSSL.crypto.X509Extension(b'subjectKeyIdentifier', False, b'hash', subject=ca), ])
        ca.sign(key, 'sha1')
        return key, ca

    @staticmethod
    def dump_ca():
        key, ca = CertUtil.create_ca()
        with open(CertUtil.ca_keyfile, 'wb') as fp:
            fp.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, ca))
            fp.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key))

    @staticmethod
    def _get_cert(commonname, sans=()):
        with open(CertUtil.ca_keyfile, 'rb') as fp:
            content = fp.read()
            key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, content)
            ca = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, content)

        pkey = OpenSSL.crypto.PKey()
        pkey.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

        req = OpenSSL.crypto.X509Req()
        subj = req.get_subject()
        subj.countryName = 'CN'
        subj.stateOrProvinceName = 'Internet'
        subj.localityName = 'Cernet'
        subj.organizationalUnitName = '%s Branch' % CertUtil.ca_vendor
        if commonname[0] == '.':
            subj.commonName = '*' + commonname
            subj.organizationName = '*' + commonname
            sans = ['*'+commonname] + [x for x in sans if x != '*'+commonname]
        else:
            subj.commonName = commonname
            subj.organizationName = commonname
            sans = [commonname] + [x for x in sans if x != commonname]
        #req.add_extensions([OpenSSL.crypto.X509Extension(b'subjectAltName', True, ', '.join('DNS: %s' % x for x in sans)).encode()])
        req.set_pubkey(pkey)
        req.sign(pkey, 'sha1')

        cert = OpenSSL.crypto.X509()
        cert.set_version(2)
        try:
            cert.set_serial_number(int(hashlib.md5(commonname.encode('utf-8')).hexdigest(), 16))
        except OpenSSL.SSL.Error:
            cert.set_serial_number(int(time.time()*1000))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(60 * 60 * 24 * 3652)
        cert.set_issuer(ca.get_subject())
        cert.set_subject(req.get_subject())
        cert.set_pubkey(req.get_pubkey())
        if commonname[0] == '.':
            sans = ['*'+commonname] + [s for s in sans if s != '*'+commonname]
        else:
            sans = [commonname] + [s for s in sans if s != commonname]
        #cert.add_extensions([OpenSSL.crypto.X509Extension(b'subjectAltName', True, ', '.join('DNS: %s' % x for x in sans))])
        cert.sign(key, 'sha1')

        certfile = os.path.join(CertUtil.ca_certdir, commonname + '.crt')
        with open(certfile, 'wb') as fp:
            fp.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
            fp.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pkey))
        return certfile

    @staticmethod
    def get_cert(commonname, sans=()):
        if commonname.count('.') >= 2 and [len(x) for x in reversed(commonname.split('.'))] > [2, 4]:
            commonname = '.'+commonname.partition('.')[-1]
        certfile = os.path.join(CertUtil.ca_certdir, commonname + '.crt')
        if os.path.exists(certfile):
            return certfile
        elif OpenSSL is None:
            return CertUtil.ca_keyfile
        else:
            with CertUtil.ca_lock:
                if os.path.exists(certfile):
                    return certfile
                return CertUtil._get_cert(commonname, sans)

    @staticmethod
    def import_ca(certfile):
        commonname = os.path.splitext(os.path.basename(certfile))[0]
        sha1digest = 'AB:70:2C:DF:18:EB:E8:B4:38:C5:28:69:CD:4A:5D:EF:48:B4:0E:33'
        if OpenSSL:
            try:
                with open(certfile, 'rb') as fp:
                    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, fp.read())
                    commonname = next(v.decode() for k, v in x509.get_subject().get_components() if k == b'O')
                    sha1digest = x509.digest('sha1')
            except StandardError as e:
                logging.error('load_certificate(certfile=%r) failed:%s', certfile, e)
        if sys.platform.startswith('win'):
            import ctypes
            with open(certfile, 'rb') as fp:
                certdata = fp.read()
                if certdata.startswith(b'-----'):
                    begin = b'-----BEGIN CERTIFICATE-----'
                    end = b'-----END CERTIFICATE-----'
                    certdata = base64.b64decode(b''.join(certdata[certdata.find(begin)+len(begin):certdata.find(end)].strip().splitlines()))
                crypt32 = ctypes.WinDLL(b'crypt32.dll'.decode())
                store_handle = crypt32.CertOpenStore(10, 0, 0, 0x4000 | 0x20000, b'ROOT'.decode())
                if not store_handle:
                    return -1
                X509_ASN_ENCODING = 0x00000001
                CERT_FIND_HASH = 0x10000
                class CRYPT_HASH_BLOB(ctypes.Structure):
                    _fields_ = [('cbData', ctypes.c_ulong), ('pbData', ctypes.c_char_p)]
                crypt_hash = CRYPT_HASH_BLOB(20, binascii.a2b_hex(sha1digest.replace(':', '')))
                crypt_handle = crypt32.CertFindCertificateInStore(store_handle, X509_ASN_ENCODING, 0, CERT_FIND_HASH, ctypes.byref(crypt_hash), None)
                if crypt_handle:
                    crypt32.CertFreeCertificateContext(crypt_handle)
                    return 0
                ret = crypt32.CertAddEncodedCertificateToStore(store_handle, 0x1, certdata, len(certdata), 4, None)
                crypt32.CertCloseStore(store_handle, 0)
                del crypt32
                return 0 if ret else -1
        elif sys.platform == 'darwin':
            return os.system(('security find-certificate -a -c "%s" | grep "%s" >/dev/null || security add-trusted-cert -d -r trustRoot -k "/Library/Keychains/System.keychain" "%s"' % (commonname, commonname, certfile.decode('utf-8'))).encode('utf-8'))
        elif sys.platform.startswith('linux'):
            import platform
            platform_distname = platform.dist()[0]
            if platform_distname == 'Ubuntu':
                pemfile = "/etc/ssl/certs/%s.pem" % commonname
                new_certfile = "/usr/local/share/ca-certificates/%s.crt" % commonname
                if not os.path.exists(pemfile):
                    return os.system('cp "%s" "%s" && update-ca-certificates' % (certfile, new_certfile))
            elif any(os.path.isfile('%s/certutil' % x) for x in os.environ['PATH'].split(os.pathsep)):
                return os.system('certutil -L -d sql:$HOME/.pki/nssdb | grep "%s" || certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n "%s" -i "%s"' % (commonname, commonname, certfile))
            else:
                logging.warning('please install *libnss3-tools* package to import GoAgent root ca')
        return 0

    @staticmethod
    def check_ca():
        #Check CA exists
        capath = os.path.join(os.path.dirname(os.path.abspath(__file__)), CertUtil.ca_keyfile)
        certdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), CertUtil.ca_certdir)
        if not os.path.exists(capath):
            if not OpenSSL:
                logging.critical('CA.key is not exist and OpenSSL is disabled, ABORT!')
                sys.exit(-1)
            if os.path.exists(certdir):
                if os.path.isdir(certdir):
                    any(os.remove(x) for x in glob.glob(certdir+'/*.crt')+glob.glob(certdir+'/.*.crt'))
                else:
                    os.remove(certdir)
                    os.mkdir(certdir)
            CertUtil.dump_ca()
        if glob.glob('%s/*.key' % CertUtil.ca_certdir):
            for filename in glob.glob('%s/*.key' % CertUtil.ca_certdir):
                try:
                    os.remove(filename)
                    os.remove(os.path.splitext(filename)[0]+'.crt')
                except EnvironmentError:
                    pass
        #Check CA imported
        if CertUtil.import_ca(capath) != 0:
            logging.warning('install root certificate failed, Please run as administrator/root/sudo')
        #Check Certs Dir
        if not os.path.exists(certdir):
            os.makedirs(certdir)


class DetectMobileBrowser:
    """detect mobile function from http://detectmobilebrowsers.com"""
    regex_match_a = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M).search
    regex_match_b = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M).search

    @staticmethod
    def detect(user_agent):
        return DetectMobileBrowser.regex_match_a(user_agent) or DetectMobileBrowser.regex_match_b(user_agent)


class SSLConnection(object):
    """OpenSSL Connection Wapper"""

    def __init__(self, context, sock):
        self._context = context
        self._sock = sock
        self._connection = OpenSSL.SSL.Connection(context, sock)
        self._makefile_refs = 0

    def __getattr__(self, attr):
        if attr not in ('_context', '_sock', '_connection', '_makefile_refs'):
            return getattr(self._connection, attr)

    def __wait_sock_io(self, io_func, *args, **kwargs):
        timeout = self._sock.gettimeout() or 0.1
        fd = self._sock.fileno()
        while True:
            try:
                return io_func(*args, **kwargs)
            except (OpenSSL.SSL.WantReadError, OpenSSL.SSL.WantX509LookupError):
                sys.exc_clear()
                _, _, errors = select.select([fd], [], [fd], timeout)
                if errors:
                    break
            except OpenSSL.SSL.WantWriteError:
                sys.exc_clear()
                _, _, errors = select.select([], [fd], [fd], timeout)
                if errors:
                    break

    def accept(self):
        sock, addr = self._sock.accept()
        client = OpenSSL.SSL.Connection(sock._context, sock)
        return client, addr

    def do_handshake(self):
        return self.__wait_sock_io(self._connection.do_handshake)

    def connect(self, *args, **kwargs):
        return self.__wait_sock_io(self._connection.connect, *args, **kwargs)

    def send(self, data, flags=0):
        try:
            return self.__wait_sock_io(self._connection.send, data, flags)
        except OpenSSL.SSL.SysCallError as e:
            if e[0] == -1 and not data:
                # errors when writing empty strings are expected and can be ignored
                return 0
            raise

    def recv(self, bufsiz, flags=0):
        pending = self._connection.pending()
        if pending:
            return self._connection.recv(min(pending, bufsiz))
        try:
            return self.__wait_sock_io(self._connection.recv, bufsiz, flags)
        except OpenSSL.SSL.ZeroReturnError:
            return ''

    def read(self, bufsiz, flags=0):
        return self.recv(bufsiz, flags)

    def write(self, buf, flags=0):
        return self.sendall(buf, flags)

    def close(self):
        if self._makefile_refs < 1:
            self._connection = None
            if self._sock:
                socket.socket.close(self._sock)
        else:
            self._makefile_refs -= 1

    def makefile(self, mode='r', bufsize=-1):
        self._makefile_refs += 1
        return socket._fileobject(self, mode, bufsize, close=True)

    @staticmethod
    def context_builder(ssl_version='SSLv23', ca_certs=None, cipher_suites=('ALL', '!aNULL', '!eNULL')):
        protocol_version = getattr(OpenSSL.SSL, '%s_METHOD' % ssl_version)
        ssl_context = OpenSSL.SSL.Context(protocol_version)
        if ca_certs:
            ssl_context.load_verify_locations(os.path.abspath(ca_certs))
            ssl_context.set_verify(OpenSSL.SSL.VERIFY_PEER, lambda c, x, e, d, ok: ok)
        else:
            ssl_context.set_verify(OpenSSL.SSL.VERIFY_NONE, lambda c, x, e, d, ok: ok)
        ssl_context.set_cipher_list(':'.join(cipher_suites))
        if hasattr(OpenSSL.SSL, 'SESS_CACHE_BOTH'):
            ssl_context.set_session_cache_mode(OpenSSL.SSL.SESS_CACHE_BOTH)
        return ssl_context


class ProxyUtil(object):
    """ProxyUtil module, based on urllib2"""

    @staticmethod
    def parse_proxy(proxy):
        return urllib2._parse_proxy(proxy)

    @staticmethod
    def get_system_proxy():
        proxies = urllib2.getproxies()
        return proxies.get('https') or proxies.get('http') or {}

    @staticmethod
    def get_listen_ip():
        listen_ip = '127.0.0.1'
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(('8.8.8.8', 53))
            listen_ip = sock.getsockname()[0]
        except socket.error:
            pass
        finally:
            if sock:
                sock.close()
        return listen_ip


def inflate(data):
    return zlib.decompress(data, -zlib.MAX_WBITS)


def deflate(data):
    return zlib.compress(data)[2:-4]


def parse_hostport(host, default_port=80):
    m = re.match(r'(.+)[#](\d+)$', host)
    if m:
        return m.group(1).strip('[]'), int(m.group(2))
    else:
        return host.strip('[]'), default_port


def dnslib_resolve_over_udp(query, dnsservers, timeout, **kwargs):
    """
    http://gfwrev.blogspot.com/2009/11/gfwdns.html
    http://zh.wikipedia.org/wiki/%E5%9F%9F%E5%90%8D%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%BC%93%E5%AD%98%E6%B1%A1%E6%9F%93
    http://support.microsoft.com/kb/241352
    """
    if not isinstance(query, (basestring, dnslib.DNSRecord)):
        raise TypeError('query argument requires string/DNSRecord')
    blacklist = kwargs.get('blacklist', ())
    turstservers = kwargs.get('turstservers', ())
    dns_v4_servers = [x for x in dnsservers if ':' not in x]
    dns_v6_servers = [x for x in dnsservers if ':' in x]
    sock_v4 = sock_v6 = None
    socks = []
    if dns_v4_servers:
        sock_v4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socks.append(sock_v4)
    if dns_v6_servers:
        sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        socks.append(sock_v6)
    timeout_at = time.time() + timeout
    try:
        for _ in xrange(4):
            try:
                for dnsserver in dns_v4_servers:
                    if isinstance(query, basestring):
                        query = dnslib.DNSRecord(q=dnslib.DNSQuestion(query))
                    query_data = query.pack()
                    sock_v4.sendto(query_data, parse_hostport(dnsserver, 53))
                for dnsserver in dns_v6_servers:
                    if isinstance(query, basestring):
                        query = dnslib.DNSRecord(q=dnslib.DNSQuestion(query, qtype=dnslib.QTYPE.AAAA))
                    query_data = query.pack()
                    sock_v6.sendto(query_data, parse_hostport(dnsserver, 53))
                while time.time() < timeout_at:
                    ins, _, _ = select.select(socks, [], [], 0.1)
                    for sock in ins:
                        reply_data, reply_address = sock.recvfrom(512)
                        reply_server = reply_address[0]
                        record = dnslib.DNSRecord.parse(reply_data)
                        iplist = [str(x.rdata) for x in record.rr if x.rtype in (1, 28, 255)]
                        if any(x in blacklist for x in iplist):
                            logging.warning('query=%r dnsservers=%r record bad iplist=%r', query, dnsservers, iplist)
                        elif record.header.rcode and not iplist and reply_server in turstservers:
                            logging.info('query=%r trust reply_server=%r record rcode=%s', query, reply_server, record.header.rcode)
                            return record
                        elif iplist:
                            logging.debug('query=%r reply_server=%r record iplist=%s', query, reply_server, iplist)
                            return record
                        else:
                            logging.debug('query=%r reply_server=%r record null iplist=%s', query, reply_server, iplist)
                            continue
            except socket.error as e:
                logging.warning('handle dns query=%s socket: %r', query, e)
        raise socket.gaierror(11004, 'getaddrinfo %r from %r failed' % (query, dnsservers))
    finally:
        for sock in socks:
            sock.close()


def dnslib_resolve_over_tcp(query, dnsservers, timeout, **kwargs):
    """dns query over tcp"""
    if not isinstance(query, (basestring, dnslib.DNSRecord)):
        raise TypeError('query argument requires string/DNSRecord')
    blacklist = kwargs.get('blacklist', ())
    def do_resolve(query, dnsserver, timeout, queobj):
        if isinstance(query, basestring):
            qtype = dnslib.QTYPE.AAAA if ':' in dnsserver else dnslib.QTYPE.A
            query = dnslib.DNSRecord(q=dnslib.DNSQuestion(query, qtype=qtype))
        query_data = query.pack()
        sock_family = socket.AF_INET6 if ':' in dnsserver else socket.AF_INET
        sock = socket.socket(sock_family)
        rfile = None
        try:
            sock.settimeout(timeout or None)
            sock.connect(parse_hostport(dnsserver, 53))
            sock.send(struct.pack('>h', len(query_data)) + query_data)
            rfile = sock.makefile('r', 1024)
            reply_data_length = rfile.read(2)
            if len(reply_data_length) < 2:
                raise socket.gaierror(11004, 'getaddrinfo %r from %r failed' % (query, dnsserver))
            reply_data = rfile.read(struct.unpack('>h', reply_data_length)[0])
            record = dnslib.DNSRecord.parse(reply_data)
            iplist = [str(x.rdata) for x in record.rr if x.rtype in (1, 28, 255)]
            if any(x in blacklist for x in iplist):
                logging.debug('query=%r dnsserver=%r record bad iplist=%r', query, dnsserver, iplist)
                raise socket.gaierror(11004, 'getaddrinfo %r from %r failed' % (query, dnsserver))
            else:
                logging.debug('query=%r dnsserver=%r record iplist=%s', query, dnsserver, iplist)
                queobj.put(record)
        except socket.error as e:
            logging.debug('query=%r dnsserver=%r failed %r', query, dnsserver, e)
            queobj.put(e)
        finally:
            if rfile:
                rfile.close()
            sock.close()
    queobj = Queue.Queue()
    for dnsserver in dnsservers:
        thread.start_new_thread(do_resolve, (query, dnsserver, timeout, queobj))
    for i in range(len(dnsservers)):
        try:
            result = queobj.get(timeout)
        except Queue.Empty:
            raise socket.gaierror(11004, 'getaddrinfo %r from %r failed' % (query, dnsservers))
        if result and not isinstance(result, Exception):
            return result
        elif i == len(dnsservers) - 1:
            logging.warning('dnslib_resolve_over_tcp %r with %s return %r', query, dnsservers, result)
    raise socket.gaierror(11004, 'getaddrinfo %r from %r failed' % (query, dnsservers))


def dnslib_record2iplist(record):
    """convert dnslib.DNSRecord to iplist"""
    assert isinstance(record, dnslib.DNSRecord)
    iplist = [x for x in (str(r.rdata) for r in record.rr) if re.match(r'^\d+\.\d+\.\d+\.\d+$', x) or ':' in x]
    return iplist


def get_dnsserver_list():
    if os.name == 'nt':
        import ctypes
        import ctypes.wintypes
        DNS_CONFIG_DNS_SERVER_LIST = 6
        buf = ctypes.create_string_buffer(2048)
        ctypes.windll.dnsapi.DnsQueryConfig(DNS_CONFIG_DNS_SERVER_LIST, 0, None, None, ctypes.byref(buf), ctypes.byref(ctypes.wintypes.DWORD(len(buf))))
        ipcount = struct.unpack('I', buf[0:4])[0]
        iplist = [socket.inet_ntoa(buf[i:i+4]) for i in xrange(4, ipcount*4+4, 4)]
        return iplist
    elif os.path.isfile('/etc/resolv.conf'):
        with open('/etc/resolv.conf', 'rb') as fp:
            return re.findall(r'(?m)^nameserver\s+(\S+)', fp.read())
    else:
        logging.warning("get_dnsserver_list failed: unsupport platform '%s-%s'", sys.platform, os.name)
        return []


def spawn_later(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        time.sleep(seconds)
        return target(*args, **kwargs)
    return thread.start_new_thread(wrap, args, kwargs)


def spawn_period(seconds, target, *args, **kwargs):
    def wrap(*args, **kwargs):
        try:
            time.sleep(seconds)
            target(*args, **kwargs)
        except StandardError as e:
            logging.warning('%r(%s, %s) error: %r', target, args, kwargs, e)
    return thread.start_new_thread(wrap, args, kwargs)


def is_clienthello(data):
    if len(data) < 20:
        return False
    if data.startswith('\x16\x03'):
        # TLSv12/TLSv11/TLSv1/SSLv3
        length, = struct.unpack('>h', data[3:5])
        return len(data) == 5 + length
    elif data[0] == '\x80' and data[2:4] == '\x01\x03':
        # SSLv23
        return len(data) == 2 + ord(data[1])
    else:
        return False


def is_google_ip(ipaddr):
    return ipaddr.startswith(('173.194.', '207.126.', '209.85.', '216.239.', '64.18.', '64.233.', '66.102.', '66.249.', '72.14.', '74.125.'))


def extract_sni_name(packet):
    if packet.startswith('\x16\x03'):
        stream = io.BytesIO(packet)
        stream.read(0x2b)
        session_id_length = ord(stream.read(1))
        stream.read(session_id_length)
        cipher_suites_length, = struct.unpack('>h', stream.read(2))
        stream.read(cipher_suites_length+2)
        extensions_length, = struct.unpack('>h', stream.read(2))
        # extensions = {}
        while True:
            data = stream.read(2)
            if not data:
                break
            etype, = struct.unpack('>h', data)
            elen, = struct.unpack('>h', stream.read(2))
            edata = stream.read(elen)
            if etype == 0:
                server_name = edata[5:]
                return server_name


class URLFetch(object):
    """URLFetch for gae/php fetchservers"""
    skip_headers = frozenset(['Vary', 'Via', 'X-Forwarded-For', 'Proxy-Authorization', 'Proxy-Connection', 'Upgrade', 'X-Chrome-Variations', 'Connection', 'Cache-Control'])

    def __init__(self, fetchserver, create_http_request):
        assert isinstance(fetchserver, basestring) and callable(create_http_request)
        self.fetchserver = fetchserver
        self.create_http_request = create_http_request

    def fetch(self, method, url, headers, body, timeout, **kwargs):
        if '.appspot.com/' in self.fetchserver:
            response = self.__gae_fetch(method, url, headers, body, timeout, **kwargs)
            response.app_header_parsed = True
        else:
            response = self.__php_fetch(method, url, headers, body, timeout, **kwargs)
            response.app_header_parsed = False
        return response

    def __gae_fetch(self, method, url, headers, body, timeout, **kwargs):
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
        metadata = 'G-Method:%s\nG-Url:%s\n%s' % (method, url, ''.join('G-%s:%s\n' % (k, v) for k, v in kwargs.items() if v))
        skip_headers = self.skip_headers
        metadata += ''.join('%s:%s\n' % (k.title(), v) for k, v in headers.items() if k not in skip_headers)
        # prepare GAE request
        request_fetchserver = self.fetchserver
        request_method = 'POST'
        request_headers = {}
        if common.GAE_OBFUSCATE:
            request_method = 'GET'
            request_fetchserver += '/ps/%s.gif' % uuid.uuid1()
            request_headers['X-GOA-PS1'] = base64.b64encode(deflate(metadata)).strip()
            if body:
                request_headers['X-GOA-PS2'] = base64.b64encode(deflate(body)).strip()
                body = ''
            if common.GAE_PAGESPEED:
                request_fetchserver = re.sub(r'^(\w+://)', r'\g<1>1-ps.googleusercontent.com/h/', request_fetchserver)
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
        response = self.create_http_request(request_method, request_fetchserver, request_headers, body, timeout, crlf=need_crlf, validate=need_validate, cache_key=cache_key)
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

    def __php_fetch(self, method, url, headers, body, timeout, **kwargs):
        if body:
            if len(body) < 10 * 1024 * 1024 and 'Content-Encoding' not in headers:
                zbody = deflate(body)
                if len(zbody) < len(body):
                    body = zbody
                    headers['Content-Encoding'] = 'deflate'
            headers['Content-Length'] = str(len(body))
        skip_headers = self.skip_headers
        metadata = 'G-Method:%s\nG-Url:%s\n%s%s' % (method, url, ''.join('G-%s:%s\n' % (k, v) for k, v in kwargs.items() if v), ''.join('%s:%s\n' % (k, v) for k, v in headers.items() if k not in skip_headers))
        metadata = deflate(metadata)
        app_body = b''.join((struct.pack('!h', len(metadata)), metadata, body))
        app_headers = {'Content-Length': len(app_body), 'Content-Type': 'application/octet-stream'}
        fetchserver = '%s?%s' % (self.fetchserver, random.random())
        crlf = 0
        cache_key = '%s//:%s' % urlparse.urlsplit(fetchserver)[:2]
        response = self.create_http_request('POST', fetchserver, app_headers, app_body, timeout, crlf=crlf, cache_key=cache_key)
        if not response:
            raise socket.error(errno.ECONNRESET, 'urlfetch %r return None' % url)
        if response.status >= 400:
            return response
        response.app_status = response.status
        need_decrypt = kwargs.get('password') and response.app_status == 200 and response.getheader('Content-Type', '') == 'image/gif' and response.fp
        if need_decrypt:
            response.fp = CipherFileObject(response.fp, XORCipher(kwargs['password'][0]))
        return response


class BaseProxyHandlerFilter(object):
    """base proxy handler filter"""
    def filter(self, handler):
        raise NotImplementedError


class SimpleProxyHandlerFilter(BaseProxyHandlerFilter):
    """simple proxy handler filter"""
    def filter(self, handler):
        if handler.command == 'CONNECT':
            return [handler.FORWARD, handler.host, handler.port, handler.connect_timeout]
        else:
            return [handler.DIRECT, {}]


class AuthFilter(BaseProxyHandlerFilter):
    """authorization filter"""
    auth_info = "Proxy authentication required"""
    white_list = set(['127.0.0.1'])

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_auth_header(self, auth_header):
        method, _, auth_data = auth_header.partition(' ')
        if method == 'Basic':
            username, _, password = base64.b64decode(auth_data).partition(':')
            if username == self.username and password == self.password:
                return True
        return False

    def filter(self, handler):
        if self.white_list and handler.client_address[0] in self.white_list:
            return None
        auth_header = handler.headers.get('Proxy-Authorization') or getattr(handler, 'auth_header', None)
        if auth_header and self.check_auth_header(auth_header):
            handler.auth_header = auth_header
        else:
            headers = {'Access-Control-Allow-Origin': '*',
                       'Proxy-Authenticate': 'Basic realm="%s"' % self.auth_info,
                       'Content-Length': '0',
                       'Connection': 'keep-alive'}
            return [handler.MOCK, 407, headers, '']


class SimpleProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """SimpleProxyHandler for GoAgent 3.x"""

    protocol_version = 'HTTP/1.1'
    ssl_version = ssl.PROTOCOL_SSLv23
    disable_transport_ssl = True
    scheme = 'http'
    skip_headers = frozenset(['Vary', 'Via', 'X-Forwarded-For', 'Proxy-Authorization', 'Proxy-Connection', 'Upgrade', 'X-Chrome-Variations', 'Connection', 'Cache-Control'])
    bufsize = 256 * 1024
    max_timeout = 4
    connect_timeout = 2
    first_run_lock = threading.Lock()
    handler_filters = [SimpleProxyHandlerFilter()]
    sticky_filter = None

    def finish(self):
        """make python2 BaseHTTPRequestHandler happy"""
        try:
            BaseHTTPServer.BaseHTTPRequestHandler.finish(self)
        except NetWorkIOError as e:
            if e[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise

    def address_string(self):
        return '%s:%s' % self.client_address[:2]

    def send_response(self, code, message=None):
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''
        if self.request_version != 'HTTP/0.9':
            self.wfile.write('%s %d %s\r\n' % (self.protocol_version, code, message))

    def send_header(self, keyword, value):
        """Send a MIME header."""
        base_send_header = BaseHTTPServer.BaseHTTPRequestHandler.send_header
        keyword = keyword.title()
        if keyword == 'Set-Cookie':
            for cookie in re.split(r', (?=[^ =]+(?:=|$))', value):
                base_send_header(self, keyword, cookie)
        elif keyword == 'Content-Disposition' and '"' not in value:
            value = re.sub(r'filename=([^"\']+)', 'filename="\\1"', value)
            base_send_header(self, keyword, value)
        else:
            base_send_header(self, keyword, value)

    def setup(self):
        if isinstance(self.__class__.first_run, collections.Callable):
            try:
                with self.__class__.first_run_lock:
                    if isinstance(self.__class__.first_run, collections.Callable):
                        self.first_run()
                        self.__class__.first_run = None
            except StandardError as e:
                logging.exception('%s.first_run() return %r', self.__class__, e)
        self.__class__.setup = BaseHTTPServer.BaseHTTPRequestHandler.setup
        self.__class__.do_CONNECT = self.__class__.do_METHOD
        self.__class__.do_GET = self.__class__.do_METHOD
        self.__class__.do_PATCH = self.__class__.do_METHOD
        self.__class__.do_PUT = self.__class__.do_METHOD
        self.__class__.do_POST = self.__class__.do_METHOD
        self.__class__.do_HEAD = self.__class__.do_METHOD
        self.__class__.do_DELETE = self.__class__.do_METHOD
        self.__class__.do_OPTIONS = self.__class__.do_METHOD
        self.setup()

    def handle_one_request(self):
        if not self.disable_transport_ssl and self.scheme == 'http':
            leadbyte = self.connection.recv(1, socket.MSG_PEEK)
            if leadbyte in ('\x80', '\x16'):
                server_name = ''
                if leadbyte == '\x16':
                    for _ in xrange(2):
                        leaddata = self.connection.recv(1024, socket.MSG_PEEK)
                        if is_clienthello(leaddata):
                            try:
                                server_name = extract_sni_name(leaddata)
                            finally:
                                break
                try:
                    certfile = CertUtil.get_cert(server_name or 'www.google.com')
                    ssl_sock = ssl.wrap_socket(self.connection, ssl_version=self.ssl_version, keyfile=certfile, certfile=certfile, server_side=True)
                except StandardError as e:
                    if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET):
                        logging.exception('ssl.wrap_socket(self.connection=%r) failed: %s', self.connection, e)
                    return
                self.connection = ssl_sock
                self.rfile = self.connection.makefile('rb', self.bufsize)
                self.wfile = self.connection.makefile('wb', 0)
                self.scheme = 'https'
        return BaseHTTPServer.BaseHTTPRequestHandler.handle_one_request(self)

    def first_run(self):
        pass

    def gethostbyname2(self, hostname):
        return socket.gethostbyname_ex(hostname)[-1]

    def create_tcp_connection(self, hostname, port, timeout, **kwargs):
        return socket.create_connection((hostname, port), timeout)

    def create_ssl_connection(self, hostname, port, timeout, **kwargs):
        sock = self.create_tcp_connection(hostname, port, timeout, **kwargs)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=self.ssl_version)
        return ssl_sock

    def create_http_request(self, method, url, headers, body, timeout, **kwargs):
        scheme, netloc, path, query, _ = urlparse.urlsplit(url)
        if netloc.rfind(':') <= netloc.rfind(']'):
            # no port number
            host = netloc
            port = 443 if scheme == 'https' else 80
        else:
            host, _, port = netloc.rpartition(':')
            port = int(port)
        if query:
            path += '?' + query
        if 'Host' not in headers:
            headers['Host'] = host
        if body and 'Content-Length' not in headers:
            headers['Content-Length'] = str(len(body))
        ConnectionType = httplib.HTTPSConnection if scheme == 'https' else httplib.HTTPConnection
        connection = ConnectionType(netloc, timeout=timeout)
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        return response

    def create_http_request_withserver(self, fetchserver, method, url, headers, body, timeout, **kwargs):
        return URLFetch(fetchserver, self.create_http_request).fetch(method, url, headers, body, timeout, **kwargs)

    def handle_urlfetch_error(self, fetchserver, response):
        pass

    def handle_urlfetch_response_close(self, fetchserver, response):
        pass

    def parse_header(self):
        if self.command == 'CONNECT':
            netloc = self.path
        elif self.path[0] == '/':
            netloc = self.headers.get('Host', 'localhost')
            self.path = '%s://%s%s' % (self.scheme, netloc, self.path)
        else:
            netloc = urlparse.urlsplit(self.path).netloc
        m = re.match(r'^(.+):(\d+)$', netloc)
        if m:
            self.host = m.group(1).strip('[]')
            self.port = int(m.group(2))
        else:
            self.host = netloc
            self.port = 443 if self.scheme == 'https' else 80

    def forward_socket(self, local, remote, timeout):
        try:
            tick = 1
            bufsize = self.bufsize
            timecount = timeout
            while 1:
                timecount -= tick
                if timecount <= 0:
                    break
                (ins, _, errors) = select.select([local, remote], [], [local, remote], tick)
                if errors:
                    break
                for sock in ins:
                    data = sock.recv(bufsize)
                    if not data:
                        break
                    if sock is remote:
                        local.sendall(data)
                        timecount = timeout
                    else:
                        remote.sendall(data)
                        timecount = timeout
        except socket.timeout:
            pass
        except NetWorkIOError as e:
            if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.ENOTCONN, errno.EPIPE):
                raise
            if e.args[0] in (errno.EBADF,):
                return
        finally:
            for sock in (remote, local):
                try:
                    sock.close()
                except StandardError:
                    pass

    def MOCK(self, status, headers, content):
        """mock response"""
        logging.info('%s "MOCK %s %s %s" %d %d', self.address_string(), self.command, self.path, self.protocol_version, status, len(content))
        headers = dict((k.title(), v) for k, v in headers.items())
        if 'Transfer-Encoding' in headers:
            del headers['Transfer-Encoding']
        if 'Content-Length' not in headers:
            headers['Content-Length'] = len(content)
        if 'Connection' not in headers:
            headers['Connection'] = 'close'
        self.send_response(status)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content)

    def STRIP(self, do_ssl_handshake=True, sticky_filter=None):
        """strip connect"""
        certfile = CertUtil.get_cert(self.host)
        logging.info('%s "STRIP %s %s:%d %s" - -', self.address_string(), self.command, self.host, self.port, self.protocol_version)
        self.send_response(200)
        self.end_headers()
        if do_ssl_handshake:
            try:
                # ssl_sock = ssl.wrap_socket(self.connection, ssl_version=self.ssl_version, keyfile=certfile, certfile=certfile, server_side=True)
                # bugfix for youtube-dl
                ssl_sock = ssl.wrap_socket(self.connection, keyfile=certfile, certfile=certfile, server_side=True)
            except StandardError as e:
                if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET):
                    logging.exception('ssl.wrap_socket(self.connection=%r) failed: %s', self.connection, e)
                return
            self.connection = ssl_sock
            self.rfile = self.connection.makefile('rb', self.bufsize)
            self.wfile = self.connection.makefile('wb', 0)
            self.scheme = 'https'
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                return
        except NetWorkIOError as e:
            if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise
        self.sticky_filter = sticky_filter
        try:
            self.do_METHOD()
        except NetWorkIOError as e:
            if e.args[0] not in (errno.ECONNABORTED, errno.ETIMEDOUT, errno.EPIPE):
                raise

    def FORWARD(self, hostname, port, timeout, kwargs={}):
        """forward socket"""
        do_ssl_handshake = kwargs.pop('do_ssl_handshake', False)
        local = self.connection
        remote = None
        self.send_response(200)
        self.end_headers()
        self.close_connection = 1
        data = local.recv(1024)
        if not data:
            local.close()
            return
        data_is_clienthello = is_clienthello(data)
        if data_is_clienthello:
            kwargs['client_hello'] = data
        max_retry = kwargs.get('max_retry', 3)
        for i in xrange(max_retry):
            try:
                if do_ssl_handshake:
                    remote = self.create_ssl_connection(hostname, port, timeout, **kwargs)
                else:
                    remote = self.create_tcp_connection(hostname, port, timeout, **kwargs)
                if not data_is_clienthello and remote and not isinstance(remote, Exception):
                    remote.sendall(data)
                break
            except StandardError as e:
                logging.exception('%s "FWD %s %s:%d %s" %r', self.address_string(), self.command, hostname, port, self.protocol_version, e)
                if hasattr(remote, 'close'):
                    remote.close()
                if i == max_retry - 1:
                    raise
        logging.info('%s "FWD %s %s:%d %s" - -', self.address_string(), self.command, hostname, port, self.protocol_version)
        if hasattr(remote, 'fileno'):
            # reset timeout default to avoid long http upload failure, but it will delay timeout retry :(
            remote.settimeout(None)
        del kwargs
        data = data_is_clienthello and getattr(remote, 'data', None)
        if data:
            del remote.data
            local.sendall(data)
        self.forward_socket(local, remote, self.max_timeout)

    def DIRECT(self, kwargs):
        method = self.command
        if 'url' in kwargs:
            url = kwargs.pop('url')
        elif self.path.lower().startswith(('http://', 'https://', 'ftp://')):
            url = self.path
        else:
            url = 'http://%s%s' % (self.headers['Host'], self.path)
        headers = dict((k.title(), v) for k, v in self.headers.items())
        body = self.body
        response = None
        try:
            response = self.create_http_request(method, url, headers, body, timeout=self.connect_timeout, **kwargs)
            logging.info('%s "DIRECT %s %s %s" %s %s', self.address_string(), self.command, url, self.protocol_version, response.status, response.getheader('Content-Length', '-'))
            response_headers = dict((k.title(), v) for k, v in response.getheaders())
            self.send_response(response.status)
            for key, value in response.getheaders():
                self.send_header(key, value)
            self.end_headers()
            if self.command == 'HEAD' or response.status in (204, 304):
                response.close()
                return
            need_chunked = 'Transfer-Encoding' in response_headers
            while True:
                data = response.read(8192)
                if not data:
                    if need_chunked:
                        self.wfile.write('0\r\n\r\n')
                    break
                if need_chunked:
                    self.wfile.write('%x\r\n' % len(data))
                self.wfile.write(data)
                if need_chunked:
                    self.wfile.write('\r\n')
                del data
        except (ssl.SSLError, socket.timeout, socket.error):
            if response:
                if response.fp and response.fp._sock:
                    response.fp._sock.close()
                response.close()
        finally:
            if response:
                response.close()

    def URLFETCH(self, fetchservers, max_retry=2, kwargs={}):
        """urlfetch from fetchserver"""
        method = self.command
        if self.path[0] == '/':
            url = '%s://%s%s' % (self.scheme, self.headers['Host'], self.path)
        elif self.path.lower().startswith(('http://', 'https://', 'ftp://')):
            url = self.path
        else:
            raise ValueError('URLFETCH %r is not a valid url' % self.path)
        headers = dict((k.title(), v) for k, v in self.headers.items())
        body = self.body
        response = None
        errors = []
        fetchserver = fetchservers[0]
        for i in xrange(max_retry):
            try:
                response = self.create_http_request_withserver(fetchserver, method, url, headers, body, timeout=60, **kwargs)
                if response.app_status < 400:
                    break
                else:
                    self.handle_urlfetch_error(fetchserver, response)
                if i < max_retry - 1:
                    if len(fetchservers) > 1:
                        fetchserver = random.choice(fetchservers[1:])
                    logging.info('URLFETCH return %d, trying fetchserver=%r', response.app_status, fetchserver)
                    response.close()
            except StandardError as e:
                errors.append(e)
                logging.info('URLFETCH "%s %s" fetchserver=%r %r, retry...', method, url, fetchserver, e)
        if len(errors) == max_retry:
            if response and response.app_status >= 500:
                status = response.app_status
                headers = dict(response.getheaders())
                content = response.read()
                response.close()
            else:
                status = 502
                headers = {'Content-Type': 'text/html'}
                content = message_html('502 URLFetch failed', 'Local URLFetch %r failed' % url, '<br>'.join(repr(x) for x in errors))
            return self.MOCK(status, headers, content)
        logging.info('%s "URL %s %s %s" %s %s', self.address_string(), method, url, self.protocol_version, response.status, response.getheader('Content-Length', '-'))
        try:
            if response.status == 206:
                return RangeFetch(self, response, fetchservers, **kwargs).fetch()
            if response.app_header_parsed:
                self.close_connection = not response.getheader('Content-Length')
                self.send_response(response.status)
                for key, value in response.getheaders():
                    if key.title() == 'Transfer-Encoding':
                        continue
                    self.send_header(key, value)
                self.end_headers()
            bufsize = 8192
            while True:
                data = response.read(bufsize)
                if data:
                    self.wfile.write(data)
                if not data:
                    self.handle_urlfetch_response_close(fetchserver, response)
                    response.close()
                    break
                del data
        except NetWorkIOError as e:
            if e[0] in (errno.ECONNABORTED, errno.EPIPE) or 'bad write retry' in repr(e):
                return

    def do_METHOD(self):
        self.parse_header()
        self.body = self.rfile.read(int(self.headers['Content-Length'])) if 'Content-Length' in self.headers else ''
        if self.sticky_filter:
            action = self.sticky_filter.filter(self)
            if action:
                return action.pop(0)(*action)
        for handler_filter in self.handler_filters:
            action = handler_filter.filter(self)
            if action:
                return action.pop(0)(*action)


class RangeFetch(object):
    """Range Fetch Class"""

    threads = 2
    maxsize = 1024*1024*4
    bufsize = 8192
    waitsize = 1024*512

    def __init__(self, handler, response, fetchservers, **kwargs):
        self.handler = handler
        self.url = handler.path
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
                        response = self.handler.create_http_request_withserver(fetchserver, self.handler.command, self.url, headers, self.handler.body, timeout=self.handler.connect_timeout, **self.kwargs)
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


class AdvancedProxyHandler(SimpleProxyHandler):
    """Advanced Proxy Handler"""
    dns_cache = LRUCache(64*1024)
    dns_servers = []
    dns_blacklist = []
    tcp_connection_time = collections.defaultdict(float)
    tcp_connection_time_with_clienthello = collections.defaultdict(float)
    tcp_connection_cache = collections.defaultdict(Queue.PriorityQueue)
    ssl_connection_time = collections.defaultdict(float)
    ssl_connection_cache = collections.defaultdict(Queue.PriorityQueue)
    ssl_connection_good_ipaddrs = {}
    ssl_connection_bad_ipaddrs = {}
    ssl_connection_unknown_ipaddrs = {}
    ssl_connection_keepalive = False
    max_window = 4
    openssl_context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)

    def gethostbyname2(self, hostname):
        try:
            iplist = self.dns_cache[hostname]
        except KeyError:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname) or ':' in hostname:
                iplist = [hostname]
            elif self.dns_servers:
                try:
                    record = dnslib_resolve_over_udp(hostname, self.dns_servers, timeout=2, blacklist=self.dns_blacklist)
                except socket.gaierror:
                    record = dnslib_resolve_over_tcp(hostname, self.dns_servers, timeout=2, blacklist=self.dns_blacklist)
                iplist = dnslib_record2iplist(record)
            else:
                iplist = socket.gethostbyname_ex(hostname)[-1]
            self.dns_cache[hostname] = iplist
        return iplist

    def create_tcp_connection(self, hostname, port, timeout, **kwargs):
        client_hello = kwargs.get('client_hello', None)
        cache_key = kwargs.get('cache_key') if not client_hello else None
        def create_connection(ipaddr, timeout, queobj):
            sock = None
            try:
                # create a ipv4/ipv6 socket object
                sock = socket.socket(socket.AF_INET if ':' not in ipaddr[0] else socket.AF_INET6)
                # set reuseaddr option to avoid 10048 socket error
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # resize socket recv buffer 8K->32K to improve browser releated application performance
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32*1024)
                # disable nagle algorithm to send http request quickly.
                sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
                # set a short timeout to trigger timeout retry more quickly.
                sock.settimeout(min(self.connect_timeout, timeout))
                # start connection time record
                start_time = time.time()
                # TCP connect
                sock.connect(ipaddr)
                # record TCP connection time
                self.tcp_connection_time[ipaddr] = time.time() - start_time
                # send client hello and peek server hello
                if client_hello:
                    sock.sendall(client_hello)
                    if gevent and isinstance(sock, gevent.socket.socket):
                        sock.data = data = sock.recv(4096)
                    else:
                        data = sock.recv(4096, socket.MSG_PEEK)
                    if not data:
                        logging.debug('create_tcp_connection %r with client_hello return NULL byte, continue %r', ipaddr, time.time()-start_time)
                        raise socket.timeout('timed out')
                    # record TCP connection time with client hello
                    self.tcp_connection_time_with_clienthello[ipaddr] = time.time() - start_time
                # set timeout
                sock.settimeout(timeout)
                # put tcp socket object to output queobj
                queobj.put(sock)
            except (socket.error, OSError) as e:
                # any socket.error, put Excpetions to output queobj.
                queobj.put(e)
                # reset a large and random timeout to the ipaddr
                self.tcp_connection_time[ipaddr] = self.connect_timeout+random.random()
                # close tcp socket
                if sock:
                    sock.close()
        def close_connection(count, queobj, first_tcp_time):
            for _ in range(count):
                sock = queobj.get()
                tcp_time_threshold = min(1, 1.3 * first_tcp_time)
                if sock and not isinstance(sock, Exception):
                    ipaddr = sock.getpeername()
                    if cache_key and self.tcp_connection_time[ipaddr] < tcp_time_threshold:
                        cache_queue = self.tcp_connection_cache[cache_key]
                        if cache_queue.qsize() < 8:
                            try:
                                _, old_sock = cache_queue.get_nowait()
                                old_sock.close()
                            except Queue.Empty:
                                pass
                        cache_queue.put((time.time(), sock))
                    else:
                        sock.close()
        try:
            while cache_key:
                ctime, sock = self.tcp_connection_cache[cache_key].get_nowait()
                if time.time() - ctime < 30:
                    return sock
                else:
                    sock.close()
        except Queue.Empty:
            pass
        addresses = [(x, port) for x in self.gethostbyname2(hostname)]
        sock = None
        for _ in range(kwargs.get('max_retry', 3)):
            window = min((self.max_window+1)//2, len(addresses))
            if client_hello:
                addresses.sort(key=self.tcp_connection_time_with_clienthello.__getitem__)
            else:
                addresses.sort(key=self.tcp_connection_time.__getitem__)
            addrs = addresses[:window] + random.sample(addresses, window)
            queobj = gevent.queue.Queue() if gevent else Queue.Queue()
            for addr in addrs:
                thread.start_new_thread(create_connection, (addr, timeout, queobj))
            for i in range(len(addrs)):
                sock = queobj.get()
                if not isinstance(sock, Exception):
                    first_tcp_time = self.tcp_connection_time[sock.getpeername()] if not cache_key else 0
                    thread.start_new_thread(close_connection, (len(addrs)-i-1, queobj, first_tcp_time))
                    return sock
                elif i == 0:
                    # only output first error
                    logging.warning('create_tcp_connection to %r with %s return %r, try again.', hostname, addrs, sock)
        if isinstance(sock, Exception):
            raise sock

    def create_ssl_connection(self, hostname, port, timeout, **kwargs):
        cache_key = kwargs.get('cache_key')
        validate = kwargs.get('validate')
        def create_connection(ipaddr, timeout, queobj):
            sock = None
            ssl_sock = None
            try:
                # create a ipv4/ipv6 socket object
                sock = socket.socket(socket.AF_INET if ':' not in ipaddr[0] else socket.AF_INET6)
                # set reuseaddr option to avoid 10048 socket error
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # resize socket recv buffer 8K->32K to improve browser releated application performance
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32*1024)
                # disable negal algorithm to send http request quickly.
                sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
                # set a short timeout to trigger timeout retry more quickly.
                sock.settimeout(min(self.connect_timeout, timeout))
                # pick up the certificate
                if not validate:
                    ssl_sock = ssl.wrap_socket(sock, ssl_version=self.ssl_version, do_handshake_on_connect=False)
                else:
                    ssl_sock = ssl.wrap_socket(sock, ssl_version=self.ssl_version, cert_reqs=ssl.CERT_REQUIRED, ca_certs=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cacert.pem'), do_handshake_on_connect=False)
                ssl_sock.settimeout(min(self.connect_timeout, timeout))
                # start connection time record
                start_time = time.time()
                # TCP connect
                ssl_sock.connect(ipaddr)
                connected_time = time.time()
                # SSL handshake
                ssl_sock.do_handshake()
                handshaked_time = time.time()
                # record TCP connection time
                self.tcp_connection_time[ipaddr] = ssl_sock.tcp_time = connected_time - start_time
                # record SSL connection time
                self.ssl_connection_time[ipaddr] = ssl_sock.ssl_time = handshaked_time - start_time
                ssl_sock.ssl_time = connected_time - start_time
                # sometimes, we want to use raw tcp socket directly(select/epoll), so setattr it to ssl socket.
                ssl_sock.sock = sock
                # remove from bad/unknown ipaddrs dict
                self.ssl_connection_bad_ipaddrs.pop(ipaddr, None)
                self.ssl_connection_unknown_ipaddrs.pop(ipaddr, None)
                # add to good ipaddrs dict
                if ipaddr not in self.ssl_connection_good_ipaddrs:
                    self.ssl_connection_good_ipaddrs[ipaddr] = handshaked_time
                # verify SSL certificate.
                if validate and hostname.endswith('.appspot.com'):
                    cert = ssl_sock.getpeercert()
                    orgname = next((v for ((k, v),) in cert['subject'] if k == 'organizationName'))
                    if not orgname.lower().startswith('google '):
                        raise ssl.SSLError("%r certificate organizationName(%r) not startswith 'Google'" % (hostname, orgname))
                # set timeout
                ssl_sock.settimeout(timeout)
                # put ssl socket object to output queobj
                queobj.put(ssl_sock)
            except (socket.error, ssl.SSLError, OSError) as e:
                # any socket.error, put Excpetions to output queobj.
                queobj.put(e)
                # reset a large and random timeout to the ipaddr
                self.ssl_connection_time[ipaddr] = self.connect_timeout + random.random()
                # add to bad ipaddrs dict
                if ipaddr not in self.ssl_connection_bad_ipaddrs:
                    self.ssl_connection_bad_ipaddrs[ipaddr] = time.time()
                # remove from good/unknown ipaddrs dict
                self.ssl_connection_good_ipaddrs.pop(ipaddr, None)
                self.ssl_connection_unknown_ipaddrs.pop(ipaddr, None)
                # close ssl socket
                if ssl_sock:
                    ssl_sock.close()
                # close tcp socket
                if sock:
                    sock.close()
        def create_connection_withopenssl(ipaddr, timeout, queobj):
            sock = None
            ssl_sock = None
            try:
                # create a ipv4/ipv6 socket object
                sock = socket.socket(socket.AF_INET if ':' not in ipaddr[0] else socket.AF_INET6)
                # set reuseaddr option to avoid 10048 socket error
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                # resize socket recv buffer 8K->32K to improve browser releated application performance
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 32*1024)
                # disable negal algorithm to send http request quickly.
                sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
                # set a short timeout to trigger timeout retry more quickly.
                sock.settimeout(timeout or self.connect_timeout)
                # pick up the certificate
                server_hostname = b'www.googleapis.com' if cache_key.startswith('google_') or hostname.endswith('.appspot.com') else None
                ssl_sock = SSLConnection(self.openssl_context, sock)
                ssl_sock.set_connect_state()
                if server_hostname and hasattr(ssl_sock, 'set_tlsext_host_name'):
                    ssl_sock.set_tlsext_host_name(server_hostname)
                # start connection time record
                start_time = time.time()
                # TCP connect
                ssl_sock.connect(ipaddr)
                connected_time = time.time()
                # SSL handshake
                ssl_sock.do_handshake()
                handshaked_time = time.time()
                # record TCP connection time
                self.tcp_connection_time[ipaddr] = ssl_sock.tcp_time = connected_time - start_time
                # record SSL connection time
                self.ssl_connection_time[ipaddr] = ssl_sock.ssl_time = handshaked_time - start_time
                # sometimes, we want to use raw tcp socket directly(select/epoll), so setattr it to ssl socket.
                ssl_sock.sock = sock
                # remove from bad/unknown ipaddrs dict
                self.ssl_connection_bad_ipaddrs.pop(ipaddr, None)
                self.ssl_connection_unknown_ipaddrs.pop(ipaddr, None)
                # add to good ipaddrs dict
                if ipaddr not in self.ssl_connection_good_ipaddrs:
                    self.ssl_connection_good_ipaddrs[ipaddr] = handshaked_time
                # verify SSL certificate.
                if validate and hostname.endswith('.appspot.com'):
                    cert = ssl_sock.get_peer_certificate()
                    commonname = next((v for k, v in cert.get_subject().get_components() if k == 'CN'))
                    if '.google' not in commonname and not commonname.endswith('.appspot.com'):
                        raise socket.error("Host name '%s' doesn't match certificate host '%s'" % (hostname, commonname))
                # put ssl socket object to output queobj
                queobj.put(ssl_sock)
            except (socket.error, OpenSSL.SSL.Error, OSError) as e:
                # any socket.error, put Excpetions to output queobj.
                queobj.put(e)
                # reset a large and random timeout to the ipaddr
                self.ssl_connection_time[ipaddr] = self.connect_timeout + random.random()
                # add to bad ipaddrs dict
                if ipaddr not in self.ssl_connection_bad_ipaddrs:
                    self.ssl_connection_bad_ipaddrs[ipaddr] = time.time()
                # remove from good/unknown ipaddrs dict
                self.ssl_connection_good_ipaddrs.pop(ipaddr, None)
                self.ssl_connection_unknown_ipaddrs.pop(ipaddr, None)
                # close ssl socket
                if ssl_sock:
                    ssl_sock.close()
                # close tcp socket
                if sock:
                    sock.close()
        def close_connection(count, queobj, first_tcp_time, first_ssl_time):
            for _ in range(count):
                sock = queobj.get()
                ssl_time_threshold = min(1, 1.3 * first_ssl_time)
                if sock and not isinstance(sock, Exception):
                    if cache_key and sock.ssl_time < ssl_time_threshold:
                        cache_queue = self.ssl_connection_cache[cache_key]
                        if cache_queue.qsize() < 8:
                            try:
                                _, old_sock = cache_queue.get_nowait()
                                old_sock.close()
                            except Queue.Empty:
                                pass
                        cache_queue.put((time.time(), sock))
                    else:
                        sock.close()
        def reorg_ipaddrs():
            current_time = time.time()
            for ipaddr, ctime in self.ssl_connection_good_ipaddrs.items():
                if current_time - ctime > 4 * 60:
                    self.ssl_connection_good_ipaddrs.pop(ipaddr, None)
                    self.ssl_connection_unknown_ipaddrs[ipaddr] = ctime
            for ipaddr, ctime in self.ssl_connection_bad_ipaddrs.items():
                if current_time - ctime > 6 * 60:
                    self.ssl_connection_bad_ipaddrs.pop(ipaddr, None)
                    self.ssl_connection_unknown_ipaddrs[ipaddr] = ctime
            logging.info("good_ipaddrs=%d, bad_ipaddrs=%d, unkown_ipaddrs=%d", len(self.ssl_connection_good_ipaddrs), len(self.ssl_connection_bad_ipaddrs), len(self.ssl_connection_unknown_ipaddrs))
        try:
            while cache_key:
                ctime, sock = self.ssl_connection_cache[cache_key].get_nowait()
                if time.time() - ctime < 30:
                    return sock
                else:
                    sock.close()
        except Queue.Empty:
            pass
        addresses = [(x, port) for x in self.gethostbyname2(hostname)]
        sock = None
        for i in range(kwargs.get('max_retry', 5)):
            reorg_ipaddrs()
            window = self.max_window + i
            good_ipaddrs = [x for x in addresses if x in self.ssl_connection_good_ipaddrs]
            good_ipaddrs = sorted(good_ipaddrs, key=self.ssl_connection_time.get)[:window]
            unkown_ipaddrs = [x for x in addresses if x not in self.ssl_connection_good_ipaddrs and x not in self.ssl_connection_bad_ipaddrs]
            random.shuffle(unkown_ipaddrs)
            unkown_ipaddrs = unkown_ipaddrs[:window]
            bad_ipaddrs = [x for x in addresses if x in self.ssl_connection_bad_ipaddrs]
            bad_ipaddrs = sorted(bad_ipaddrs, key=self.ssl_connection_bad_ipaddrs.get)[:window]
            addrs = good_ipaddrs + unkown_ipaddrs + bad_ipaddrs
            remain_window = 3 * window - len(addrs)
            if 0 < remain_window <= len(addresses):
                addrs += random.sample(addresses, remain_window)
            logging.debug('%s good_ipaddrs=%d, unkown_ipaddrs=%r, bad_ipaddrs=%r', cache_key, len(good_ipaddrs), len(unkown_ipaddrs), len(bad_ipaddrs))
            queobj = gevent.queue.Queue() if gevent else Queue.Queue()
            for addr in addrs:
                thread.start_new_thread(create_connection_withopenssl, (addr, timeout, queobj))
            for i in range(len(addrs)):
                sock = queobj.get()
                if not isinstance(sock, Exception):
                    thread.start_new_thread(close_connection, (len(addrs)-i-1, queobj, sock.tcp_time, sock.ssl_time))
                    return sock
                elif i == 0:
                    # only output first error
                    logging.warning('create_ssl_connection to %r with %s return %r, try again.', hostname, addrs, sock)
        if isinstance(sock, Exception):
            raise sock

    def create_http_request(self, method, url, headers, body, timeout, max_retry=2, bufsize=8192, crlf=None, validate=None, cache_key=None):
        scheme, netloc, path, query, _ = urlparse.urlsplit(url)
        if netloc.rfind(':') <= netloc.rfind(']'):
            # no port number
            host = netloc
            port = 443 if scheme == 'https' else 80
        else:
            host, _, port = netloc.rpartition(':')
            port = int(port)
        if query:
            path += '?' + query
        if 'Host' not in headers:
            headers['Host'] = host
        if body and 'Content-Length' not in headers:
            headers['Content-Length'] = str(len(body))
        sock = None
        for i in range(max_retry):
            try:
                create_connection = self.create_ssl_connection if scheme == 'https' else self.create_tcp_connection
                sock = create_connection(host, port, timeout, validate=validate, cache_key=cache_key)
                break
            except StandardError as e:
                logging.exception('create_http_request "%s %s" failed:%s', method, url, e)
                if sock:
                    sock.close()
                if i == max_retry - 1:
                    raise
        request_data = ''
        crlf_counter = 0
        if scheme != 'https' and crlf:
            fakeheaders = dict((k.title(), v) for k, v in headers.items())
            fakeheaders.pop('Content-Length', None)
            fakeheaders.pop('Cookie', None)
            fakeheaders.pop('Host', None)
            if 'User-Agent' not in fakeheaders:
                fakeheaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1878.0 Safari/537.36'
            if 'Accept-Language' not in fakeheaders:
                fakeheaders['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'
            if 'Accept' not in fakeheaders:
                fakeheaders['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            fakeheaders_data = ''.join('%s: %s\r\n' % (k, v) for k, v in fakeheaders.items() if k not in self.skip_headers)
            while crlf_counter < 5 or len(request_data) < 1500 * 2:
                request_data += 'GET / HTTP/1.1\r\n%s\r\n' % fakeheaders_data
                crlf_counter += 1
            request_data += '\r\n\r\n\r\n'
        request_data += '%s %s %s\r\n' % (method, path, self.protocol_version)
        request_data += ''.join('%s: %s\r\n' % (k.title(), v) for k, v in headers.items() if k.title() not in self.skip_headers)
        request_data += '\r\n'
        if isinstance(body, bytes):
            sock.sendall(request_data.encode() + body)
        elif hasattr(body, 'read'):
            sock.sendall(request_data)
            while 1:
                data = body.read(bufsize)
                if not data:
                    break
                sock.sendall(data)
        else:
            raise TypeError('create_http_request(body) must be a string or buffer, not %r' % type(body))
        response = None
        try:
            while crlf_counter:
                if sys.version[:3] == '2.7':
                    response = httplib.HTTPResponse(sock, buffering=False)
                else:
                    response = httplib.HTTPResponse(sock)
                    response.fp.close()
                    response.fp = sock.makefile('rb', 0)
                response.begin()
                response.read()
                response.close()
                crlf_counter -= 1
        except StandardError as e:
            logging.exception('crlf skip read host=%r path=%r error: %r', headers.get('Host'), path, e)
            if response:
                if response.fp and response.fp._sock:
                    response.fp._sock.close()
                response.close()
            if sock:
                sock.close()
            return None
        if sys.version[:3] == '2.7':
            response = httplib.HTTPResponse(sock, buffering=True)
        else:
            response = httplib.HTTPResponse(sock)
            response.fp.close()
            response.fp = sock.makefile('rb')
        response.begin()
        if self.ssl_connection_keepalive and scheme == 'https' and cache_key:
            response.cache_key = cache_key
            response.cache_sock = response.fp._sock
        return response

    def handle_urlfetch_response_close(self, fetchserver, response):
        cache_sock = getattr(response, 'cache_sock', None)
        if cache_sock:
            if self.scheme == 'https':
                self.ssl_connection_cache[response.cache_key].put((time.time(), cache_sock))
            else:
                cache_sock.close()
            del response.cache_sock

    def handle_urlfetch_error(self, fetchserver, response):
        pass


class Common(object):
    """Global Config Object"""

    ENV_CONFIG_PREFIX = 'GOAGENT_'

    def __init__(self):
        """load config from proxy.ini"""
        ConfigParser.RawConfigParser.OPTCRE = re.compile(r'(?P<option>[^=\s][^=]*)\s*(?P<vi>[=])\s*(?P<value>.*)$')
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

        self.GAE_APPIDS = re.findall(r'[\w\-\.]+', self.CONFIG.get('gae', 'appid').replace('.appspot.com', ''))
        self.GAE_PASSWORD = self.CONFIG.get('gae', 'password').strip()
        self.GAE_PATH = self.CONFIG.get('gae', 'path')
        self.GAE_MODE = self.CONFIG.get('gae', 'mode')
        self.GAE_PROFILE = self.CONFIG.get('gae', 'profile').strip()
        self.GAE_WINDOW = self.CONFIG.getint('gae', 'window')
        self.GAE_KEEPALIVE = self.CONFIG.getint('gae', 'keepalive') if self.CONFIG.has_option('gae', 'keepalive') else 0
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
        hosts_section, http_section = '%s/hosts' % self.GAE_PROFILE, '%s/http' % self.GAE_PROFILE

        if 'USERDNSDOMAIN' in os.environ and re.match(r'^\w+\.\w+$', os.environ['USERDNSDOMAIN']):
            self.CONFIG.set(hosts_section, '.' + os.environ['USERDNSDOMAIN'], '')

        self.HOST_MAP = collections.OrderedDict((k, v or k) for k, v in self.CONFIG.items(hosts_section) if '\\' not in k and ':' not in k and not k.startswith('.'))
        self.HOST_POSTFIX_MAP = collections.OrderedDict((k, v) for k, v in self.CONFIG.items(hosts_section) if '\\' not in k and ':' not in k and k.startswith('.'))
        self.HOST_POSTFIX_ENDSWITH = tuple(self.HOST_POSTFIX_MAP)

        self.HOSTPORT_MAP = collections.OrderedDict((k, v) for k, v in self.CONFIG.items(hosts_section) if ':' in k and not k.startswith('.'))
        self.HOSTPORT_POSTFIX_MAP = collections.OrderedDict((k, v) for k, v in self.CONFIG.items(hosts_section) if ':' in k and k.startswith('.'))
        self.HOSTPORT_POSTFIX_ENDSWITH = tuple(self.HOSTPORT_POSTFIX_MAP)

        self.URLRE_MAP = collections.OrderedDict((re.compile(k).match, v) for k, v in self.CONFIG.items(hosts_section) if '\\' in k)

        self.HTTP_WITHGAE = set(self.CONFIG.get(http_section, 'withgae').split('|'))
        self.HTTP_CRLFSITES = tuple(self.CONFIG.get(http_section, 'crlfsites').split('|'))
        self.HTTP_FORCEHTTPS = tuple(self.CONFIG.get(http_section, 'forcehttps').split('|')) if self.CONFIG.get(http_section, 'forcehttps').strip() else tuple()
        self.HTTP_NOFORCEHTTPS = set(self.CONFIG.get(http_section, 'noforcehttps').split('|')) if self.CONFIG.get(http_section, 'noforcehttps').strip() else set()
        self.HTTP_FAKEHTTPS = tuple(self.CONFIG.get(http_section, 'fakehttps').split('|')) if self.CONFIG.get(http_section, 'fakehttps').strip() else tuple()
        self.HTTP_NOFAKEHTTPS = set(self.CONFIG.get(http_section, 'nofakehttps').split('|')) if self.CONFIG.get(http_section, 'nofakehttps').strip() else set()
        self.HTTP_DNS = self.CONFIG.get(http_section, 'dns').split('|') if self.CONFIG.has_option(http_section, 'dns') else []

        self.IPLIST_MAP = collections.OrderedDict((k, v.split('|')) for k, v in self.CONFIG.items('iplist'))
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
        self.PHP_FETCHSERVER = self.CONFIG.get('php', 'fetchserver')
        self.PHP_USEHOSTS = self.CONFIG.getint('php', 'usehosts')

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
        self.AUTORANGE_HOSTS_MATCH = [re.compile(fnmatch.translate(h)).match for h in self.AUTORANGE_HOSTS]
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
                    logging.warning('%r remote host=%r failed: %s', dnslib_resolve, host, e)
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
            if name == 'google_hk':
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
        info += 'GoAgent Version    : %s (python/%s %spyopenssl/%s)\n' % (__version__, sys.version[:5], gevent and 'gevent/%s ' % gevent.__version__ or '', getattr(OpenSSL, '__version__', 'Disabled'))
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
            info += 'PHP FetchServer    : %s\n' % common.PHP_FETCHSERVER
        if common.DNS_ENABLE:
            info += 'DNS Listen         : %s\n' % common.DNS_LISTEN
            info += 'DNS Servers        : %s\n' % '|'.join(common.DNS_SERVERS)
        info += '------------------------------------------------------\n'
        return info

common = Common()


def message_html(title, banner, detail=''):
    MESSAGE_TEMPLATE = '''
    <html><head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <title>$title</title>
    <style><!--
    body {font-family: arial,sans-serif}
    div.nav {margin-top: 1ex}
    div.nav A {font-size: 10pt; font-family: arial,sans-serif}
    span.nav {font-size: 10pt; font-family: arial,sans-serif; font-weight: bold}
    div.nav A,span.big {font-size: 12pt; color: #0000cc}
    div.nav A {font-size: 10pt; color: black}
    A.l:link {color: #6f6f6f}
    A.u:link {color: green}
    //--></style>
    </head>
    <body text=#000000 bgcolor=#ffffff>
    <table border=0 cellpadding=2 cellspacing=0 width=100%>
    <tr><td bgcolor=#3366cc><font face=arial,sans-serif color=#ffffff><b>Message From LocalProxy</b></td></tr>
    <tr><td> </td></tr></table>
    <blockquote>
    <H1>$banner</H1>
    $detail
    <p>
    </blockquote>
    <table width=100% cellpadding=0 cellspacing=0><tr><td bgcolor=#3366cc><img alt="" width=1 height=4></td></tr></table>
    </body></html>
    '''
    return string.Template(MESSAGE_TEMPLATE).substitute(title=title, banner=banner, detail=detail)


try:
    from Crypto.Cipher.ARC4 import new as RC4Cipher
except ImportError:
    logging.warn('Load Crypto.Cipher.ARC4 Failed, Use Pure Python Instead.')
    class RC4Cipher(object):
        def __init__(self, key):
            x = 0
            box = range(256)
            for i, y in enumerate(box):
                x = (x + y + ord(key[i % len(key)])) & 0xff
                box[i], box[x] = box[x], y
            self.__box = box
            self.__x = 0
            self.__y = 0
        def encrypt(self, data):
            out = []
            out_append = out.append
            x = self.__x
            y = self.__y
            box = self.__box
            for char in data:
                x = (x + 1) & 0xff
                y = (y + box[x]) & 0xff
                box[x], box[y] = box[y], box[x]
                out_append(chr(ord(char) ^ box[(box[x] + box[y]) & 0xff]))
            self.__x = x
            self.__y = y
            return ''.join(out)


class XORCipher(object):
    """XOR Cipher Class"""
    def __init__(self, key):
        self.__key_gen = itertools.cycle([ord(x) for x in key]).next
        self.__key_xor = lambda s: ''.join(chr(ord(x) ^ self.__key_gen()) for x in s)
        if len(key) == 1:
            try:
                from Crypto.Util.strxor import strxor_c
                c = ord(key)
                self.__key_xor = lambda s: strxor_c(s, c)
            except ImportError:
                sys.stderr.write('Load Crypto.Util.strxor Failed, Use Pure Python Instead.\n')

    def encrypt(self, data):
        return self.__key_xor(data)


class CipherFileObject(object):
    """fileobj wrapper for cipher"""
    def __init__(self, fileobj, cipher):
        self.__fileobj = fileobj
        self.__cipher = cipher
    def __getattr__(self, attr):
        if attr not in ('__fileobj', '__cipher'):
            return getattr(self.__fileobj, attr)
    def read(self, size=-1):
        return self.__cipher.encrypt(self.__fileobj.read(size))


class LocalProxyServer(SocketServer.ThreadingTCPServer):
    """Local Proxy Server"""
    request_queue_size = 256
    allow_reuse_address = True
    daemon_threads = True

    def close_request(self, request):
        try:
            request.close()
        except StandardError:
            pass

    def finish_request(self, request, client_address):
        try:
            self.RequestHandlerClass(request, client_address, self)
        except NetWorkIOError as e:
            if e[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise

    def handle_error(self, *args):
        """make ThreadingTCPServer happy"""
        exc_info = sys.exc_info()
        error = exc_info and len(exc_info) and exc_info[1]
        if isinstance(error, NetWorkIOError) and len(error.args) > 1 and 'bad write retry' in error.args[1]:
            exc_info = error = None
        else:
            del exc_info, error
            SocketServer.ThreadingTCPServer.handle_error(self, *args)


class UserAgentFilter(BaseProxyHandlerFilter):
    """user agent filter"""
    def __init__(self, user_agent):
        self.user_agent = user_agent

    def filter(self, handler):
        handler.headers['User-Agent'] = self.user_agent


class WithGAEFilter(BaseProxyHandlerFilter):
    """with gae filter"""
    def __init__(self, withgae_sites):
        self.withgae_sites = set(withgae_sites)

    def filter(self, handler):
        if handler.host in self.withgae_sites:
            logging.debug('WithGAEFilter metched %r %r', handler.path, handler.headers)
            # assume the last one handler is GAEFetchFilter
            return handler.handler_filters[-1].filter(handler)


class ForceHttpsFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def __init__(self, forcehttps_sites, noforcehttps_sites):
        self.forcehttps_sites = tuple(forcehttps_sites)
        self.noforcehttps_sites = set(noforcehttps_sites)

    def filter(self, handler):
        if handler.command != 'CONNECT' and handler.host.endswith(self.forcehttps_sites) and handler.host not in self.noforcehttps_sites:
            if not handler.headers.get('Referer', '').startswith('https://') and not handler.path.startswith('https://'):
                logging.debug('ForceHttpsFilter metched %r %r', handler.path, handler.headers)
                headers = {'Location': handler.path.replace('http://', 'https://', 1), 'Connection': 'close'}
                return [handler.MOCK, 301, headers, '']


class FakeHttpsFilter(BaseProxyHandlerFilter):
    """fake https filter"""
    def __init__(self, fakehttps_sites, nofakehttps_sites):
        self.fakehttps_sites = tuple(fakehttps_sites)
        self.nofakehttps_sites = set(nofakehttps_sites)

    def filter(self, handler):
        if handler.command == 'CONNECT' and handler.host.endswith(self.fakehttps_sites) and handler.host not in self.nofakehttps_sites:
            logging.debug('FakeHttpsFilter metched %r %r', handler.path, handler.headers)
            return [handler.STRIP, True, None]



class URLRewriteFilter(BaseProxyHandlerFilter):
    """url rewrite filter"""
    rules = {
                'www.google.com': (r'^https?://www\.google\.com/url\?.*url=([^&]+)', lambda m: urllib.unquote_plus(m.group(1))),
                'www.google.com.hk': (r'^https?://www\.google\.com\.hk/url\?.*url=([^&]+)', lambda m: urllib.unquote_plus(m.group(1))),
            }
    def filter(self, handler):
        if handler.host in self.rules:
            pattern, callback = self.rules[handler.host]
            m = re.search(pattern, handler.path)
            if m:
                logging.debug('URLRewriteFilter metched %r', handler.path)
                headers = {'Location': callback(m), 'Connection': 'close'}
                return [handler.MOCK, 301, headers, '']


class HostsFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter_localfile(self, handler, filename):
        content_type = None
        try:
            import mimetypes
            content_type = mimetypes.types_map.get(os.path.splitext(filename)[1])
        except StandardError as e:
            logging.error('import mimetypes failed: %r', e)
        try:
            with open(filename, 'rb') as fp:
                data = fp.read()
                headers = {'Connection': 'close', 'Content-Length': str(len(data))}
                if content_type:
                    headers['Content-Type'] = content_type
                return [handler.MOCK, 200, headers, data]
        except StandardError as e:
            return [handler.MOCK, 403, {'Connection': 'close'}, 'read %r %r' % (filename, e)]

    def filter(self, handler):
        host, port = handler.host, handler.port
        hostport = handler.path if handler.command == 'CONNECT' else '%s:%d' % (host, port)
        hostname = ''
        if host in common.HOST_MAP:
            hostname = common.HOST_MAP[host] or host
        elif host.endswith(common.HOST_POSTFIX_ENDSWITH):
            hostname = next(common.HOST_POSTFIX_MAP[x] for x in common.HOST_POSTFIX_MAP if host.endswith(x)) or host
            common.HOST_MAP[host] = hostname
        if hostport in common.HOSTPORT_MAP:
            hostname = common.HOSTPORT_MAP[hostport] or host
        elif hostport.endswith(common.HOSTPORT_POSTFIX_ENDSWITH):
            hostname = next(common.HOSTPORT_POSTFIX_MAP[x] for x in common.HOSTPORT_POSTFIX_MAP if hostport.endswith(x)) or host
            common.HOSTPORT_MAP[hostport] = hostname
        if handler.command != 'CONNECT' and common.URLRE_MAP:
            try:
                hostname = next(common.URLRE_MAP[x] for x in common.URLRE_MAP if x(handler.path)) or host
            except StopIteration:
                pass
        if not hostname:
            return None
        elif hostname in common.IPLIST_MAP:
            handler.dns_cache[host] = common.IPLIST_MAP[hostname]
        elif hostname == host and host.endswith(common.DNS_TCPOVER) and host not in handler.dns_cache:
            try:
                iplist = dnslib_record2iplist(dnslib_resolve_over_tcp(host, handler.dns_servers, timeout=4, blacklist=handler.dns_blacklist))
                logging.info('HostsFilter dnslib_resolve_over_tcp %r with %r return %s', host, handler.dns_servers, iplist)
                handler.dns_cache[host] = iplist
            except socket.error as e:
                logging.warning('HostsFilter dnslib_resolve_over_tcp %r with %r failed: %r', host, handler.dns_servers, e)
        elif re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname) or ':' in hostname:
            handler.dns_cache[host] = [hostname]
        elif hostname.startswith('file://'):
            filename = hostname.lstrip('file://')
            if os.name == 'nt':
                filename = filename.lstrip('/')
            return self.filter_localfile(handler, filename)
        cache_key = '%s:%s' % (hostname, port)
        if handler.command == 'CONNECT':
            return [handler.FORWARD, host, port, handler.connect_timeout, {'cache_key': cache_key}]
        else:
            if host.endswith(common.HTTP_CRLFSITES):
                handler.close_connection = True
                return [handler.DIRECT, {'crlf': True}]
            else:
                return [handler.DIRECT, {'cache_key': cache_key}]


class DirectRegionFilter(BaseProxyHandlerFilter):
    """direct region filter"""
    geoip = pygeoip.GeoIP(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GeoIP.dat')) if pygeoip and common.GAE_REGIONS else None
    region_cache = LRUCache(16*1024)

    def __init__(self, regions):
        self.regions = set(regions)

    def get_country_code(self, hostname, dnsservers):
        """http://dev.maxmind.com/geoip/legacy/codes/iso3166/"""
        try:
            return self.region_cache[hostname]
        except KeyError:
            pass
        try:
            if re.match(r'^\d+\.\d+\.\d+\.\d+$', hostname) or ':' in hostname:
                iplist = [hostname]
            elif dnsservers:
                iplist = dnslib_record2iplist(dnslib_resolve_over_udp(hostname, dnsservers, timeout=2))
            else:
                iplist = socket.gethostbyname_ex(hostname)[-1]
            country_code = self.geoip.country_code_by_addr(iplist[0])
        except StandardError as e:
            logging.warning('DirectRegionFilter cannot determine region for hostname=%r %r', hostname, e)
            country_code = ''
        self.region_cache[hostname] = country_code
        return country_code

    def filter(self, handler):
        if self.geoip:
            country_code = self.get_country_code(handler.host, handler.dns_servers)
            if country_code in self.regions:
                if handler.command == 'CONNECT':
                    return [handler.FORWARD, handler.host, handler.port, handler.connect_timeout]
                else:
                    return [handler.DIRECT, {}]


class AutoRangeFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter(self, handler):
        path = urlparse.urlsplit(handler.path).path
        need_autorange = any(x(handler.host) for x in common.AUTORANGE_HOSTS_MATCH) or path.endswith(common.AUTORANGE_ENDSWITH)
        if path.endswith(common.AUTORANGE_NOENDSWITH) or 'range=' in urlparse.urlsplit(path).query or handler.command == 'HEAD':
            need_autorange = False
        if handler.command != 'HEAD' and handler.headers.get('Range'):
            m = re.search(r'bytes=(\d+)-', handler.headers['Range'])
            start = int(m.group(1) if m else 0)
            handler.headers['Range'] = 'bytes=%d-%d' % (start, start+common.AUTORANGE_MAXSIZE-1)
            logging.info('autorange range=%r match url=%r', handler.headers['Range'], handler.path)
        elif need_autorange:
            logging.info('Found [autorange]endswith match url=%r', handler.path)
            m = re.search(r'bytes=(\d+)-', handler.headers.get('Range', ''))
            start = int(m.group(1) if m else 0)
            handler.headers['Range'] = 'bytes=%d-%d' % (start, start+common.AUTORANGE_MAXSIZE-1)


class GAEFetchFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter(self, handler):
        """https://developers.google.com/appengine/docs/python/urlfetch/"""
        if handler.command == 'CONNECT':
            do_ssl_handshake = 440 <= handler.port <= 450 or 1024 <= handler.port <= 65535
            return [handler.STRIP, do_ssl_handshake, self if not common.URLRE_MAP else None]
        elif handler.command in ('GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'PATCH'):
            kwargs = {}
            if common.GAE_PASSWORD:
                kwargs['password'] = common.GAE_PASSWORD
            if common.GAE_VALIDATE:
                kwargs['validate'] = 1
            fetchservers = ['%s://%s.appspot.com%s' % (common.GAE_MODE, x, common.GAE_PATH) for x in common.GAE_APPIDS]
            return [handler.URLFETCH, fetchservers, common.FETCHMAX_LOCAL, kwargs]
        else:
            if common.PHP_ENABLE:
                return PHPProxyHandler.handler_filters[-1].filter(handler)
            else:
                logging.warning('"%s %s" not supported by GAE, please enable PHP mode!', handler.command, handler.host)
                return [handler.DIRECT, {}]


class GAEProxyHandler(AdvancedProxyHandler):
    """GAE Proxy Handler"""
    handler_filters = [GAEFetchFilter()]

    def first_run(self):
        """GAEProxyHandler setup, init domain/iplist map"""
        if not common.PROXY_ENABLE:
            logging.info('resolve common.IPLIST_MAP names=%s to iplist', list(common.IPLIST_MAP))
            common.resolve_iplist()
        random.shuffle(common.GAE_APPIDS)

    def gethostbyname2(self, hostname):
        for postfix in ('.appspot.com', '.googleusercontent.com'):
            if hostname.endswith(postfix):
                host = common.HOST_MAP.get(hostname) or common.HOST_POSTFIX_MAP[postfix]
                return common.IPLIST_MAP.get(host) or host.split('|')
        return AdvancedProxyHandler.gethostbyname2(self, hostname)

    def handle_urlfetch_error(self, fetchserver, response):
        gae_appid = urlparse.urlsplit(fetchserver).hostname.split('.')[-3]
        if response.app_status == 503:
            # appid over qouta, switch to next appid
            if gae_appid == common.GAE_APPIDS[0] and len(common.GAE_APPIDS) > 1:
                common.GAE_APPIDS.append(common.GAE_APPIDS.pop(0))
                logging.info('gae_appid=%r over qouta, switch next appid=%r', gae_appid, common.GAE_APPIDS[0])


class PHPFetchFilter(BaseProxyHandlerFilter):
    """force https filter"""
    def filter(self, handler):
        if handler.command == 'CONNECT':
            return [handler.STRIP, True, self]
        else:
            kwargs = {}
            if common.PHP_PASSWORD:
                kwargs['password'] = common.PHP_PASSWORD
            if common.PHP_VALIDATE:
                kwargs['validate'] = 1
            return [handler.URLFETCH, [common.PHP_FETCHSERVER], 1, kwargs]


class PHPProxyHandler(AdvancedProxyHandler):
    """PHP Proxy Handler"""
    first_run_lock = threading.Lock()
    handler_filters = [PHPFetchFilter()]

    def first_run(self):
        if common.PHP_USEHOSTS:
            self.handler_filters.insert(-1, HostsFilter())
        if not common.PROXY_ENABLE:
            common.resolve_iplist()
            fetchhost = urlparse.urlsplit(common.PHP_FETCHSERVER).hostname
            logging.info('resolve common.PHP_FETCHSERVER domain=%r to iplist', fetchhost)
            if common.PHP_USEHOSTS and fetchhost in common.HOST_MAP:
                hostname = common.HOST_MAP[fetchhost]
                fetchhost_iplist = sum([socket.gethostbyname_ex(x)[-1] for x in common.IPLIST_MAP.get(hostname) or hostname.split('|')], [])
            else:
                fetchhost_iplist = self.gethostbyname2(fetchhost)
            if len(fetchhost_iplist) == 0:
                logging.error('resolve %r domain return empty! please use ip list to replace domain list!', fetchhost)
                sys.exit(-1)
            self.dns_cache[fetchhost] = list(set(fetchhost_iplist))
            logging.info('resolve common.PHP_FETCHSERVER domain to iplist=%r', fetchhost_iplist)
        return True


class ProxyChainMixin:
    """proxy chain mixin"""

    def gethostbyname2(self, hostname):
        try:
            return socket.gethostbyname_ex(hostname)[-1]
        except socket.error:
            return [hostname]

    def create_tcp_connection(self, hostname, port, timeout, **kwargs):
        sock = socket.create_connection((common.PROXY_HOST, int(common.PROXY_PORT)))
        if hostname.endswith('.appspot.com'):
            hostname = 'www.google.com'
        request_data = 'CONNECT %s:%s HTTP/1.1\r\n' % (hostname, port)
        if common.PROXY_USERNAME and common.PROXY_PASSWROD:
            request_data += 'Proxy-Authorization: Basic %s\r\n' % base64.b64encode(('%s:%s' % (common.PROXY_USERNAME, common.PROXY_PASSWROD)).encode()).decode().strip()
        request_data += '\r\n'
        sock.sendall(request_data)
        response = httplib.HTTPResponse(sock)
        response.fp.close()
        response.fp = sock.makefile('rb', 0)
        response.begin()
        if response.status >= 400:
            raise httplib.BadStatusLine('%s %s %s' % (response.version, response.status, response.reason))
        return sock

    def create_ssl_connection(self, hostname, port, timeout, **kwargs):
        sock = self.create_tcp_connection(hostname, port, timeout, **kwargs)
        ssl_sock = ssl.wrap_socket(sock)
        return ssl_sock


class GreenForwardMixin:
    """green forward mixin"""

    @staticmethod
    def io_copy(dest, source, timeout, bufsize):
        try:
            dest.settimeout(timeout)
            source.settimeout(timeout)
            while 1:
                data = source.recv(bufsize)
                if not data:
                    break
                dest.sendall(data)
        except socket.timeout:
            pass
        except NetWorkIOError as e:
            if e.args[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.ENOTCONN, errno.EPIPE):
                raise
            if e.args[0] in (errno.EBADF,):
                return
        finally:
            for sock in (dest, source):
                try:
                    sock.close()
                except StandardError:
                    pass

    def forward_socket(self, local, remote, timeout):
        """forward socket"""
        bufsize = self.bufsize
        thread.start_new_thread(GreenForwardMixin.io_copy, (remote.dup(), local.dup(), timeout, bufsize))
        GreenForwardMixin.io_copy(local, remote, timeout, bufsize)


class ProxyChainGAEProxyHandler(ProxyChainMixin, GAEProxyHandler):
    pass


class ProxyChainPHPProxyHandler(ProxyChainMixin, PHPProxyHandler):
    pass


class GreenForwardGAEProxyHandler(GreenForwardMixin, GAEProxyHandler):
    pass


class GreenForwardPHPProxyHandler(GreenForwardMixin, PHPProxyHandler):
    pass


class ProxyChainGreenForwardGAEProxyHandler(ProxyChainMixin, GreenForwardGAEProxyHandler):
    pass


class ProxyChainGreenForwardPHPProxyHandler(ProxyChainMixin, GreenForwardPHPProxyHandler):
    pass


def get_uptime():
    if os.name == 'nt':
        import ctypes
        try:
            tick = ctypes.windll.kernel32.GetTickCount64()
        except AttributeError:
            tick = ctypes.windll.kernel32.GetTickCount()
        return tick / 1000.0
    elif os.path.isfile('/proc/uptime'):
        with open('/proc/uptime', 'rb') as fp:
            uptime = fp.readline().strip().split()[0].strip()
            return float(uptime)
    elif any(os.path.isfile(os.path.join(x, 'uptime')) for x in os.environ['PATH'].split(os.pathsep)):
        # http://www.opensource.apple.com/source/lldb/lldb-69/test/pexpect-2.4/examples/uptime.py
        pattern = r'up\s+(.*?),\s+([0-9]+) users?,\s+load averages?: ([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9]),?\s+([0-9]+\.[0-9][0-9])'
        output = os.popen('uptime').read()
        duration, _, _, _, _ = re.search(pattern, output).groups()
        days, hours, mins = 0, 0, 0
        if 'day' in duration:
            m = re.search(r'([0-9]+)\s+day', duration)
            days = int(m.group(1))
        if ':' in duration:
            m = re.search(r'([0-9]+):([0-9]+)', duration)
            hours = int(m.group(1))
            mins = int(m.group(2))
        if 'min' in duration:
            m = re.search(r'([0-9]+)\s+min', duration)
            mins = int(m.group(1))
        return days * 86400 + hours * 3600 + mins * 60
    else:
        #TODO: support other platforms
        return None


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
                    return [handler.MOCK, 403, {'Content-Type': 'text/plain'}, 'client address %r not allowed' % handler.client_address[0]]
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
                return [handler.MOCK, 200, headers, content]


class StaticFileFilter(BaseProxyHandlerFilter):
    """static file filter"""
    index_file = 'index.html'

    def format_index_html(self, dirname):
        INDEX_TEMPLATE = u'''
        <html>
        <title>Directory listing for $dirname</title>
        <body>
        <h2>Directory listing for $dirname</h2>
        <hr>
        <ul>
        $html
        </ul>
        <hr>
        </body></html>
        '''
        html = ''
        if not isinstance(dirname, unicode):
            dirname = dirname.decode(sys.getfilesystemencoding())
        for name in os.listdir(dirname):
            fullname = os.path.join(dirname, name)
            suffix = u'/' if os.path.isdir(fullname) else u''
            html += u'<li><a href="%s%s">%s%s</a>\r\n' % (name, suffix, name, suffix)
        return string.Template(INDEX_TEMPLATE).substitute(dirname=dirname, html=html)

    def filter(self, handler):
        path = urlparse.urlsplit(handler.path).path
        if path.startswith('/'):
            path = urllib.unquote_plus(path.lstrip('/') or '.').decode('utf8')
            if os.path.isdir(path):
                index_file = os.path.join(path, self.index_file)
                if not os.path.isfile(index_file):
                    content = self.format_index_html(path).encode('UTF-8')
                    headers = {'Content-Type': 'text/html; charset=utf-8', 'Connection': 'close'}
                    return [handler.MOCK, 200, headers, content]
                else:
                    path = index_file
            if os.path.isfile(path):
                content_type = 'application/octet-stream'
                try:
                    import mimetypes
                    content_type = mimetypes.types_map.get(os.path.splitext(path)[1])
                except StandardError as e:
                    logging.error('import mimetypes failed: %r', e)
                with open(path, 'rb') as fp:
                    content = fp.read()
                    headers = {'Connection': 'close', 'Content-Type': content_type}
                    return [handler.MOCK, 200, headers, content]


class BlackholeFilter(BaseProxyHandlerFilter):
    """blackhole filter"""
    one_pixel_gif = 'GIF89a\x01\x00\x01\x00\x80\xff\x00\xc0\xc0\xc0\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'

    def filter(self, handler):
        if handler.command == 'CONNECT':
            return [handler.STRIP, True, self]
        elif handler.path.startswith(('http://', 'https://')):
            headers = {'Cache-Control': 'max-age=86400',
                       'Expires': 'Oct, 01 Aug 2100 00:00:00 GMT',
                       'Connection': 'close'}
            content = ''
            if urlparse.urlsplit(handler.path).path.lower().endswith(('.jpg', '.gif', '.png','.jpeg', '.bmp')):
                headers['Content-Type'] = 'image/gif'
                content = self.one_pixel_gif
            return [handler.MOCK, 200, headers, content]
        else:
            return [handler.MOCK, 404, {'Connection': 'close'}, '']


class PACProxyHandler(SimpleProxyHandler):
    """pac proxy handler"""
    handler_filters = [PacFileFilter(), StaticFileFilter(), BlackholeFilter()]


def get_process_list():
    import ctypes
    import collections
    Process = collections.namedtuple('Process', 'pid name exe')
    process_list = []
    if os.name == 'nt':
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        lpidProcess = (ctypes.c_ulong * 1024)()
        cb = ctypes.sizeof(lpidProcess)
        cbNeeded = ctypes.c_ulong()
        ctypes.windll.psapi.EnumProcesses(ctypes.byref(lpidProcess), cb, ctypes.byref(cbNeeded))
        nReturned = cbNeeded.value/ctypes.sizeof(ctypes.c_ulong())
        pidProcess = [i for i in lpidProcess][:nReturned]
        has_queryimage = hasattr(ctypes.windll.kernel32, 'QueryFullProcessImageNameA')
        for pid in pidProcess:
            hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, 0, pid)
            if hProcess:
                modname = ctypes.create_string_buffer(2048)
                count = ctypes.c_ulong(ctypes.sizeof(modname))
                if has_queryimage:
                    ctypes.windll.kernel32.QueryFullProcessImageNameA(hProcess, 0, ctypes.byref(modname), ctypes.byref(count))
                else:
                    ctypes.windll.psapi.GetModuleFileNameExA(hProcess, 0, ctypes.byref(modname), ctypes.byref(count))
                exe = modname.value
                name = os.path.basename(exe)
                process_list.append(Process(pid=pid, name=name, exe=exe))
                ctypes.windll.kernel32.CloseHandle(hProcess)
    elif sys.platform.startswith('linux'):
        for filename in glob.glob('/proc/[0-9]*/cmdline'):
            pid = int(filename.split('/')[2])
            exe_link = '/proc/%d/exe' % pid
            if os.path.exists(exe_link):
                exe = os.readlink(exe_link)
                name = os.path.basename(exe)
                process_list.append(Process(pid=pid, name=name, exe=exe))
    else:
        try:
            import psutil
            process_list = psutil.get_process_list()
        except StandardError as e:
            logging.exception('psutil.get_process_list() failed: %r', e)
    return process_list

def pre_start():
    if not OpenSSL:
        logging.warning('python-openssl not found, please install it!')
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
                logging.warning("*NOTE*, Please set [gae]window=2 [gae]keepalive=1")
    if GAEProxyHandler.max_window != common.GAE_WINDOW:
        GAEProxyHandler.max_window = common.GAE_WINDOW
    if common.GAE_KEEPALIVE and common.GAE_MODE == 'https':
        GAEProxyHandler.ssl_connection_keepalive = True
    if common.GAE_PAGESPEED and not common.GAE_OBFUSCATE:
        logging.critical("*NOTE*, [gae]pagespeed=1 requires [gae]obfuscate=1")
        sys.exit(-1)
    if common.GAE_SSLVERSION:
        GAEProxyHandler.ssl_version = getattr(ssl, 'PROTOCOL_%s' % common.GAE_SSLVERSION)
        GAEProxyHandler.openssl_context = SSLConnection.context_builder(common.GAE_SSLVERSION)
    if common.GAE_APPIDS[0] == 'goagent':
        logging.critical('please edit %s to add your appid to [gae] !', common.CONFIG_FILENAME)
        sys.exit(-1)
    if common.GAE_MODE == 'http' and common.GAE_PASSWORD == '':
        logging.critical('to enable http mode, you should set %r [gae]password = <your_pass> and [gae]options = rc4', common.CONFIG_FILENAME)
        sys.exit(-1)
    if common.GAE_TRANSPORT:
        GAEProxyHandler.disable_transport_ssl = False
    if common.GAE_REGIONS and not pygeoip:
        logging.critical('to enable [gae]regions mode, you should install pygeoip')
        sys.exit(-1)
    if common.PAC_ENABLE:
        pac_ip = ProxyUtil.get_listen_ip() if common.PAC_IP in ('', '::', '0.0.0.0') else common.PAC_IP
        url = 'http://%s:%d/%s' % (pac_ip, common.PAC_PORT, common.PAC_FILE)
        spawn_later(600, urllib2.build_opener(urllib2.ProxyHandler({})).open, url)
    if not dnslib:
        logging.error('dnslib not found, please put dnslib-0.8.3.egg to %r!', os.path.dirname(os.path.abspath(__file__)))
        sys.exit(-1)
    if not common.DNS_ENABLE:
        if not common.HTTP_DNS:
            common.HTTP_DNS = common.DNS_SERVERS[:]
        for dnsservers_ref in (common.HTTP_DNS, common.DNS_SERVERS):
            any(dnsservers_ref.insert(0, x) for x in [y for y in get_dnsserver_list() if y not in dnsservers_ref])
        AdvancedProxyHandler.dns_servers = common.HTTP_DNS
        AdvancedProxyHandler.dns_blacklist = common.DNS_BLACKLIST
    else:
        AdvancedProxyHandler.dns_servers = common.HTTP_DNS or common.DNS_SERVERS
        AdvancedProxyHandler.dns_blacklist = common.DNS_BLACKLIST
    RangeFetch.threads = common.AUTORANGE_THREADS
    RangeFetch.maxsize = common.AUTORANGE_MAXSIZE
    RangeFetch.bufsize = common.AUTORANGE_BUFSIZE
    RangeFetch.waitsize = common.AUTORANGE_WAITSIZE
    if True:
        GAEProxyHandler.handler_filters.insert(0, AutoRangeFilter())
    if common.GAE_REGIONS:
        GAEProxyHandler.handler_filters.insert(0, DirectRegionFilter(common.GAE_REGIONS))
    if True:
        GAEProxyHandler.handler_filters.insert(0, HostsFilter())
    if True:
        GAEProxyHandler.handler_filters.insert(0, URLRewriteFilter())
    if common.HTTP_FAKEHTTPS:
        GAEProxyHandler.handler_filters.insert(0, FakeHttpsFilter(common.HTTP_FAKEHTTPS, common.HTTP_NOFAKEHTTPS))
        PHPProxyHandler.handler_filters.insert(0, FakeHttpsFilter(common.HTTP_FAKEHTTPS, common.HTTP_NOFAKEHTTPS))
    if common.HTTP_FORCEHTTPS:
        GAEProxyHandler.handler_filters.insert(0, ForceHttpsFilter(common.HTTP_FORCEHTTPS, common.HTTP_NOFORCEHTTPS))
        PHPProxyHandler.handler_filters.insert(0, ForceHttpsFilter(common.HTTP_FORCEHTTPS, common.HTTP_NOFORCEHTTPS))
    if common.HTTP_WITHGAE:
        GAEProxyHandler.handler_filters.insert(0, WithGAEFilter(common.HTTP_WITHGAE))
    if common.USERAGENT_ENABLE:
        GAEProxyHandler.handler_filters.insert(0, UserAgentFilter(common.USERAGENT_STRING))
        PHPProxyHandler.handler_filters.insert(0, UserAgentFilter(common.USERAGENT_STRING))
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
    CertUtil.check_ca()
    sys.stderr.write(common.info())

    uvent_enabled = 'uvent.loop' in sys.modules and isinstance(gevent.get_hub().loop, __import__('uvent').loop.UVLoop)

    if common.PHP_ENABLE:
        host, port = common.PHP_LISTEN.split(':')
        HandlerClass = ((PHPProxyHandler, GreenForwardPHPProxyHandler) if not common.PROXY_ENABLE else (ProxyChainPHPProxyHandler, ProxyChainGreenForwardPHPProxyHandler))[uvent_enabled]
        server = LocalProxyServer((host, int(port)), HandlerClass)
        thread.start_new_thread(server.serve_forever, tuple())

    if common.PAC_ENABLE:
        server = LocalProxyServer((common.PAC_IP, common.PAC_PORT), PACProxyHandler)
        thread.start_new_thread(server.serve_forever, tuple())

    if common.DNS_ENABLE:
        try:
            sys.path += ['.']
            from dnsproxy import DNSServer
            host, port = common.DNS_LISTEN.split(':')
            server = DNSServer((host, int(port)), dns_servers=common.DNS_SERVERS, dns_blacklist=common.DNS_BLACKLIST, dns_tcpover=common.DNS_TCPOVER)
            thread.start_new_thread(server.serve_forever, tuple())
        except ImportError:
            logging.exception('GoAgent DNSServer requires dnslib and gevent 1.0')
            sys.exit(-1)

    HandlerClass = ((GAEProxyHandler, GreenForwardGAEProxyHandler) if not common.PROXY_ENABLE else (ProxyChainGAEProxyHandler, ProxyChainGreenForwardGAEProxyHandler))[uvent_enabled]
    server = LocalProxyServer((common.LISTEN_IP, common.LISTEN_PORT), HandlerClass)
    try:
        server.serve_forever()
    except SystemError as e:
        if '(libev) select: ' in repr(e):
            logging.error('PLEASE START GOAGENT BY uvent.bat')
            sys.exit(-1)

if __name__ == '__main__':
    main()
