import json
import requests

# Script to identify Microsoft devs amongst those raising issues
# within the best practice repositories.

# Using authentication
        
token = 'XXXX'
headers = {'Authorization': 'token ' + token}

# List all users from the three repos

issues = {}

for repo in ['microsoft/nlp', 'microsoft/computervision', 'microsoft/recommenders']:
    print(repo)
    i = 1
    while True:
        response = requests.get('https://api.github.com/repos/' + repo + '/issues?state=all&page=' + str(i) + '&per_page=100').json()
        if len(response) == 0: break
        if len(issues) == 0:
            issues = response
        else:
            issues = issues + response
        print(i, len(response), len(issues))
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

for u in users:
    if requests.get('https://api.github.com/orgs/microsoft/members/' + u, headers=headers).status_code == 204:
        internal += [u]
    elif requests.get('https://api.github.com/orgs/azure/members/' + u, headers=headers).status_code == 204:
        internal += [u]
    else:
        external += [u]

# Print list of users in microsoft

print("Microsoft internal devs are:")
print(internal)

print(f"There are {len(internal)} internal devs raising issues.")
print(f"There are {len(external)} other devs raising issues.")
