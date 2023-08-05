import requests
import os

def get_token(key, secret):
    if not key or not secret:
        raise Exception("""
        !!! You must pass a Bitbucket consumer key and secret to deploy this application !!!
        """)

    r = requests.post(
            'https://bitbucket.org/site/oauth2/access_token',
            data={'grant_type': 'client_credentials'},
            auth=(key, secret)).json()

    if 'error_description' in r:
        print('\n', r)
        raise Exception('!!! Error found !!!')

    return r['access_token']

def build_url(user, repo, branch, egg, token):
    return 'git+https://x-token-auth:{}@bitbucket.org/{}/{}.git@{}#egg={}'.format(
            token, user, repo, branch, egg)

