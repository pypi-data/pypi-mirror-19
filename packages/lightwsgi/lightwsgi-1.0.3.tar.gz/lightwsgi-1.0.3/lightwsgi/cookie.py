import time
from Cookie import SimpleCookie

def cookieExpiryFormat(epochtime):
    return time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(epochtime))

def getCookieDict(environ):
    if "HTTP_COOKIE" in environ:
        cookies = {}
        for key, morsel in SimpleCookie(environ["HTTP_COOKIE"]).items():
            cookies[key] = morsel.value
        return cookies
    else:
        return {}

def cookieError(name, value):
    return {"name": name, "value": value, "expires": time.time() + 10}
