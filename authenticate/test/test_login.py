from authenticate import login

def test_login():
    session, request = login()
    assert(session != None)
    assert(request != None)