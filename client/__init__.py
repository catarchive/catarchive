#!/usr/bin/env python3

import os
import sys
import argparse

try:
    from . import client
    from . import network
except ImportError:
    import client
    import network

def main():
    """Starts the crawler."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint', type=str, help='The host:port of the server to connect to, e.g. "x.x.x.x:x", or "example.com:x"', default='')
    parser.add_argument('-t', '--token', type=str, help='The authentication token of the server to connect to, or set the CAT_ARCHIVE_TOKEN environment variable', default='')
    args = parser.parse_args()

    e = args.endpoint.split(':')
    if len(e) < 2 or (len(e) > 1 and not e[1].isdigit()):
        print('CA: Error: Invalid endpoint', file=sys.stderr)
        exit(1)

    if args.token == '':
        if (cat := os.environ.get('CAT_ARCHIVE_TOKEN')) != None:
            args.token = cat
        else:
            print('CA: Error: Invalid token', file=sys.stderr)
            exit(1)

    # Instantiate server class
    s = network.Server(e[0], int(e[1]), args.token)

    # Connect
    try:
        s.connect()
    except Exception as e:
        print('CA: Error: Could not connect to server, exception:', e, file=sys.stderr)
        exit(1)
    print('CA: Connected to', e[0]+e[1])

    # Authenticate
    try:
        s.auth()
    except Exception as e:
        print('CA: Error: Could not authenticate with server, exception:', e, file=sys.stderr)
        exit(1)
    print('CA: Authenticated successfully')

    # Get URLs
    urls = []
    try:
        urls = s.urls()
    except Exception as e:
        print('CA: Error: Could not get URLs from server, exception:', e, file=sys.stderr)
        os.exit(1)
    print('CA: using URLs:', urls)

    # Instantiate client
    c = client.Client(urls)

    try:
        c.start()
    except KeyboardInterrupt:
        pass

    with open('./cats.log', 'a+') as f:
        for cat in list(c.cats):
            f.write(cat + '\n')

    print('CA: Done.')
    exit(0)

if __name__ == '__main__':
    main()
