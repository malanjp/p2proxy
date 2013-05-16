# -*- coding: utf-8 -*-
from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.python import log
import sys, re
import urlparse
import mechanize
import cookielib
import requests
 
log.startLogging(sys.stdout)

LOGINID = ''
PASSWORD = ''

class P2Browser(object):
    browser = None
    cookiejar = None

    def __init__(self):
        """
        A function to make browser object.
        """
        self.browser = mechanize.Browser()

        # Making Cookie Jar and bind it to browser
        self.cookiejar = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cookiejar)

        # Setting browser options
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                                   max_time=1)
        self.browser.set_debug_http(False) # HTTPのヘッダを表示
        self.browser.addheaders = [('User-agent',
            ('Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3)' ' Gecko/20041001 P2ProxyMac/0.1'))]

    def login(self, loginid='', password=''):
        self.browser.open('http://p2.2ch.net/p2/')
        self.browser.select_form(nr=0)

        # Login
        self.browser.form['form_login_id'] = loginid
        self.browser.form['form_login_pass'] = password
        self.browser.submit()


# プロキシリクエストのクラス
class P2ProxyRequest(proxy.ProxyRequest):
#  protocols = {'http': P2ProxyClientFactory}

  # processメソッドを継承
  def process(self):
    log.msg('>>>> process start...')
    log.msg('>>> args =', self.args)
    parsed = urlparse.urlparse(self.uri)
    protocol = parsed[0]
    host = parsed[1]
    log.msg('>>> method =', self.method)
    log.msg('>>> parsed =', parsed)
    log.msg('>>> host =', host)

    port = self.ports[protocol]
    if ':' in host:
      host, port = host.split(':')
      port = int(port)
      log.msg('>>> host, port =', host, port)

    # 2p.2ch.net 以外の *.2ch.net
    sp = host.split('.')
    if self.method == 'POST' and ((sp[0] != 'p2' and sp[1] == '2ch' and sp[2] == 'net') or
                                  (sp[0] != 'p2' and sp[1] == 'bbspink' and sp[2] == 'com')):
      self.host = host
      self.post_process()

    rest = urlparse.urlunparse(('', '') + parsed[2:])
    if not rest:
      rest = rest + '/'
    class_ = self.protocols[protocol]
    headers = self.getAllHeaders().copy()
    if 'host' not in headers:
      headers['host'] = host
    self.content.seek(0, 0)
    s = self.content.read()

    clientFactory = class_(self.method, rest, self.clientproto, headers, s, self)
    self.reactor.connectTCP(host, port, clientFactory)
    log.msg('>>>> process...done')

  def post_process(self):
    """
    p2.2ch.net 以外の *.2ch.net への書き込み
    """
    log.msg('>>>> post_process...')
    global p2
    if not p2.cookiejar:
      return False

    log.msg('>>> SUBMIT...')
    p2.browser.open('http://p2.2ch.net/p2/post_form.php?host=%s&bbs=%s&key=%s' % (self.host, self.args.get('bbs')[0], self.args.get('key')[0]))
    body = p2.browser.response().read()
    p2.browser.select_form(nr=0)
    p2.browser.form['FROM'] = self.args.get('FROM', [''])[0]
    p2.browser.form['mail'] = self.args.get('mail', [''])[0]
    p2.browser.form['MESSAGE'] = self.args.get('MESSAGE', [''])[0]
    r = p2.browser.submit()
    #log.msg(r.read())
    log.msg('>>> SUBMIT...done')
    log.msg('>>>> post_process...done')



# プロキシクラスを継承
class P2Proxy(proxy.Proxy):
  requestFactory = P2ProxyRequest
  def dataReceived(self, data):
    log.msg('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    log.msg(data)
    log.msg('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
    # perform the default functionality on modified data 
    return proxy.Proxy.dataReceived(self, data)


# HTTPプロキシサーバのクラス
class P2ProxyFactory(http.HTTPFactory):
  protocol = P2Proxy
 

log.msg('>>>> P2Proxy Start...')
log.msg('>>> LOGIN P2 START')
p2 = P2Browser()
log.msg('>>> P2 Browser Initializing...')
try:
  p2.login(loginid=LOGINID, password=PASSWORD)
  log.msg('>>> P2 Browser Initializing...done')
except Exception as e:
  log.msg('>>> ============================')
  log.msg('>>> ERROR!', e)
  log.msg('>>> ============================')

# 実行
reactor.listenTCP(8081, P2ProxyFactory())
reactor.run()

log.msg('>>>> P2Proxy...done')



