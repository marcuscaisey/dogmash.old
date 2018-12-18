from dogmash import calculations


def test_new_elos():
    w_rating = 2400
    l_rating = 2000
    k = 32
    assert calculations.new_elos(w_rating, l_rating, k) == (2403, 1997)
