#!/usr/bin/env python3

# This script converts xrdb (X11) color scheme format to
# the new Windows Terminal color scheme format
#
# Usage:
# xrdb2vscode.py path/to/xrdb/files -d /vscode/output

import os
import re
import argparse
import json
from xrdbparser import Xrdb


def process_file(data):
    # map to Windows Terminal names
    pairs = [
        ("foreground", "terminal.foreground"),
        ("background", "terminal.background"),
        ("cursorColor", "terminalCursor.foreground"),
        ("selectionBackground", "terminal.selectionBackground")
    ]

    ansi = [
        "terminal.ansiBlack",
        "terminal.ansiBlue",
        "terminal.ansiCyan",
        "terminal.ansiGreen",
        "terminal.ansiMagenta",
        "terminal.ansiRed",
        "terminal.ansiWhite",
        "terminal.ansiYellow",
        "terminal.ansiBrightBlack",
        "terminal.ansiBrightBlue",
        "terminal.ansiBrightCyan",
        "terminal.ansiBrightGreen",
        "terminal.ansiBrightMagenta",
        "terminal.ansiBrightRed",
        "terminal.ansiBrightWhite",
        "terminal.ansiBrightYellow"
    ]

    scheme = OrderedDict()

    for i, name in enumerate(ansi):
        color = data.colors[i]
        if color:
            scheme[name]: color

    for vscode, xrdb in pairs:
        color = getattr(data, xrdb, None)
        if color:
            scheme[vscode]: color


    return json.dumps({"workbench.colorCustomizations":scheme}, indent=4)



def main(xrdb_path, output_path=None):
    for data in Xrdb.parse_all(xrdb_path):
        output = process_file(data)
        if not output_path:
            print(output)
        else:
            dest = os.path.join(output_path, data.name)
            with open('{0}.json'.format(dest), 'w+') as f:
                f.write(output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Translate X color schemes to Windows Terminal format')
    parser.add_argument('xrdb_path', type=str, help='path to xrdb files')
    parser.add_argument('-d', '--destiny', type=str, dest='output_path',
                        help='path where Windows Terminal config files will be' +
                        ' created, if not provided then will be printed')

    args = parser.parse_args()

    main(args.xrdb_path, args.output_path)
