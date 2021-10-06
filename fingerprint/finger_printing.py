#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import traceback
import os
import json
from bs4 import BeautifulSoup
import mmh3
import codecs

from .favicon_fingerprint import favinger

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class finger_print:

    def whatisapp(self, url):
        req = requests.get(url, verify=False, timeout=10)
        if req.status_code in [403, 401] and "WWW-Authenticate" in req.headers:
            print(" [i] Basic authentification")
            return "basic_auth"
        else:
            return "web"


    def cms_check(self, url, second_test=False):
        if second_test:
            url_base = url.split("/")[2] if len(url.split("/")) < 5 else "{}".format("_".join(url.split("/")[2:-1]))
        else:
            url_base = "".join(url.split("/")[1:3])
        if not os.path.exists("fingerprint/CMSeeK/Result/{}/cms.json".format(url)):
            try:
                os.system('python3 fingerprint/CMSeeK/cmseek.py -u {} -o --follow-redirect >/dev/null'.format(url_base))
            except Exception:
                traceback.print_exc() #DEBUG
                pass
        with open("fingerprint/CMSeeK/Result/{}/cms.json".format(url_base)) as result:
            data = json.load(result)
            if data["cms_name"] != "":
                return data["cms_name"]
            else:
                if not second_test:
                    self.cms_check(url, second_test=True)
                else:
                    return False


    def other_check(self, url):
        print(" [i] Search technologie")

        techno_found = False

        domain = "/".join(url.split("/")[:3])
        url_fav =  "{}favicon.ico".format(domain) if domain[-1] == "/" else "{}/favicon.ico".format(domain)
        req = requests.get(url_fav, verify=False, timeout=10, allow_redirects=True)
        if req.status_code == 200:
            fav_found = False
            favicon = codecs.encode(req.content,"base64")
            hash_fav = mmh3.hash(favicon)
            for fg in favinger:
                if hash_fav == fg:
                    techno_found = True
                    print("  \u251c {} found".format(favinger[fg]))
                    return favinger[fg]
            if not techno_found:
                print("\t\u251c [i] Favicon.ico hash: {}".format(hash_fav))
                username_input = False
                password_input = False
                default_input = ["username:password", "usr:pwd", "user:pass"]
                print("\t\u251c [i] Search input")
                #TODO search input with a percentage
                soup = BeautifulSoup(req.text, "html.parser")
                for p in soup.find_all('input'):
                    for di in default_input:
                        if di.split(":")[0] == p["name"]:
                            print(" - input user found: {}".format(p["name"]))
                            username_input = p["name"]
                        if di.split(":")[1] == p["name"]:
                            print(" - input password found: {}".format(p["name"]))
                            password_input = p["name"]
                if username_input and password_input:
                    return username_input, password_input

