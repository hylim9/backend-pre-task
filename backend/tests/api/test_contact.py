import pytest

CONTACT_API = "/api/v1/contacts"


@pytest.mark.django_db
def test_post_labels(client):
    response = client.post(f"{CONTACT_API}/labels", dict(name="기타"))

    assert response.status_code == 201


@pytest.mark.django_db
def test_get_labels(client):
    response = client.get(f"{CONTACT_API}/labels")
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_contact(client):
    import json

    payload = {
        "label": [1],
        "updated_by": "pytest",
        "profile_picture": "https://picsum.photos/200",
        "name": "테스터",
        "email": "pytest@example.com",
        "phone_number": "010-1515-1300",
        "company": "PYTEST",
        "job_title": "tester",
        "description": "테스트",
        "address": "서울",
        "birth_date": "2024-04-23",
        "homepage_url": "https://www.hompage.com",
    }

    response = client.post(
        f"{CONTACT_API}/", json.dumps(payload), content_type="application/json"
    )

    data = response.data

    assert response.status_code == 201
    assert data["name"] == payload["name"]


@pytest.mark.django_db(transaction=True)  # 독립 수행 test
def test_post_contact_with_label(client):
    label_response = client.post(f"{CONTACT_API}/labels", dict(name="기타"))

    payload = dict(
        label=label_response.data["id"],
        updated_by="pytest",
        profile_picture="https://picsum.photos/200",
        name="테스터",
        email="pytest@example.com",
        phone_number="010-1515-1300",
        company="PYTEST",
        job_title="tester",
        description="테스트",
        address="서울",
        birth_date="2024-04-23",
        homepage_url="https://www.hompage.com",
    )

    response = client.post(f"{CONTACT_API}/", payload)

    data = response.data

    assert response.status_code == 201
    assert data["name"] == payload["name"]


@pytest.mark.django_db
def test_get_contacts(client):
    response = client.get(f"{CONTACT_API}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_contact_by_id(client):
    response = client.get(f"{CONTACT_API}/1")

    assert response.status_code == 200
    assert isinstance(response.data, dict)


@pytest.mark.django_db
def test_edit_contact_by_id(client):
    import json

    data = {"name": "테스터이름수정"}
    response = client.put(
        f"{CONTACT_API}/1", json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.data["name"] == data["name"]
    assert isinstance(response.data, dict)


@pytest.mark.django_db
def test_contact_phone_number_validation(client):
    import json

    payload = {
        "label": [1],
        "updated_by": "pytest",
        "profile_picture": "https://picsum.photos/200",
        "name": "같은번호테스터",
        "email": "pytest@example.com",
        "phone_number": "010-1111-0000",
        "company": "PYTEST",
        "job_title": "tester",
        "description": "테스트",
        "address": "서울",
        "birth_date": "2024-04-23",
        "homepage_url": "",
    }

    response = client.post(
        f"{CONTACT_API}/", json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_contact_email_validation(client):
    import json

    payload = {
        "label": [1],
        "updated_by": "pytest",
        "profile_picture": "https://picsum.photos/200",
        "name": "잘못된이메일주소",
        "email": "pytestexample.com",
        "phone_number": "010-1111-0002",
        "company": "PYTEST",
        "job_title": "tester",
        "description": "테스트",
        "address": "서울",
        "birth_date": "2024-04-23",
        "homepage_url": "",
    }

    response = client.post(
        f"{CONTACT_API}/", json.dumps(payload), content_type="application/json"
    )

    # data = response.data
    # print(data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_contact_profile_picture_validation(client):
    import json

    payload = {
        "updated_by": "pytest",
        "profile_picture": "picsum.photos/200",
        "name": "잘못된프로필사진URL",
        "email": "pytest@example.com",
        "phone_number": "010-1111-0003",
        "company": "PYTEST",
        "job_title": "tester",
        "description": "테스트",
        "address": "서울",
        "birth_date": "2024-04-23",
        "homepage_url": "",
    }

    response = client.post(
        f"{CONTACT_API}/", json.dumps(payload), content_type="application/json"
    )

    # data = response.data
    # print(data)
    assert response.status_code == 400
