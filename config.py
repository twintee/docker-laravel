#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from os.path import join, dirname, abspath, isfile, isdir
import shutil
import argparse
from urllib.parse import urlparse

dir_scr = dirname(abspath(__file__))
import helper as fn

dir_scr = dirname(abspath(__file__))

def main(_args):
    print("----- redis env setting start.")

    env_org = join(dir_scr, "_org", '.env')
    env_file = join(dir_scr, '.env')
    nconf_org = join(dir_scr, "_org", 'default.conf')
    nconf_dst = join(dir_scr, "nginx", 'default.conf')
    netrc_org = join(dir_scr, "_org", '.netrc')
    netrc_dst = join(dir_scr, "php", '.netrc')

    if _args.reset or not isfile(env_file):
        print("[info] init .env file.")
        shutil.copyfile(env_org, env_file)

    params = fn.getenv(env_file)

    req_keys = [
        'TZ',
        'APP_NAME',
        'APP_DOMAIN',
        'APP_PORT',
        'PORT_INTERNAL',
    ]

    _input = input("get app source from git. ok? (y/*) :").lower()
    if _input in ["y", "yes"]:
        req_keys.append('GIT_USER')
        req_keys.append('GIT_TOKEN')
        req_keys.append('GIT_REPO')
        req_keys.append('GIT_BRANCH')
    else:
        req_keys.append('LARAVEL_VER')
    fn.setparams(params, req_keys)

    fn.setenv(params, env_file)
    fn.update_file(params, nconf_org, "___", nconf_dst)

    if params['GIT_REPO'] != "":
        # URLをパースする
        params['GIT_DOMAIN'] = urlparse(params['GIT_REPO']).netloc.replace("www.", "")
        fn.update_file(params, netrc_org, "___", netrc_dst)

    for k,v in params.items():
        print(f"{k}={v}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='set config files')
    parser.add_argument('--reset', '-r', help="reset files", action="store_true")
    args = parser.parse_args()

    main(args)
