# -*- coding: utf-8 -*-

# Copyright 2019 (c) Graham.Williams@togaware.com
# Licensed under the MIT License.
#
# Script to calculate metrics, separating internal (Microsoft) and
# external.

import sys
import os
import json
import requests
import argparse

exec(open("secrets.py").read()) # token= and devs=

# Command line argument identifies the metric and the repositories as
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
headers = {'Authorization': 'token ' + token}

# The secrets file also includes the list of devs that are regarded as
# internal devs. All other devs are thus external devs. Cached list of
# known devs raising issues for one of a set of repositoris of
# interest as generated from orgs.py, rather than using multiple REST
# calls here. The list is built from the output of orgs.py here.

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
        if response.ok:
            response = response.json()
            if len(response) == 0: break
            metrics = metrics + response if len(metrics) > 0 else response
            i += 1
            
#    print(json.dumps(metrics, indent=2))
    
    external = internal = 0

    # NOTE - issue with counting recursive forks.....
    
    for m in metrics:
        subforks = 0
        if metric in ('issues', 'pulls'):
            login = m['user']['login']
        elif metric in ('forks'):
            login = m['owner']['login']
            subforks = m['forks_count']
            print(subforks)
        elif metric in ('subscribers', 'stargazers'):
            login = m['login']
        else:
            login = m['login']
            
        if login in devs:
            internal += 1
        else:
            external += 1 + subforks

    print(f"{metric},{repo},{internal+external},{internal},{external},{round(100*external/(internal+external))}")
