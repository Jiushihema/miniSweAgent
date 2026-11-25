from expr_eval import evaluate


def test_add_mul():
    assert evaluate("1 + 2 * 3") == 7
