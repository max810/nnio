from io import StringIO

from starlette.testclient import TestClient
from http import HTTPStatus
from .main import app
from .models import LayerTypes

client = TestClient(app)


def test_load_from_json_body_empty():
    response = client.request('post', '/architecture/load-from-json-body', json=dict())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_incorrect():
    response = client.request('post', '/architecture/load-from-json-body', json=dict(foo='bar'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_incorrect_with_id():
    response = client.request('post', '/architecture/load-from-json-body', json=dict(id='my_id_1'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_correct():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    response = client.request('post', '/architecture/load-from-json-body', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": "my_id_1", "num_layers": 0}


def test_load_from_json_body_incorrect_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[]))
    data['layers'].append(dict(name='Dense_1', type="sada", inputs=['Input_1']))
    response = client.request('post', '/architecture/load-from-json-body', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_correct_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[], params=dict()))
    data['layers'].append(dict(name='Dense_1', type=LayerTypes.Dense, inputs=['Input_1'], params=dict()))
    response = client.request('post', '/architecture/load-from-json-body', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": "my_id_1", "num_layers": 2}


def test_load_from_json_file_empty():
    response = client.request('post', '/architecture/load-from-json-file')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_file_correct():
    files = {"architecture-file": open("ExampleDiplomaArchitecture.json", 'rt')}
    response = client.request('post', '/architecture/load-from-json-file', files=files)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": "086de44a-f785-4159-bd35-906fc2d36296", "num_layers": 4}


def test_load_from_json_file_incorrect_json():
    files = {"architecture_": StringIO("incorrect architecture data")}
    response = client.request('post', '/architecture/load-from-json-file', files=files)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_file_incorrect_data():
    files = {"architecture_": StringIO("""{ "a": "b" }""")}
    response = client.request('post', '/architecture/load-from-json-file', files=files)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
