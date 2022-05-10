import json
from unittest.mock import MagicMock

import pytest

from common.utils.exceptions import AlreadyRegisteredError, InvalidRegistrationCredentialsError

REGISTRATION_URL = "/api/registration"

USERNAME = "test_user"
PASSWORD = "test_password"


@pytest.fixture
def mock_authentication_service(monkeypatch):
    mock_service = MagicMock()
    mock_service.register_new_user = MagicMock()
    mock_service.needs_registration = MagicMock()

    monkeypatch.setattr(
        "monkey_island.cc.resources.auth.registration.AuthenticationService", mock_service
    )

    return mock_service


@pytest.fixture
def make_registration_request(flask_client):
    def inner(request_body):
        return flask_client.post(REGISTRATION_URL, data=request_body, follow_redirects=True)

    return inner


def test_registration(make_registration_request, mock_authentication_service):
    registration_request_body = f'{{"username": "{USERNAME}", "password": "{PASSWORD}"}}'
    response = make_registration_request(registration_request_body)

    assert response.status_code == 200
    mock_authentication_service.register_new_user.assert_called_with(USERNAME, PASSWORD)


def test_empty_credentials(make_registration_request, mock_authentication_service):
    registration_request_body = "{}"
    make_registration_request(registration_request_body)

    mock_authentication_service.register_new_user.assert_called_with("", "")


def test_invalid_credentials(make_registration_request, mock_authentication_service):
    mock_authentication_service.register_new_user = MagicMock(
        side_effect=InvalidRegistrationCredentialsError()
    )

    registration_request_body = "{}"
    response = make_registration_request(registration_request_body)

    assert response.status_code == 400


def test_registration_not_needed(make_registration_request, mock_authentication_service):
    mock_authentication_service.register_new_user = MagicMock(side_effect=AlreadyRegisteredError())

    registration_request_body = "{}"
    response = make_registration_request(registration_request_body)

    assert response.status_code == 400


def test_internal_error(make_registration_request, mock_authentication_service):
    mock_authentication_service.register_new_user = MagicMock(side_effect=Exception())

    registration_request_body = json.dumps({})
    response = make_registration_request(registration_request_body)

    assert response.status_code == 500


@pytest.mark.parametrize("needs_registration", [True, False])
def test_needs_registration(flask_client, mock_authentication_service, needs_registration):
    mock_authentication_service.needs_registration = MagicMock(return_value=needs_registration)
    response = flask_client.get(REGISTRATION_URL, follow_redirects=True)

    assert response.status_code == 200
    assert response.json["needs_registration"] is needs_registration
