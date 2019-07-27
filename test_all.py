from io import StringIO
from starlette.testclient import TestClient
from http import HTTPStatus
from .main import app
from .models import LayerTypes

client = TestClient(app)


def test_export_from_json_body_empty():
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=dict())

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect():
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=dict(foo='bar'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect_with_id():
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=dict(id='my_id_1'))

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_correct():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json().items() >= {"id": "my_id_1", "num_layers": 0}.items()


def test_export_from_json_body_no_framework():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    response = client.request('post', '/architecture/export-from-json-body', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_incorrect_framework():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    response = client.request('post', '/architecture/export-from-json-body?framework=mock_framework', json=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_export_from_json_body_incorrect_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[])
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[]))
    data['layers'].append(dict(name='Dense_1', type="sada", inputs=['Input_1']))
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_body_correct_multiple_layers():
    data = dict(date_created="2019-07-24 17:56:34", id="my_id_1", layers=[], name='MyModel_1')
    data['layers'].append(dict(name='Input_1', type=LayerTypes.Input, inputs=[], params=dict()))
    data['layers'].append(dict(name='Dense_1', type=LayerTypes.Dense, inputs=['Input_1'], params=dict()))
    response = client.request('post', '/architecture/export-from-json-body?framework=Keras', json=data)

    assert response.status_code == HTTPStatus.OK
    assert response.json().items() >= {"id": "my_id_1", "num_layers": 2}.items()


def test_export_from_json_file_empty():
    response = client.request('post', '/architecture/export-from-json-file?framework=Keras')

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_file_correct():
    files = {"architecture-file": open("ExampleDiplomaArchitecture.json", 'rt')}
    response = client.request('post', '/architecture/export-from-json-file?framework=Keras', files=files)

    assert response.status_code == HTTPStatus.OK
    assert response.json().items() >= {"id": "086de44a-f785-4159-bd35-906fc2d36296", "num_layers": 4}.items()


def test_export_from_json_file_incorrect_json():
    files = {"architecture_": StringIO("incorrect architecture data")}
    response = client.request('post', '/architecture/export-from-json-file?framework=Keras', files=files)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_file_incorrect_data():
    files = {"architecture_": StringIO("""{ "a": "b" }""")}
    response = client.request('post', '/architecture/export-from-json-file?framework=Keras', files=files)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_export_from_json_file_model_creation():
    files = {"architecture-file": open("ExampleDiplomaArchitecture.json", 'rt')}
    response = client.request('post', '/architecture/export-from-json-file?framework=Keras', files=files)

    assert response.status_code == HTTPStatus.OK
    assert response.json()["model"] == "{}<br>{}<br>{}<br>{}<br>".format(
        "Input_1 -> Flatten_1",
        "Input_1 -> Flatten_1 -> Dense_1",
        "Flatten_1 -> Dense_1 -> Dense_2",
        "Dense_1 -> Dense_2",
    )
