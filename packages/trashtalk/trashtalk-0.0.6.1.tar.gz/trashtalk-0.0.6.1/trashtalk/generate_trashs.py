from __future__ import print_function, absolute_import
import pwd
from os import getlogin
from pathlib import Path
from trashtalk.trash import Trash
import sys
from os.path import expanduser

"""
Module who generate trash

:example
in /home/user/.trashtalk
add
# to make a commentary
MEDIA_PATH=path/to/your/media
TRASH_PATH=a/direct/path/to/trash , nameofyourtrash
"""

MEDIA_DIR = ['/media']
TRASHS_PATH = [] # direct link to Trash
HOME_TRASH_PATH = ".local/share/Trash"


def add_profil_info(f):
    for line in f:
        line = line.split('#')[0].strip()
        try:
            key, val = line.split("=")
            if key == "MEDIA_PATH":
                MEDIA_DIR.append(val)
            elif key == "TRASH_PATH":
                path, name = val.split(',')
                TRASHS_PATH.append((name.strip(), path.strip()))
        except:
            pass

profil = Path(expanduser("~/.trashtalk"))
if profil.exists():
    add_profil_info(profil.open())

def generate_trashs(users=[], medias=[], home=True, all_media=False):
    trashs = []
    error = []
    if not users:
        users = [getlogin()]
    for user in users:
        if home:
            trash = Path(expanduser("~%s/%s" % (user, HOME_TRASH_PATH)))
            if trash.exists():
                trashs.append(Trash(str(trash.absolute()), user))
            else:
                error.append("can't find: " + trash.name)
        if all_media or medias:
            trashs_media, errors_media = get_media_trashs(user, medias)
            trashs += trashs_media
            error += errors_media
    return trashs, error


def get_media_trashs(user, medias_name=[]):
    trashs = []
    error = []
    media_dir = MEDIA_DIR + ["%s/%s" % (MEDIA_DIR[0], user)]
    for d in media_dir:
        m_d = Path(d)
        if not m_d.exists():
            continue
        for m in m_d.iterdir():
            trash = m /  (".Trash-" + str(pwd.getpwnam(user)[2]))
            if trash.exists() and (not medias_name or m.name in medias_name):
                trashs.append(Trash(str(trash.absolute()), m.name))
            elif m.name in medias_name:
                error.append("can't find: " + m.name)
    for d in TRASHS_PATH:
        trash = Path(d[1])
        name = d[0]
        if trash.exists() and (not medias_name or name in medias_name):
            trashs.append(Trash(str(trash.absolute()), name))
        elif name in medias_name:
            error.append("can't find: " + name)
    return trashs, error
