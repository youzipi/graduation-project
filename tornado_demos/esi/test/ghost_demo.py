from ghost import Ghost
ghost = Ghost()

with ghost.start() as session:
    page, extra_resources = session.open("http://jeanphix.me")
    assert page.http_status == 200 and 'jeanphix' in page.content
