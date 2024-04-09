import hashlib
import json
import time
import sys
import argparse

import requests


def retry_request(http_verb, endpoint, headers = {}, timeout=(3.05, 5)) :
    """
    A wrapper for a Python requests calls with retry logic. This function will attempt a
    maximum of 3 calls before raising an exception.  The delay between the calls will be 
    0s, 0s and 1s to recreate the beginning pattern of an exponential backoff between retries.
    This will raise an exception if both the retries fail.

    The default timeout settings are 3.05s for the connect timeout and 5s for a read timeout
    From the requests documentation: It’s a good practice to set connect timeouts to slightly larger
    than a multiple of 3, which is the default TCP packet retransmission window. 
    (Source: https://requests.readthedocs.io/en/latest/user/advanced/#timeouts)
    """

    backoff = [0, 0, 1]
    for ind, b in enumerate(backoff):
        time.sleep(b)

        if ind > 0:
            print(f"Retry #{ind}: {http_verb} to {endpoint}",  file=sys.stderr)

        try:
            r = requests.request(http_verb, endpoint, headers=headers, timeout=timeout)
            if r.status_code == 200:
                return r
        except requests.RequestException:
            # Normally we should probably be more specific about exceptions but 
            # in this case we're handling them all the same way:
            # catch and warn since we're going to retry
            # Some of the cases we hope to handle:
            # - error responses (all responses with non 200 status codes)
            # - timeouts
            # - dropped connections
            print(f"Exception on request # {ind}", file=sys.stderr)

    # If we get here, we're still getting errors so warn and raise an exception
    print("2nd Retry failed so raising exception",  file=sys.stderr)

    # TODO: create our own exception because this one is coming from us and not
    # the requests library
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

    # Parse list and convert to JSON
    user_list = r.text.split('\n')
    try:
        return json.dumps(user_list)
    except TypeError:
        return None

    
def main(args):
    host = args.host

    auth_token = get_auth_token(host)

    if not auth_token:
        print("Could not retrieve auth token.", file=sys.stderr)
        sys.exit(1)

    user_list_json = get_user_list(host, auth_token)

    if not user_list_json:
        print( "Could not get user list.", file=sys.stderr)
        sys.exit(1)

    print(user_list_json)
    # if we get here we should be all good so exit successfully
    sys.exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Retrieve NOC list')
    parser.add_argument('--host', help='server host and port', default="http://0.0.0.0:8888")
    args = parser.parse_args()
    main(args)