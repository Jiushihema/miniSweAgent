from expr_eval import evaluate


def test_power_and_unary_and_divmod():
    assert evaluate("2 ** 3 ** 2") == 512
    assert evaluate("-2 ** 2") == -4
    assert evaluate("(-2) ** 2") == 4
    assert evaluate("17 // 5 + 17 % 5") == 5
