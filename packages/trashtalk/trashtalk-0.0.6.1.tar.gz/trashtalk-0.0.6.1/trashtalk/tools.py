from __future__ import print_function
import sys


def human_readable_from_bytes(num):
    if not num or type(num) is str:
        return num
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024:
            return ("%.2f" % num).rstrip('0').rstrip('.') + unit
        num /= 1024.0

    return ("%.2f" % num).rstrip('0').rstrip('.') + 'Y'


def print_files(list_files, nb_col=1):
    line = ""
    if not list_files:
        return
    if len(list_files[0]) > 1:
        for row in list_files:
            row[1] = human_readable_from_bytes(row[1])
    for e in range(nb_col):
        new_list = []
        for x in list_files:
            try:
                new_list.append(x[e])
            except:
                x.append("")
                new_list.append("")
        spaces = len(str(max(new_list, key=lambda x: len(str(x))))) + 1
        line += "{%d:%d}" % (e, spaces)
    for f in list_files:
        if f[0]:
            print(line.format(*f))
        else:
            print(f[1], file=sys.stderr)
