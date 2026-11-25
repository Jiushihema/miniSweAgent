from ini_parser import parse_ini


def test_default_section_and_inline_comments():
    text = """
app = my_app ; top level
[web]
color = "#ff00aa" # hex color
note = 'a;b#c' ; keep inside quotes
escaped = "hello \"world\"" # comment
"""
    parsed = parse_ini(text)
    assert parsed["DEFAULT"]["app"] == "my_app"
    assert parsed["web"]["color"] == "#ff00aa"
    assert parsed["web"]["note"] == "a;b#c"
    assert parsed["web"]["escaped"] == 'hello "world"'
