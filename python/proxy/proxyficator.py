import urlparse
import requests
import socks
import socket
import sys
import re
import logging


class proxyficator:
    def __init__(self, proxy_url="socks5://localhost:8085"):
        self.log = logging.getLogger("proxyficator")
        self.initialize_socks(proxy_url)

    def initialize_socks(self, socks_uri):
        #Needs to be upgraded to accept proxy username y password    
        uri_parse = urlparse.urlparse(socks_uri)
        if not ( uri_parse.scheme and uri_parse.hostname and uri_parse.port):
            self.log.error("Cannot determine proxy server. Exiting...")
            sys.exit()

        protocol_types = {'socks5':socks.PROXY_TYPE_SOCKS5, 'socks4':socks.PROXY_TYPE_SOCKS4, 'http':socks.PROXY_TYPE_HTTP}

        self.real_ip = self.get_ip()
        if not self.real_ip:
            self.log.error("Cannot get real ip, exiting...")
            sys.exit()

        #Socket override by socks
        socks.setdefaultproxy(protocol_types[uri_parse.scheme.lower()], uri_parse.hostname, int(uri_parse.port), True, uri_parse.username, uri_parse.password)
        socket.socket = socks.socksocket
        #Remote DNS proxy fix
        def getaddrinfo(*args):
            return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
        socket.getaddrinfo = getaddrinfo
        self.proxyfied_ip = self.get_ip()

        #Checking that the proxy works fine
        if not self.proxyfied_ip:
            self.log.error("Cannot get proxified ip, exiting...")
            sys.exit()
        if self.real_ip == self.proxyfied_ip:
            self.log.error("Real ip and proxified ip are the same, exiting...")
            sys.exit()
        self.log.info("Proxy configured successfully. Real IP '{}' - Proxy IP '{}'".format(self.real_ip,self.proxyfied_ip))

    def get_ip(self):
        socket_errors = requests_errors = proxy_errors = 0
        services = ["http://checkip.amazonaws.com/", "http://ipv4.icanhazip.com"]
        for service in services:
            try:
                r = requests.get(service)
                if r.status_code == 200:
                    ip_reg = re.match("^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$",r.text)
                    if ip_reg and len(ip_reg.groups()) == 1:
                        return ip_reg.group(0)
                requests_errors += 1
            except requests.exceptions.RequestException as msg:
                requests_errors += 1
            except socket.error as msg:
                socket_errors += 1
            except socks.GeneralProxyError as msg:
                socket_errors += 1
            except socks.ProxyConnectionError as msg:
                proxy_errors += 1
        if socket_errors == len(services):
            self.log.error("ERROR with sockets")
        elif requests_errors == len(services):
            self.log.error("No service alive")
        elif proxy_errors == len(services):
            self.log.error("ERROR with proxy")
        else:
            self.log.error("Cannot get IP by unknown error")
        return None

