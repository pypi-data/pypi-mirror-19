from pathlib import Path
from trashtalk import generate_trashs
from tests.init_test import generate_trash
import pwd


def test_add_profil_info(tmpdir):
    test_file = tmpdir.join('.trashtalk')
    s = "MEDIA_PATH=/testmediapath\nTRASH_PATH=/testtrashpath , bob"
    test_file.write(s)
    f = Path(str(test_file))
    generate_trashs.MEDIA_DIR = ['/media']
    generate_trashs.TRASHS_PATH = []
    generate_trashs.add_profil_info(f.open())
    assert generate_trashs.MEDIA_DIR == ['/media', '/testmediapath']
    assert generate_trashs.TRASHS_PATH == [('bob', '/testtrashpath')]


def test_get_media_trashs(generate_trash, tmpdir, monkeypatch):
    trash = generate_trash
    generate_trashs.MEDIA_DIR = [str(tmpdir)]
    generate_trashs.TRASHS_PATH = [("test", trash.path)]
    def mockgetpwnam(user):
        return [1, 2, '0000']
    monkeypatch.setattr(pwd, 'getpwnam', mockgetpwnam)
    trashs, err = generate_trashs.get_media_trashs("remy")
    assert trashs[0].path == str(tmpdir) + "/media/.Trash-0000"
    assert trashs[0].name == "media"
    assert trashs[1].path == trash.path
    assert trashs[1].name == "test"
    trashs, err = generate_trashs.get_media_trashs("remy", ['desk'])
    assert trashs == []
    assert bool(err) is True
    generate_trashs.TRASHS_PATH = [("error", str(tmpdir) + "/fail")]
    trashs, err = generate_trashs.get_media_trashs("remy", ['error'])
    assert trashs == []
    assert bool(err) is True
