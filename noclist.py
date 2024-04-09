import hashlib
import json
import time
import sys
import argparse

import requests

# doc strings?
 # Recommended timeout of a value greater than a multiple of 3 to align with TCP packet transmission retry
def retry_request(http_verb, endpoint, headers = {}, timeout=(3.05, 5)) :

    backoff = [0, 0, 1]
    # Retry logic
    for ind, b in enumerate(backoff):
        time.sleep(b)

        if ind > 0:
            print(f"Retry #{ind}: {http_verb} to {endpoint}",  file=sys.stderr)

        try:
            r = requests.request(http_verb, endpoint, headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r
        except:
            # Normally we shouldn't catch all exceptions but in this case we're handling them all the same way:
            # catch and warn since we're going to retry
            print(f"Exception on request # {ind}", file=sys.stderr)

    # If we get here, we're still getting errors so warn and raise an exception
    print("2nd Retry failed so raising exception",  file=sys.stderr)
    raise requests.RequestException    

def get_auth_token(host):
    try:    
        r = retry_request('HEAD', host + '/auth')
    except requests.RequestException:
        return None

    return r.headers.get('Badsec-Authentication-Token')

def get_user_list(host, auth_token):
    checksum = hashlib.sha256((auth_token + '/users').encode())
    headers= {'X-Request-Checksum': checksum.hexdigest()}

    try:    
        r = retry_request('GET', host + '/users', headers=headers)
    except requests.RequestException:
        return None

    # Parse list into JSON
    user_list = r.text.split('\n')
    try:
        return json.dumps(user_list)
    except TypeError:
        return None

    
def main(args):
    host = args.host

    auth_token = get_auth_token(host)

    if not auth_token:
        print("Could not retrieve auth token", file=sys.stderr)
        sys.exit(1)

    user_list_json = get_user_list(host, auth_token)

    if not user_list_json:
        print( "Could not get user list", file=sys.stderr)
        sys.exit(1)

    print(user_list_json)
    # if we get here we should be all good so exit successfully
    sys.exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Retrieve NOC list')
    parser.add_argument('--host', help='host and port to send request', default="http://0.0.0.0:8888")
    args = parser.parse_args()
    main(args)