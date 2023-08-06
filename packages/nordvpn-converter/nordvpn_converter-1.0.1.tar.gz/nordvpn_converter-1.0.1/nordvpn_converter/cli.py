#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import tempfile

from nordvpn_converter.converter import Converter


# -*- coding: utf-8 -*-

VERSION = '1.0'
PROGRAM = "NordVPN Converter"


def main():
    parser = argparse.ArgumentParser(description='This is a simple conversion tool.')

    parser.add_argument('--source', type=str, help='Source folder for ovpn config files')
    parser.add_argument('--destination', type=str, help='Destination folder for output files',
                        default=tempfile.gettempdir())
    parser.add_argument('--certs', type=str, help='Source folder for certificates')
    parser.add_argument('--user', type=str, help='Username used for the NordVPN connection')
    parser.add_argument('-v', '--verbose', action="store_true", help='Verbose mode')

    parser.add_argument('--version', action='version', version="{0} {1}".format(PROGRAM, VERSION))

    args = parser.parse_args()

    if not (args.source and args.user and args.certs):
        parser.print_help()
        return

    try:
        c = Converter(debug_mode=args.verbose)
        c.set_source_folder(args.source)
        c.set_destination_folder(args.destination)
        c.set_certs_folder(args.certs)
        c.set_username(args.user)

        c.do_conversion()
    except Exception as e:
        print()
        print("[ERROR] Something went wrong. Details below:")
        print(e)
        print()

        parser.print_help()

if __name__ == "__main__":
    main()

