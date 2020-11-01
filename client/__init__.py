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
    parser.add_argument('-l', '--local', type=str, help='Set an initial URL and crawl without connecting to a server (mainly just for testing purposes)', default='')
    args = parser.parse_args()

    endpoint = ('', '0')
    if args.local != '':
        network.local_urls = [args.local]
    else:

        endpoint = args.endpoint.split(':')
        if len(endpoint) < 2 or (len(endpoint) > 1 and not endpoint[1].isdigit()):
            print('CA: Error: Invalid endpoint')
            sys.exit(1)

        # Use environment variable if args.token is empty
        if args.token == '':
            cat = os.environ.get('CAT_ARCHIVE_TOKEN')
            if cat != None:
                args.token = cat
            else:
                print('CA: Error: Invalid token')
                sys.exit(1)

    # Instantiate server class
    s = network.Server(endpoint[0], int(endpoint[1]), args.token)

    # Connect
    try:
        s.connect()
    except Exception as e:
        print('CA: Error: Could not connect to server, exception:', e)
        s.close()
        sys.exit(1)
    if args.local != '':
        print('CA: Running without server')
    else:
        print('CA: Connected to', endpoint[0]+":"+endpoint[1])

    # Authenticate
    try:
        s.auth()
    except network.exceptions.InvalidStrtPacketReceived:
        print('CA: Error: Could not authenticate, invalid STRT packet received')
        s.close()
        sys.exit(1)
    except Exception as e:
        print('CA: Error: Could not authenticate with server, exception:', e)
        s.close()
        sys.exit(1)
    print('CA: Authenticated successfully')

    # Instantiate client:
    c = client.Client(s)

    # Start the client
    try:
        c.start()
    except KeyboardInterrupt:
        pass

    # Write found cats
    with open('./cats.log', 'a+') as f:
        for cat in list(c.cats):
            f.write(cat + '\n')

    print('CA: Wrote to cats.log')
    s.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
