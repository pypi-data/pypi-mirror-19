from trashtalk.tools import human_readable_from_bytes, print_files


def test_human_readable_from_bytes():
    b = human_readable_from_bytes(500)
    k = human_readable_from_bytes(1024)
    m = human_readable_from_bytes(1024**2)
    g = human_readable_from_bytes(1024**3)
    t = human_readable_from_bytes(1024**4)
    p = human_readable_from_bytes(1024**5)
    e = human_readable_from_bytes(1024**6)
    z = human_readable_from_bytes(1024**7)
    y = human_readable_from_bytes(1024**8)

    assert b == '500'
    assert k == "1K"
    assert m == "1M"
    assert g == "1G"
    assert t == "1T"
    assert p == "1P"
    assert e == "1E"
    assert z == "1Z"
    assert y == "1Y"

    assert "test error" == human_readable_from_bytes("test error")

def test_print_files(capsys):
    l = [["un", 2, 3, 4], ["deux", 2, 3], ["trois", 2, 3, 4]]
    print_files(l, 4)
    out, err = capsys.readouterr()
    assert bool(err) == False
    s = out.split('\n')
    assert s[0] == "un    2  3 4"
    assert s[1] == "deux  2  3  "
    assert s[2] == "trois 2  3 4"

    print_files([], 4)
    out, err = capsys.readouterr()
    assert bool(err) == False
    assert bool(out) == False

    l = [[None, "error"]]
    print_files(l, 4)
    out, err = capsys.readouterr()
    assert bool(out) == False
    assert err == "error\n"
