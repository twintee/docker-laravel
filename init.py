#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from os.path import join, dirname, abspath, isfile, isdir


from dotenv import load_dotenv

dir_scr = os.path.abspath(os.path.dirname(__file__))
import helper as fn

os.chdir(dir_scr)
file_env = os.path.join(dir_scr, ".env")

def main():
    """
    initialize container
    """

    params = fn.getenv(file_env)

    # コンテナ削除
    for line in fn.cmdlines(_cmd="docker-compose down"):
        sys.stdout.write(line)

    # ログリセット
    dir_log = join(dir_scr, "log")
    if isdir(dir_log):
        _input = input("remove logs. ok? (y/*) :").lower()
        if _input in ["y", "yes"]:
            # ボリューム削除
            print("[info] reset log volume.")
            shutil.rmtree(dir_log)

    # ソースリセット
    dir_src = join(dir_scr, "src")
    if isdir(dir_src):
        _input = input("remove app. ok? (y/*) :").lower()
        if _input in ["y", "yes"]:
            # ボリューム削除
            print("[info] reset app volume.")
            shutil.rmtree(dir_src)

    # コンテナ作成
    for line in fn.cmdlines(_cmd=f"docker-compose up -d"):
        sys.stdout.write(line)

    docker_exec = "docker exec -it app-php"

    dir_app = join(dir_src, params['APP_NAME'])
    if not isdir(dir_app):
        if params['GIT_REPO'] == "":
            cmd = f"{docker_exec} composer create-project --prefer-dist laravel/laravel={params['LARAVEL_VER']} {params['APP_NAME']}"
            for line in fn.cmdlines(_cmd=cmd):
                sys.stdout.write(line)
        else:
            # gitからリポジトリクローン
            gituser = params['GIT_USER']
            netrc_path = join(dir_scr, "php", ".netrc")
            if isfile(netrc_path):
                cmd = f"docker cp {netrc_path} app-php:/root"
                for line in fn.cmdlines(_cmd=cmd):
                    sys.stdout.write(line)
            if "gitlab" in params['GIT_REPO']:
                print("[info] clone from gitlab.")
                gituser = "oauth2"
            clone_url = params['GIT_REPO'].replace("://", f"://{gituser}:{params['GIT_TOKEN']}@")
            cmd = f"{docker_exec} git clone {clone_url} {params['APP_NAME']}"
            if params['GIT_BRANCH'] != "":
                cmd = f"{docker_exec} git clone -b {params['GIT_BRANCH']} {clone_url} {params['APP_NAME']}"
            for line in fn.cmdlines(_cmd=cmd):
                sys.stdout.write(line)

    # パーミッション
    for line in fn.cmdlines(_cmd=f"{docker_exec} chmod -R 777 {params['APP_NAME']}/storage/framework"):
        sys.stdout.write(line)

    # composer load
    print(f"""[info] execute composer dump-autoload.
----------
{docker_exec} bash
cd /var/www/html/{params['APP_NAME']}
composer dump-autoload
----------""")

if __name__ == "__main__":

    _input = input("initialize container. ok? (y/*) :").lower()
    if not _input in ["y", "yes"]:
        print("[info] initialize canceled.")
        sys.exit()

    print("[info] initialize start.")
    main()
    print("[info] initialize end.")
