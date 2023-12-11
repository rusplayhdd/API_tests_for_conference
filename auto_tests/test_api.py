"""
API testing 09-12-2023(c)
"""
import warnings

import requests, pytest

resp = requests.get("https://reqres.in/api/users")
bad_resp = requests.get("https://reqres.in/a123pi/us123ers")


def test_status_code():
    """
    запрос возвращает ответ со статусом 200; id=0001
    """
    assert resp.status_code == 200


@pytest.mark.parametrize("i", [0, 1, 2, 3, 4, 5])
def test_check_users(i):
    """id=0002
    запрос возвращает список юзеров при успешном ответе
    """
    assert list(resp.json().keys())[4] == "data", "key is wrong"
    assert type(resp.json()["data"]) == list, "something wrong"
    assert type(resp.json()["data"][i]) == dict, "should be an obj!!"
    assert "first_name" and "last_name" in resp.json()["data"][i]


def test_bad_status_code():
    """id=0003
    запрос возвращает ответ со статусом 404 при некорректом пути хоста
    """
    assert bad_resp.status_code == 404


def test_error_message_body():
    """id=0004"""
    errors = ["error", "Error", "Not found", "not found", "404"]
    assert any(error in bad_resp.text for error in errors)


@pytest.mark.xfail(reason="waiting for fix!")
def test_bad_resp_has_dict():
    """id=0005"""
    assert type(bad_resp.json()) == dict, "should be an obj!!!"


def test_bad_status_has_error_in_body():
    """id=0006"""
    assert 399 <= bad_resp.status_code <= 500
    errors = ["error", "Error", "Not found", "not found", "404"]
    assert any(error in bad_resp.text for error in errors)


def test_body_has_a_dict_with_good_status():
    """id==0007"""
    assert resp.status_code == 200
    assert isinstance(resp.json(), object), "body should be an obj!!!"


@pytest.mark.parametrize("i", [0, 1, 2, 3, 4, 5])
def test_body_has_objs(i):
    """id==0008"""
    assert "data" in resp.json()
    assert isinstance(resp.json()["data"], list)
    assert type(resp.json()["data"][i]) == dict, "should be an obj!!"


@pytest.mark.parametrize("i", [0, 1, 2, 3, 4, 5])
def test_body_has_keys_as_string(i):
    """id=0009"""
    assert 199 <= resp.status_code <= 300
    keys = ("id", "first_name", "last_name")
    assert all(map(resp.json()["data"][i].__contains__, keys))
    # ==================
    keys = ["email", "avatar"]

    # assert not any(key in resp.json()["data"][i] for key in keys)
    # print("\033[33m The data in body doesn't contain any key\033[0m")

    if not any(key in resp.json()["data"][i] for key in keys):
        print("\033[33m The data in body doesn't contain any key\033[0m")


@pytest.mark.parametrize("index, key, __type", [(0, "id", int), (0, "avatar", str),
                                                (1, "id", int), (1, "avatar", str),
                                                (2, "id", int), (2, "avatar", str),
                                                (3, "id", int), (3, "avatar", str),
                                                (4, "id", int), (4, "avatar", str),
                                                (5, "id", int), (5, "avatar", str)])
def test_budy_has_all_the_necessary_keys(index, key, __type):
    """id=0010"""
    assert resp.status_code == 200
    assert type(resp.json()["data"][index][key]) == __type
