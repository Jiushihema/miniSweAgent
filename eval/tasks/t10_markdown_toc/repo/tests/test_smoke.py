from md_toc import extract_toc


def test_simple_toc():
    assert extract_toc("# Hello World\n") == [(1, "Hello World", "hello-world")]
