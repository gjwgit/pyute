# -*- coding: utf-8 -*-

# Copyright 2019 (c) Graham.Williams@togaware.com
# Licensed under the MIT License.
#
# Script to calculate metrics for who are raising issues and pull
# requests.

import json
import requests
import argparse

# Command line argument identifies the repository as in microsoft/nlp.

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'repos',
    nargs="+",
    help='name of github repository as in microsoft/nlp')

args = option_parser.parse_args()
repos = args.repos

# Cached list of known Microsoft users raising issues for one of a set
# of repositoris of interest as generated from orgs.py, rather than
# using multiple REST calls here. Just copy and paste the output of
# orgs.py here.

msdevs = [XXXX]

for repo in repos:
    
    # Obtain all issues and pull requests.

    issues = {}
    i = 1

    while True:
        response = requests.get('https://api.github.com/repos/' + repo + '/issues?state=all&page=' + str(i) + '&per_page=100').json()
        if len(response) == 0: break
        if len(issues) == 0:
            issues = response
        else:
            issues = issues + response
        i += 1    

    external = internal = 0

    for i in issues:
        login = i['user']['login']

        if login in msdevs:
            internal += 1
        else:
            external += 1

    print(f"{repo},{internal},{external}")
