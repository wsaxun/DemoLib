

def test_ehlo(smtp_connection):
    response,msg = smtp_connection.ehlo()
    assert response == 250
    assert b"smtp.gmail.com" in msg
    assert 0

def test_noop(smtp_connection):
    response,msg = smtp_connection.noop()
    assert response == 250
    assert 0