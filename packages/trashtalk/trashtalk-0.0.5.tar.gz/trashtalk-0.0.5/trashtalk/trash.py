from __future__ import print_function
from pathlib import Path
from datetime import datetime
from shutil import move
from trashtalk.exception import WrongFormat

__all__ = ["Trash"]


class Trash():
    """
    This object is an implementation of posix trash

    :Example:

    >>> from trasktalk import Trash
    >>> trash = Trash("/path/to/trash", "mytrash")
    >>> for element in trash: # list all elements in this trash
    >>>     print(element)
        element1
        element2
    """

    def __init__(self, path=None, name=""):
        """
        You can init Trash without value or
        path = "The trash path"
        name = "trash name"
        """
        if path:
            self.select_path(path, name)
        else:
            self.name = name

    def select_path(self, path, name):
        self.path = path
        self.name = name
        self.info = str((Path(path) / 'info').absolute())
        self.files = str((Path(path) / 'files').absolute())

    def list_files(self, files=None, size=False, info=False):
        """
        method to list files in trash

        can print size in byte with size
        if file doesn't exist return [None, 'error message']

        :param files: list specific file, if param == None list all elements
        :param size: at true return size in byte with file name
        :return: a generator who yield list [filename], or [filename, size]
        """
        total = 0
        if not files:
            l = Path(self.files).iterdir()
        else:
            l = map(lambda x: (Path(self.files) / x), files)
        for i in l:
            try:
                if not i.exists():
                    raise IOError("File: %s doesn't exist" % i.name)
                list_info_from_file = [i.name]
                if size:
                    list_info_from_file.append(i.lstat().st_size)
                    total += i.lstat().st_size
                if info:
                    i = (Path(self.info) / (i.name + ".trashinfo"))
                    if i.exists():
                        line = list(i.open())
                        for i in range(1, 3):
                            try:
                                list_info_from_file.append(
                                    line[i].split('=')[1].strip())
                            except:
                                list_info_from_file.append("unknow")
                yield list_info_from_file
            except Exception as e:
                yield [None, str(e)]
        if size:
            yield ["Total: ", total]

    def clean(self, list_files=None, path=None):
        """
        method to clean files from trash

        :return: list of error message
        """
        error = []
        info = False
        if not path:
            info = True
            path = self.files
        if not list_files:
            l = Path(path).iterdir()
        else:
            l = map(lambda x: (Path(path) / x), list_files)
        for i in l:
            try:
                if i.is_dir():
                    self.clean(path=(str(i)))
                    i.rmdir()
                else:
                    i.unlink()
                if info:
                    info = (Path(self.info) / (i.name + ".trashinfo"))
                    if info.exists():
                        info.unlink()
            except Exception as e:
                error.append(str(e))
        return error

    def remove(self, list_files=[]):
        """
        move file in list_files to trash and built trashinfo
        """
        if type(list_files) is not list and type(list_files) is not tuple:
            raise WrongFormat()
        files = Path(self.files)
        files_in_trash = list(map(lambda x: x[0], self.list_files()))
        error = []
        for f in list_files:
            old_path = Path(f)
            name = old_path.name
            while name in files_in_trash:
                i = 1
                name += str(i)
                i += 1
            if not old_path.exists():
                error.append("file %s doesn't exist" % old_path.name)
                continue
            info_path = (Path(self.info) / (name + '.trashinfo'))
            info_path.touch()
            move(str(old_path.absolute()), str(files) + '/' + name)
            with open(str(info_path.absolute()), "w") as o:
                o.write('[Trash Info]\n')
                o.write('Path=%s\n' % str(old_path.absolute()))
                date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                o.write('DeletionDate=%s\n' % date)
        return error

    def restore(self, list_files):
        if type(list_files) is not list and type(list_files) is not tuple:
            raise WrongFormat()
        error = []
        files_dir = Path(self.files)
        info_dir = Path(self.info)
        for f in list_files:
            file_path = files_dir / f
            file_info = info_dir / (f + ".trashinfo")
            if not file_path.exists():
                error.append("file doesn't in %s trash" % self.name)
                continue
            if not file_info.exists():
                error.append(
                    "file doesn't have trahsinfo in %s trash" % self.name)
                continue
            with file_info.open() as o:
                i = list(o)
                old_path = i[1].split("Path=")[1][:-1]
                # move file to old path
                try:
                    move(str(file_path.absolute()), old_path)
                    file_info.unlink()
                except Exception as e:
                    error.append(str(e))
        return error

    def __iter__(self):
        """Trash object iter on file in /files"""
        return self.list_files()

    def __str__(self):
        """return path """
        return "%s" % (self.path)
