from csv_agg import aggregate_sum


def test_missing_values_and_tiebreak():
    txt = "team,score\n z , 10 \n a , 10 \n a , NA \n b , \n c , null \n z , N/A \n"
    res = aggregate_sum(txt, "team", "score")
    assert res == [("a", 10.0), ("z", 10.0)]
