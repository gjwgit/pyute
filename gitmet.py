# -*- coding: utf-8 -*-

# Copyright 2019 (c) Graham.Williams@microsoft.com
# Licensed under the MIT License.
#
# Script to calculate metrics, separating internal (Microsoft) and
# external.

import sys
import os
import json
import requests
import argparse

# Command line argument identifies the metrix and the repositories as
# in microsoft/nlp.

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'metric',
    help='the metric of interest (issues, pulls, clones)')

option_parser.add_argument(
    'repos',
    nargs="+",
    help='name of github repository as in microsoft/nlp')

args = option_parser.parse_args()
metric = args.metric
repos = args.repos

# Without a header you have a very limited number of REST calls per
# hour (30). With an authorization token you get more.

headers = None
token = 'XXXX'
headers = {'Authorization': 'token ' + token}

# Cached list of known Microsoft users raising issues for one of a set
# of repositoris of interest as generated from orgs.py, rather than
# using multiple REST calls here. Just copy and paste the output of
# orgs.py here.

msdevs = [XXXX]

for repo in repos:
    
    # Obtain all pull requests.

    metrics = {}
    i = 1

    while True:
        response = requests.get(f'https://api.github.com/repos/{repo}' +
                                f'/{metric}?state=all&page={str(i)}' +
                                f'&per_page=100', headers=headers)
        if response.status_code == 403:
            print("API rate limit exceeded.", file=sys.stderr)
            sys.exit(403)
        response = response.json()
        if len(response) == 0: break
        metrics = metrics + response if len(metrics) > 0 else response
        i += 1

    external = internal = 0

    for m in metrics:
        if metric in ('issues', 'pulls'):
            login = m['user']['login']
        elif metric in ('forks'):
            login = m['owner']['login']
        elif metric in ('subscribers', 'stargazers'):
            login = m['login']
        else:
            login = m['login']
            
        if login in msdevs:
            internal += 1
        else:
            external += 1

    print(f"{metric},{repo},{len(metrics)},{internal},{external}," +
          f"{round(100*external/(internal+external))}")
