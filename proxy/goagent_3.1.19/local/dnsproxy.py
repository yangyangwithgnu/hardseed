#!/usr/bin/env python
# coding:utf-8

__version__ = '1.0'

import sys
import os
import glob

sys.path += glob.glob('*.egg')

import gevent
import gevent.server
import gevent.timeout
import gevent.monkey
gevent.monkey.patch_all(subprocess=True)

import re
import time
import logging
import heapq
import socket
import select
import struct
import errno
import thread
import dnslib
import Queue
try:
    import pygeoip
except ImportError:
    pygeoip = None


is_local_addr = re.compile(r'(?i)(?:[0-9a-f:]+0:5efe:)?(?:127(?:\.\d+){3}|10(?:\.\d+){3}|192\.168(?:\.\d+){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d+){2})').match


def get_dnsserver_list():
    if os.name == 'nt':
        import ctypes, ctypes.wintypes, struct, socket
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


def parse_hostport(host, default_port=80):
    m = re.match(r'(.+)[#](\d+)$', host)
    if m:
        return m.group(1).strip('[]'), int(m.group(2))
    else:
        return host.strip('[]'), default_port


class ExpireCache(object):
    """ A dictionary-like object, supporting expire semantics."""
    def __init__(self, max_size=1024):
        self.__maxsize = max_size
        self.__values = {}
        self.__expire_times = {}
        self.__expire_heap = []

    def size(self):
        return len(self.__values)

    def clear(self):
        self.__values.clear()
        self.__expire_times.clear()
        del self.__expire_heap[:]

    def exists(self, key):
        return key in self.__values

    def set(self, key, value, expire):
        try:
            et = self.__expire_times[key]
            pos = self.__expire_heap.index((et, key))
            del self.__expire_heap[pos]
            if pos < len(self.__expire_heap):
                heapq._siftup(self.__expire_heap, pos)
        except KeyError:
            pass
        et = int(time.time() + expire)
        self.__expire_times[key] = et
        heapq.heappush(self.__expire_heap, (et, key))
        self.__values[key] = value
        self.cleanup()

    def get(self, key):
        et = self.__expire_times[key]
        if et < time.time():
            self.cleanup()
            raise KeyError(key)
        return self.__values[key]

    def delete(self, key):
        et = self.__expire_times.pop(key)
        pos = self.__expire_heap.index((et, key))
        del self.__expire_heap[pos]
        if pos < len(self.__expire_heap):
            heapq._siftup(self.__expire_heap, pos)
        del self.__values[key]

    def cleanup(self):
        t = int(time.time())
        eh = self.__expire_heap
        ets = self.__expire_times
        v = self.__values
        size = self.__maxsize
        heappop = heapq.heappop
        #Delete expired, ticky
        while eh and eh[0][0] <= t or len(v) > size:
            _, key = heappop(eh)
            del v[key], ets[key]


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


