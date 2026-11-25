from csv_agg import aggregate_sum


def test_basic_sum():
    txt = "team,score\na,10\nb,20\na,5\n"
    assert aggregate_sum(txt, "team", "score") == [("b", 20.0), ("a", 15.0)]
