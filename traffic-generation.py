#!/usr/bin/python3

import urllib.error
import urllib.request
import sys

urls = [
    'http://github.com',
    'http://www.facebook.com',
    'http://www.exploit-db.com'
]

if __name__ == '__main__':
    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print('usage: python %s [proxy_host proxy_port]' % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) == 3:
        proxy_host = sys.argv[1]
        proxy_port = sys.argv[2]
        proxy_handler = urllib.request.ProxyHandler({'http': proxy_host + ':' + proxy_port})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0')
    ]

    while True:
        for url in urls:
            print('request the host: %s' % url)
            try:
                f = opener.open(url, timeout=2)
                print('HTTP status code: %d' % f.getcode())
            except urllib.error.URLError:
                print('There was an error when you request %s url' % url)
            except KeyboardInterrupt:
                sys.exit(0)
