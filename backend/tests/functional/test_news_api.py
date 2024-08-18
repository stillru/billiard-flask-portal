from .. import log


def test_add_tag(client):
    tags = client.post("/api/tags", json={"name": "club"})
    tags2 = client.post("/api/tags", json={"name": "tounament"})
    tags3 = client.post("/api/tags", json={"name": "season"})
    json_data = tags.get_json()
    log.debug(json_data)
    assert tags.status_code == 201


def test_show_tags(client):
    tags = client.get("/api/tags")
    json_data = tags.get_json()
    log.debug(json_data)
    assert tags.status_code == 200


def test_duplicate_tag(client):
    tags = client.post("/api/tags", json={"name": "club"})
    json_data = tags.get_json()
    log.debug(json_data)
    assert tags.status_code == 400


def test_invalid_input_tag(client):
    tags = client.post("/api/tags", json={"name1": "club"})
    json_data = tags.get_json()
    log.debug(json_data)
    assert tags.status_code == 400


def test_insert_news(client):
    new_news = client.post(
        "/api/news",
        json={
            "title": "First news",
            "body": "new data",
            "source_type": "club",
            "source_id": "1",
            "tags": "club",
        },
    )
    json_data = new_news.get_json()
    log.debug(json_data)
    assert new_news.status_code == 201


def test_show_news(client):
    news_list = client.get("/api/news")
    json_data = news_list.get_json()
    log.debug(json_data)
    assert news_list.status_code == 200
