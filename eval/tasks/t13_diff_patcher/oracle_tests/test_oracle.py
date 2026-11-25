import pytest
from mini_patch import apply_unified_diff


def test_multi_hunk_and_mismatch():
    orig = "1\n2\n3\n4\n5\n6\n7\n8\n"
    diff = (
        "@@ -1,3 +1,4 @@\n"
        " 1\n"
        "+1.5\n"
        " 2\n"
        " 3\n"
        "@@ -6,3 +7,2 @@\n"
        " 6\n"
        "-7\n"
        " 8\n"
    )
    assert apply_unified_diff(orig, diff) == "1\n1.5\n2\n3\n4\n5\n6\n8\n"
    bad_diff = "@@ -1,2 +1,2 @@\n 1\n-WRONG\n+2\n"
    with pytest.raises(ValueError):
        apply_unified_diff(orig, bad_diff)
