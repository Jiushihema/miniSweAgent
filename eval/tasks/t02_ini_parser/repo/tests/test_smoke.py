from ini_parser import parse_ini


def test_basic_section():
    data = parse_ini("[db]\nhost = localhost\n")
    assert data == {"db": {"host": "localhost"}}
