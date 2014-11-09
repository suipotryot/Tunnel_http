def proxy_mangle_request(req):
    print(req)

    if not check_user_agent(req):
        return False
    return req

def proxy_mangle_response(res):
    print(res)

    # if not check_server_name(res) \
    #        or not check_ssh_header(res):
    if not check_server_name(res):
        return False
    return res

def check_user_agent(req):
    ua = req.getHeader('User-Agent')[0]

    if ua == '' \
            or 'python' in ua.lower() \
            or 'perl' in ua.lower():
        return False
    return True

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
