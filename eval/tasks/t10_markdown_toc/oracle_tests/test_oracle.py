from md_toc import extract_toc


def test_fenced_blocks_trailing_hash_and_dups():
    md = """# Setup ##
```python
# not a heading
## also not a heading
```
## Setup
### Setup
~~~bash
# ignored
~~~
"""
    assert extract_toc(md) == [
        (1, "Setup", "setup"),
        (2, "Setup", "setup-1"),
        (3, "Setup", "setup-2"),
    ]
