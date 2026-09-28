from app import app, notes


def client():
    app.config["TESTING"] = True
    notes.clear()
    return app.test_client()


def add_note(c, **overrides):
    data = {"title": "Normalization", "subject": "DBMS",
            "author": "Amit", "content": "1NF, 2NF, 3NF"}
    data.update(overrides)
    return c.post("/add", data=data)


def test_health():
    res = client().get("/health")
    assert res.json["status"] == "ok"


def test_add_note_shows_on_home_and_api():
    c = client()
    assert add_note(c).status_code == 302
    assert b"Normalization" in c.get("/").data
    assert len(c.get("/api/notes").json) == 1


def test_missing_field_rejected():
    res = add_note(client(), title="")
    assert res.status_code == 400


def test_search_and_subject_filter():
    c = client()
    add_note(c)
    add_note(c, title="Deadlock", subject="OS", content="Coffman conditions")
    assert len(c.get("/api/notes?subject=OS").json) == 1
    assert len(c.get("/api/notes?q=normal").json) == 1


def test_like_increments_and_unknown_note_404():
    c = client()
    add_note(c)
    c.post("/like/1")
    assert c.get("/api/notes").json[0]["likes"] == 1
    assert c.post("/like/99").status_code == 404


def test_html_is_escaped():
    c = client()
    add_note(c, content="<script>alert(1)</script>")
    assert b"<script>alert(1)</script>" not in c.get("/").data
