import os
import sys
import argparse

from . import network

def main():
    """Starts the crawler."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--endpoint', type=str, help='The host:port of the server to connect to, e.g. "x.x.x.x:x", or "example.com:x"', default='')
    parser.add_argument('-t', '--token', type=str, help='The authentication token of the server to connect to, or set the CAT_ARCHIVE_TOKEN environment variable', default='')
    parser.add_argument('-l', '--local', type=str, help='Set an initial URL and crawl without connecting to a server (mainly just for testing purposes)', default='')
    parser.add_argument('-c', '--custom', type=bool, help='Use the custom model or not (default False)', default=False)
    parser.add_argument('-g', '--good-domains', type=str, help='A comma separated list of good domains, e.g. "www.reddit.com,www.animalplanet.com"', default='')
    parser.add_argument('-b', '--bad-domains', type=str, help='A comma separated list of bad domains', default='')
    args = parser.parse_args()

    endpoint = ('', '0')
    if args.local != '':
        network.local_urls = [args.local]
    else:

        endpoint = args.endpoint.split(':')
        if len(endpoint) < 2 or (len(endpoint) > 1 and not endpoint[1].isdigit()):
            print('Error: Invalid endpoint')
            sys.exit(1)

        # Use environment variable if args.token is empty
        if args.token == '':
            cat = os.environ.get('CAT_ARCHIVE_TOKEN')
            if cat != None:
                args.token = cat
            else:
                print('Error: Invalid token')
                sys.exit(1)

    # Instantiate server class
    s = network.Server(endpoint[0], int(endpoint[1]), args.token)

    # Instantiate client:
    # Import here for a faster --help
    from .client import Client
    print('Good domains:', args.good_domains.split(','))
    print('Bad domains:', args.bad_domains.split(','))
    c = Client(s, args.custom, args.good_domains.split(','), args.bad_domains.split(','))

    # Connect
    try:
        s.connect()
    except Exception as e:
        print('Error: Could not connect to server, exception:', e)
        s.close()
        sys.exit(1)
    if args.local != '':
        print('Running without server')
    else:
        print('Connected to', endpoint[0]+":"+endpoint[1])

    # Authenticate
    try:
        s.auth()
    except network.exceptions.InvalidStrtPacketReceived:
        print('Error: Could not authenticate, invalid STRT packet received')
        s.close()
        sys.exit(1)
    except Exception as e:
        print('Error: Could not authenticate with server, exception:', e)
        s.close()
        sys.exit(1)
    print('Authenticated successfully')

    # Start the client
    try:
        c.start()
    except KeyboardInterrupt:
        pass

    # Write found cats
    with open('./cats.log', 'a+') as f:
        for cat in list(c.cats):
            f.write(str(cat) + '\n')
        f.write(str(c.domain_priority))

    print('Wrote to cats.log')
    s.close()
    sys.exit(0)
