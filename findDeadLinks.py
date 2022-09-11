#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import re
from pathlib import Path
import urllib.request
import urllib.error
import ssl
import json


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
FILE_EXTENSION = ".txt"   # lower case!
URI_REGEX = re.compile(r"https?://[a-zA-Z0-9:%_\+\.~\?&\\/=!-]+")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def isUnreachable(theuri):
    e = False
    try:
        req = urllib.request.Request(theuri, data=None, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, context=ctx) as u:
            if u.getcode() != 200:
                return True
    except urllib.error.URLError as ee:
        return True
    return False


def findbrokenlinks(notebookpath, ignoreFolders):
    links = {}
    for thefile in notebookpath.glob("**/*"):
        relpath = thefile.relative_to(notebookpath)
        skipthis = False

        for rr in ignoreFolders:
            if relpath.is_relative_to(rr):
                skipthis = True
                break
        if skipthis:
            continue

        if thefile.name.lower().endswith(FILE_EXTENSION):
            newFile = True
            with open(thefile, "r", encoding="utf-8") as f:
                for theline in f:
                    all = URI_REGEX.findall(theline)
                    for theuri in all:
                        if theuri not in links:
                            links[theuri] = isUnreachable(theuri=theuri)

                        if links[theuri]:
                            if newFile:
                                print("\n[" + str(relpath) + "]")
                                newFile = False
                            print("    UNREACHABLE: " + theuri)


if __name__ == "__main__":
    argParse = argparse.ArgumentParser()
    argParse.add_argument("--notebookpath", required=True)
    argParse.add_argument("--ignoreFolder", nargs="*", required=False)
    argParse.add_argument("--proxy")
    argParse.add_argument('--noask', required=False, action="store_true", default=False)
    argParse.add_argument('--confirmExit', required=False, action="store_true", default=False)
    args = argParse.parse_args()

    if not args.noask:
        yn = input("\nfind broken links? [y/n] ")
        if yn.strip().lower() != "y":
            exit()

    if args.proxy is not None:
        theproxy = json.loads(args.proxy)
        print("PROXY: " + str(theproxy))
        proxy_support = urllib.request.ProxyHandler(theproxy)
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    ignoreFolder = []
    if args.ignoreFolder is not None:
        for i in args.ignoreFolder:
            ignoreFolder.append(Path(i))

    findbrokenlinks(notebookpath=Path(args.notebookpath), ignoreFolders=ignoreFolder)

    if args.confirmExit:
        yn = input("\npress enter ... ")
