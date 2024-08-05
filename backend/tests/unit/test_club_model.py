from backend.models.club import Club

def test_club_model():
    test_club = Club('Meridian')
    assert test_club.name == 'Meridian'
