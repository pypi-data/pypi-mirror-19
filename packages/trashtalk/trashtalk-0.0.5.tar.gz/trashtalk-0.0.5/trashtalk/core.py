#! /usr/bin/env python3
"""
Option parser and the main function
"""
from __future__ import print_function, absolute_import
import argparse
from trashtalk.generate_trashs import generate_trashs
import sys
from trashtalk.tools import print_files

__all__ = ["trashtalk"]


def parse_option(args=None):
    parser = argparse.ArgumentParser(
        description="Taking out your trash easily")
    # CLASSIC
    from trashtalk.__init__ import __version__
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s: ' + __version__)
    parser.add_argument('--verbose', action='store_true')
    # TRASH SELECTION
    selection = parser.add_argument_group('trash selections')
    option = parser.add_argument_group('trash options')
    selection.add_argument('trash', nargs='*', default=[],
                           help=("name where you want use trash, "
                                 "this is a list, you can write home or media,"
                                 " by default your home trash was selected"))
    selection.add_argument('-a', action='store_true', default=False,
                           help="select all trash (home + all your media)")
    selection.add_argument('-u', action='store', nargs='*',
                           help="select user")
    selection.add_argument('-am', action='store_true', default=False,
                           help="select all media, this can depend of user")
    # TRASH OPTION
    option.add_argument('-p', action='store_true', default=False,
                        help="print trash path")
    option.add_argument('-f', '--files', action='store', nargs='*',
                        help="select file in trash")
    option.add_argument('-l', action='store_true', default=False,
                        help="list file in trash")
    option.add_argument('-s', action='store_true',
                        help=("print size"))
    option.add_argument('-i', action='store_true',
                        help=("print info"))
    option.add_argument('-cl', '--clean', action='store_true',
                        help="clean file, or without file all")
    option.add_argument('-rm', action='store', nargs='*',
                        help="move file to selected trash")
    option.add_argument('-re', action='store_true', default=False,
                        help="restore file from selected trash")
    if args:
        return parser.parse_known_args(args)
    return parser.parse_args()


def trashtalk():
    options = parse_option()
    if (options.am or options.trash) and "home" not in options.trash:
        home = False
    else:
        home = True
        if options.trash:
            options.trash.remove('home')
    if options.a:
        options.am = True
    trashs , error = generate_trashs(options.u, options.trash, home, options.am)
    for error in error:
        print(error, file=sys.stderr)
    for trash in trashs:
        error = []
        if not trash:
            continue
        if options.p or (
                not options.l and not
                options.s and not options.clean
                and not options.rm):
            if options.p:
                print('\033[34;1m%s: ' % trash.name, end='')
            print("%s\033[0m" % str(trash))
        if options.l or options.s:
            print_files(
                list(trash.list_files(options.files, options.s, options.i)),
                options.s + options.i * 2 + 1
            )
        if options.clean:
            error = trash.clean(options.files)
        if options.rm:
            error = trash.remove(options.rm)
        if options.re:
            error = trash.restore(options.f)
        if error:
            for e in error:
                print(e, file=sys.stderr)