class DNSServer(gevent.server.DatagramServer):
    """DNS Proxy based on gevent/dnslib"""

    def __init__(self, *args, **kwargs):
        dns_blacklist = kwargs.pop('dns_blacklist')
        dns_servers = kwargs.pop('dns_servers')
        dns_tcpover = kwargs.pop('dns_tcpover', [])
        dns_timeout = kwargs.pop('dns_timeout', 2)
        super(self.__class__, self).__init__(*args, **kwargs)
        self.dns_servers = list(dns_servers)
        self.dns_tcpover = tuple(dns_tcpover)
        self.dns_intranet_servers = [x for x in self.dns_servers if is_local_addr(x)]
        self.dns_blacklist = set(dns_blacklist)
        self.dns_timeout = int(dns_timeout)
        self.dns_cache = ExpireCache(max_size=65536)
        self.dns_trust_servers = set(['8.8.8.8', '8.8.4.4', '2001:4860:4860::8888', '2001:4860:4860::8844'])
        if pygeoip:
            for dirname in ('.', '/usr/share/GeoIP/', '/usr/local/share/GeoIP/'):
                filename = os.path.join(dirname, 'GeoIP.dat')
                if os.path.isfile(filename):
                    geoip = pygeoip.GeoIP(filename)
                    for dnsserver in self.dns_servers:
                        if ':' not in dnsserver and geoip.country_name_by_addr(parse_hostport(dnsserver, 53)[0]) not in ('China',):
                            self.dns_trust_servers.add(dnsserver)
                    break

    def do_read(self):
        try:
            return gevent.server.DatagramServer.do_read(self)
        except socket.error as e:
            if e[0] not in (errno.ECONNABORTED, errno.ECONNRESET, errno.EPIPE):
                raise

    def get_reply_record(self, data):
        request = dnslib.DNSRecord.parse(data)
        qname = str(request.q.qname).lower()
        qtype = request.q.qtype
        dnsservers = self.dns_servers
        if qname.endswith('.in-addr.arpa'):
            ipaddr = '.'.join(reversed(qname[:-13].split('.')))
            record = dnslib.DNSRecord(header=dnslib.DNSHeader(id=request.header.id, qr=1,aa=1,ra=1), a=dnslib.RR(qname, rdata=dnslib.A(ipaddr)))
            return record
        if 'USERDNSDOMAIN' in os.environ:
            user_dnsdomain = '.' + os.environ['USERDNSDOMAIN'].lower()
            if qname.endswith(user_dnsdomain):
                qname = qname[:-len(user_dnsdomain)]
                if '.' not in qname:
                    if not self.dns_intranet_servers:
                        logging.warning('qname=%r is a plain hostname, need intranet dns server!!!', qname)
                        return dnslib.DNSRecord(header=dnslib.DNSHeader(id=request.header.id, rcode=3))
                    qname += user_dnsdomain
                    dnsservers = self.dns_intranet_servers
        try:
            return self.dns_cache.get((qname, qtype))
        except KeyError:
            pass
        try:
            dns_resolve = dnslib_resolve_over_tcp if qname.endswith(self.dns_tcpover) else dnslib_resolve_over_udp
            kwargs = {'blacklist': self.dns_blacklist, 'turstservers': self.dns_trust_servers}
            record = dns_resolve(request, dnsservers, self.dns_timeout, **kwargs)
            ttl = max(x.ttl for x in record.rr) if record.rr else 600
            self.dns_cache.set((qname, qtype), record, ttl * 2)
            return record
        except socket.gaierror as e:
            logging.warning('resolve %r failed: %r', qname, e)
            return dnslib.DNSRecord(header=dnslib.DNSHeader(id=request.header.id, rcode=3))

    def handle(self, data, address):
        logging.debug('receive from %r data=%r', address, data)
        record = self.get_reply_record(data)
        return self.sendto(data[:2] + record.pack()[2:], address)


def test():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(asctime)s %(message)s', datefmt='[%b %d %H:%M:%S]')
    dns_servers = ['114.114.114.114', '114.114.115.115', '8.8.8.8', '8.8.4.4']
    dns_blacklist = '1.1.1.1|255.255.255.255|74.125.127.102|74.125.155.102|74.125.39.102|74.125.39.113|209.85.229.138|4.36.66.178|8.7.198.45|37.61.54.158|46.82.174.68|59.24.3.173|64.33.88.161|64.33.99.47|64.66.163.251|65.104.202.252|65.160.219.113|66.45.252.237|72.14.205.104|72.14.205.99|78.16.49.15|93.46.8.89|128.121.126.139|159.106.121.75|169.132.13.103|192.67.198.6|202.106.1.2|202.181.7.85|203.161.230.171|203.98.7.65|207.12.88.98|208.56.31.43|209.145.54.50|209.220.30.174|209.36.73.33|209.85.229.138|211.94.66.147|213.169.251.35|216.221.188.182|216.234.179.13|243.185.187.3|243.185.187.39'.split('|')
    dns_tcpover = ['.youtube.com', '.googlevideo.com']
    logging.info('serving at port 53...')
    DNSServer(('', 53), dns_servers=dns_servers, dns_blacklist=dns_blacklist, dns_tcpover=dns_tcpover).serve_forever()


if __name__ == '__main__':
    test()
