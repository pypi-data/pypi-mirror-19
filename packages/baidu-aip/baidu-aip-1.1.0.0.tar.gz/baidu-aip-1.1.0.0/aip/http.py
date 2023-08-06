# -*- coding: utf-8 -*-

"""
    http.get http.post
"""

import socket
import urllib
import urllib2

# timeout 60s
socket.setdefaulttimeout(60)

def get(url, params=None, headers=None):
    """
        HTTP GET
    """
    
    params = params or {}
    headers = headers or {}

    if params:
        url = url + (url.find('?') == -1 and '?' or '&') + urllib.urlencode(params)
    
    headers['User-Agent'] = 'baidu-aip-python-sdk-1.0.0.0'
    request =  urllib2.Request(url=url, headers=headers)
    
    response = urllib2.urlopen(request)
    content = response.read()

    response.close()

    return content

def post(url, data=None, params=None, headers=None):
    """
        HTTP POST
    """

    data = data or {}
    params = params or {}
    headers = headers or {}

    if params:
        url = url + (url.find('?') == -1 and '?' or '&') + urllib.urlencode(params)
    
    headers['User-Agent'] = 'baidu-aip-python-sdk-1.0.0.0'
    data = isinstance(data, str) and data or urllib.urlencode(data)
    request =  urllib2.Request(url=url, data=data, headers=headers)
    
    response = urllib2.urlopen(request)
    content = response.read()
    response.close()

    return content
