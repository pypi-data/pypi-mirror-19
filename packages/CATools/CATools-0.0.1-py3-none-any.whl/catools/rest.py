import urllib
import requests
from requests.auth import HTTPBasicAuth
from xml.etree import ElementTree as ET


def sdm_login(host, userid, password, port=8050, timeout=30):
    base_url = "http://{}:{}/caisd-rest/".format(host, port)
    login_url = base_url + "rest_access"
    data = "<rest_access/>"
    r = requests.post(login_url, auth=HTTPBasicAuth(userid, password), data=data, timeout=timeout)
    root = ET.fromstring(r.content)
    headers = {"x-AccessKey": root.attrib['COMMON_NAME'], "x-Obj-Attrs": ""}
    access_data = {'url': base_url, 'headers': headers, 'ctype': 'application/xml; charset=UTF-8'}
    return access_data

def sdm_logout(access_dict):
    access_key = access_dict['headers']['x-accesskey']
    return requests.delete(access_dict['url'] + "/{}".format(access_key), headers=access_dict['headers'])

def search_sdm(access_dict, obj_name, query, return_attributes=""):
    url = "{}{}?WC={}".format(access_dict['url'], obj_name, urllib.request.quote(query))
    print(url)
    headers = access_dict['headers']
    headers['x-obj-attrs'] = return_attributes
    response = requests.get(url, headers=headers)
    return response


def get_object(access_dict, obj_url, return_attributes=""):
    headers = access_dict['headers']
    headers['x-obj-attrs'] = return_attributes
    response = requests.get(obj_url, headers=headers)
    return response


def remove_object(access_dict, obj_url, return_attributes=""):
    headers = access_dict['headers']
    headers['x-obj-attrs'] = return_attributes
    response = requests.delete(obj_url, headers=headers)
    return response

