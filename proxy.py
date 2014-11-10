def proxy_mangle_request(req):
    print(req)

    if not check_user_agent(req) \
            or not check_404(req):
        return False
    return req

def proxy_mangle_response(res):
    print(res)

    if not check_server_name(res) \
           or not check_ssh_header(res):
        return False
    return res

def check_user_agent(req):
    ua = req.getHeader('User-Agent')[0]

    if ua == '' \
            or 'python' in ua.lower() \
            or 'perl' in ua.lower():
        return False
    return True

def check_404(req):
    import urllib2
    url = req.getHost()

    if url[1] == 80:
        if '192' in url[0]:
            url = 'http://' + url[0] + "/azhkjdhvpoiu134124EZfgsdf23134lkfsdjfh34354342.html"
        else:
            url = 'http://www.' + url[0] + "/azhkjdhvpoiu134124EZfgsdf23134lkfsdjfh34354342.html"
    else:
        return

    if '192' in url:
        opener = urllib2.build_opener()
    else:
        proxy_handler = urllib2.ProxyHandler({'http': 'cacheserv3.univ-lille1.fr:3128'})
        opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    print('request the host: %s' % url)
    req = urllib2.Request(url)
    req.add_header('User-agent', 'Mozilla/5.0')

    try:
        f = urllib2.urlopen(req, timeout=2)
        print('HTTP return code: %d' % f.getcode())
        print(f.info().get('Server'))
    except urllib2.URLError, e:
        print(e)
        if '404' in e.__str__():
            return True
    return False

def check_server_name(res):
    list_server_name = res.getHeader('Server')

    # TODO: use a whitelist
    for server_name in list_server_name:
        if server_name == '' \
                or 'python' in server_name.lower() \
                or 'perl' in server_name.lower():
            return False
    return True

def check_ssh_header(res):
    import base64

    body = base64.b64decode(res.body)
    if 'OpenSSH_' in body:
        return False
    return True
