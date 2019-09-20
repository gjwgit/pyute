# -*- coding: utf-8 -*-

# Copyright 2019 (c) Graham.Williams@togaware.com
# Licensed under the MIT License.
#
# Script to identify Microsoft devs amongst those raising issues
# within the best practice repositories.

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

# Use authentication.  For information on generating a token see
# https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/
        
token = 'XXXX'
headers = {'Authorization': 'token ' + token}

# List all users from the three repos

issues = {}

for repo in repos:
    i = 1
    while True:
        response = requests.get(f'https://api.github.com/repos/{repo}' +
                                f'/issues?state=all&page={str(i)}' +
                                f'&per_page=100').json()
        if len(response) == 0: break
        if len(issues) == 0:
            issues = response
        else:
            issues = issues + response
        i += 1    

# Obtain a unique list of all user logins.

users = []

for i in issues:
    user = i['user']['login']
    if not user in users:
        users += [user]
    
len(users)

# Keep those in microsoft in the list

internal = []
external = []

# Not particularly robust in the case of having gone over the github
# API call limit which returns status code 404.

for u in users:
    if requests.get(f'https://api.github.com/orgs/microsoft/members/{u}', headers=headers).status_code == 204:
        internal += [u]
    elif requests.get(f'https://api.github.com/orgs/azure/members/{u}', headers=headers).status_code == 204:
        internal += [u]
    else:
        external += [u]

# Print the Microsoft devs in a form that can be pasted into
# issues.py, for example.

print(f"Microsoft devs ({len(internal)}):")
print(internal)
print("")
print(f"Non-Microsoft devs ({len(external)}):")
print(external)
