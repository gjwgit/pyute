import json
import requests
import argparse

# Script to calculate metrics for who are raising issues and pull
# requests.

# Command line argument identifies the repository as in microsoft/nlp.

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'repo',
    help='name of github repository as in microsoft/nlp')

args = option_parser.parse_args()
repo = args.repo

# Cached list of known Microsoft users as generated from orgs.py.

msdevs = [XXXX]

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

# print(json.dumps(issues, indent=4))

external = internal = 0

for i in issues:
    login = i['user']['login']

    if login in msdevs:
        internal += 1
    else:
        external += 1

print(repo, internal, external)
