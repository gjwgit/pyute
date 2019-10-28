# -*- coding: utf-8 -*-

# Copyright 2019 (c) Graham.Williams@togaware.com
# Licensed under the MIT License.
#
# Script to report populatrity metrics from github.
#
# Top 10 referrers past 14 days
# gitpop referrers microsoft/recommenders
# gitpop all microsoft/recommenders

import sys
import os
import json
import requests
import argparse

exec(open("secrets.py").read()) # token=

# Command line argument identifies the metric and repository as in
# microsoft/nlp.

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'metric',
    help='the metric of interest (all, referrers, paths, views, clones)')

option_parser.add_argument(
    'repos',
    nargs="+",
    help='name of github repository as in microsoft/nlp')

args = option_parser.parse_args()
metric = args.metric
repos = args.repos

headers = None
headers = {'Authorization': 'token ' + token}

if metric == "all":
    metrics = ["referrers", "paths", "views", "clones"]
else:
    metrics = [metric]

for metric in metrics:

    for repo in repos:

        if metric in ["referrers", "paths"]:
            metric = f"traffic/popular/{metric}"
        elif metric in ["views", "clones"]:
            metric = f"traffic/{metric}"

        response = requests.get(f'https://api.github.com/repos/{repo}' +
                                f'/{metric}', headers=headers)
        if response.status_code == 403:
            print("API rate limit exceeded.", file=sys.stderr)
            print(response.json())
            sys.exit(403)

        if response.ok:
            response = response.json()
            if len(response) == 0: break

            if metric == "traffic/popular/referrers":
                for m in response:
                    print(f"{metric},{repo},{m['referrer']}," +
                          f"{m['count']},{m['uniques']}")
            elif metric == "traffic/popular/paths":
                for m in response:
                    print(f"{metric},{repo},{m['path']}," +
                          f"{m['count']},{m['uniques']},{m['title']}")
            elif metric in ["traffic/views", "traffic/clones"]:
                print(f"{metric},{repo},{response['count']}," +
                      f"{response['uniques']}")
