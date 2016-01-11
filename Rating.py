# TODO: Docstrings
# https://metinmediamath.wordpress.com/2013/11/27/how-to-calculate-the-elo-rating-including-example/

k_factor = 32  # The ICC uses 32 for chess matches

def ratingAdjust(win_player, lose_player, outcome):
    # Outcome may be 'win' or 'tie'
    # Get the ratings of both players
    w_rating = win_player.getRating()
    l_rating = lose_player.getRating()

    # Transform the ratings for an elo system
    w_transform = 10**(w_rating/400)
    l_transform = 10**(l_rating/400)

    # Expected score
    w_expected =  w_transform/(w_transform + l_transform)
    l_expected = l_transform/(w_transform + l_transform)

    # New values
    k_factor = 32  # The ICC uses 32 for chess matches
    s = None
    if outcome == 'win':
        s = 1
    else:
        s = 0.5
    win_player.setRating(w_rating + k_factor * (s - w_expected))
    lose_player.setRating(w_rating + k_factor * ((1-s) - l_expected))


