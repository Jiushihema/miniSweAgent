from mini_patch import apply_unified_diff


def test_single_hunk():
    orig = "a\nb\nc\n"
    diff = "@@ -1,3 +1,3 @@\n a\n-b\n+B\n c\n"
    assert apply_unified_diff(orig, diff) == "a\nB\nc\n"
