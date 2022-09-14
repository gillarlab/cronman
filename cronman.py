#!/usr/bin/python3

import sys
import getopt
from web import WebApp


def print_help():
    print('cronman -h for this help')
    print('cronman -p <portnumber>')


def main(argv):
    opts = None
    try:
        opts, _ = getopt.getopt(argv, 'hp:u:')
    except getopt.GetoptError:
        print_help()
        exit(2)

    port = 4321
    users = ['root']

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt == '-p':
            try:
                port = int(arg)
            except TypeError:
                port = 4321
        elif opt == '-u':
            users = list(map(str.strip, arg.split(',')))

    app = WebApp(users, port)
    app.run()


if __name__ == '__main__':
    main(sys.argv[1:])
