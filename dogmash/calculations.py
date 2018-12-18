def new_elos(w_rating, l_rating, k):
    """Return the Elo ratings of two players after they have played a zero-sum
    game.

    Args:
        w_rating (int): Rating of winner before the game.
        l_rating (int): Rating of loser before the game.
        k (int): Measure of how much a game will affect the players' ratings.

    Returns:
        tuple of int: New ratings in tuple: (new_w_rating, new_l_rating).
    """
    R_1, R_2 = map(lambda x: 10 ** (x / 400), [w_rating, l_rating])
    E_1, E_2 = map(lambda x: x / (R_1 + R_2), [R_1, R_2])
    new_w_rating = round(w_rating + k * (1 - E_1))
    new_l_rating = round(l_rating - k * E_2)
    return new_w_rating, new_l_rating
