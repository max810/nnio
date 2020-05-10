import json
from io import StringIO
from http import HTTPStatus

from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

valid_model_body = json.load(open('example_sequential.json'))
valid_model_body_2_inputs = json.load(open('example_2inputs.json'))
valid_model_body_small = json.load(open('example_sequential_small.json'))


def test_export_from_json_body_empty_body():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras', json=dict())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_no_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    response = client.request('post', '/architecture/export-from-json-body?framework=keras', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras', json=dict(foo='bar'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect_with_id():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras', json=dict(id='my_id_1'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_no_framework():
    response = client.request('post', '/architecture/export-from-json-body', json=valid_model_body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect_framework():
    response = client.request('post', '/architecture/export-from-json-body?framework=mock_framework',
                              json=valid_model_body)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_correct():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras',
                              json=valid_model_body)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_body_correct_small():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras',
                              json=valid_model_body_small)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_body_correct_optional_params():
    response = client.request(
        'post',
        '/architecture/export-from-json-body?framework=keras&keras_prefer_sequential=1&line_break=crlf',
        json=valid_model_body
    )

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_body_correct_small_optional_params():
    response = client.request(
        'post',
        '/architecture/export-from-json-body?framework=keras&keras_prefer_sequential=1&line_break=crlf',
        json=valid_model_body_small
    )

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_body_correct_2_inputs():
    response = client.request('post', '/architecture/export-from-json-body?framework=keras',
                              json=valid_model_body_2_inputs)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_body_correct_2_inputs_try_sequential():
    # data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    response = client.request('post', '/architecture/export-from-json-body?framework=keras&prefer_sequential=1',
                              json=valid_model_body_2_inputs)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_file_empty():
    response = client.request('post', '/architecture/export-from-json-file?framework=keras')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_file_correct():
    files = {"architecture-file": open("example_sequential.json", 'rt')}
    response = client.request('post', '/architecture/export-from-json-file?framework=keras', files=files)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_file_random_order_correct():
    files = {"architecture-file": open("example_reversed.json", 'rt')}
    response = client.request('post', '/architecture/export-from-json-file?framework=keras', files=files)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_file_complex_correct():
    files = {"architecture-file": open("example_weird.json", 'rt')}
    response = client.request('post', '/architecture/export-from-json-file?framework=keras', files=files)

    assert response.status_code == HTTPStatus.OK


def test_export_from_json_file_incorrect_data():
    files = {"architecture-file": StringIO("""{ "a": "b" }""")}
    response = client.request('post', '/architecture/export-from-json-file?framework=keras', files=files)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
