from starlette.testclient import TestClient
from http import HTTPStatus
from .main import app
from .models import LayerTypes

client = TestClient(app)


def test_load_from_json_body_empty():
    response = client.request('post', '/architecture/load_from_json_body', json=dict())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_incorrect():
    response = client.request('post', '/architecture/load_from_json_body', json=dict(foo='bar'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_incorrect_with_id():
    response = client.request('post', '/architecture/load_from_json_body', json=dict(id='my_id_1'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_correct():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    response = client.request('post', '/architecture/load_from_json_body', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": "my_id_1", "num_layers": 0}


def test_load_from_json_body_incorrect_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[]))
    data['layers'].append(dict(name='Dense_1', type="sada", inputs=['Input_1']))
    response = client.request('post', '/architecture/load_from_json_body', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_load_from_json_body_correct_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[], params=dict()))
    data['layers'].append(dict(name='Dense_1', type=LayerTypes.Dense, inputs=['Input_1'], params=dict()))
    response = client.request('post', '/architecture/load_from_json_body', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": "my_id_1", "num_layers": 2}
