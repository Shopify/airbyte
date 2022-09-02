#
# Copyright (c) 2022 Airbyte, Inc., all rights reserved.
#

from datetime import datetime
from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from source_razorpay.streams import RazorpayStream





@pytest.fixture
def patch_base_class(mocker):
    # Mock abstract methods to enable instantiating abstract class
    mocker.patch.object(RazorpayStream, "path", "v0/example_endpoint")
    mocker.patch.object(RazorpayStream, "primary_key", "test_primary_key")
    mocker.patch.object(RazorpayStream, "__abstractmethods__", set())


@pytest.fixture(name="config")
def config_fixture():
    config = {"authenticator": "authenticator", "account_id": "123456", "start_date": "2022-08-25T12:30:55Z"}
    return config


def test_request_params(patch_base_class, config):
    stream = RazorpayStream(authenticator=config["authenticator"], start_date=config["start_date"])
    next_page_token = {"skip": 50}
    inputs = {"stream_slice": None, "stream_state": None, "next_page_token": next_page_token}
    expected_from_timestamp = datetime.strptime(config["start_date"], "%Y-%m-%dT%H:%M:%SZ").timestamp()

    expected_params = {"count": 10, "from": expected_from_timestamp, "skip": 50}
    assert stream.request_params(**inputs) == expected_params


def test_next_page_token(patch_base_class):
    stream = RazorpayStream()
    # TODO: replace this with your input parameters
    inputs = {"response": MagicMock()}
    # TODO: replace this with your expected next page token
    expected_token = None
    assert stream.next_page_token(**inputs) == expected_token


def test_parse_response(patch_base_class):
    stream = RazorpayStream()
    # TODO: replace this with your input parameters
    inputs = {"response": MagicMock()}
    # TODO: replace this with your expected parced object
    expected_parsed_object = {}
    assert next(stream.parse_response(**inputs)) == expected_parsed_object


def test_request_headers(patch_base_class):
    stream = RazorpayStream()
    # TODO: replace this with your input parameters
    inputs = {"stream_slice": None, "stream_state": None, "next_page_token": None}
    # TODO: replace this with your expected request headers
    expected_headers = {}
    assert stream.request_headers(**inputs) == expected_headers


def test_http_method(patch_base_class):
    stream = RazorpayStream()
    # TODO: replace this with your expected http request method
    expected_method = "GET"
    assert stream.http_method == expected_method


@pytest.mark.parametrize(
    ("http_status", "should_retry"),
    [
        (HTTPStatus.OK, False),
        (HTTPStatus.BAD_REQUEST, False),
        (HTTPStatus.TOO_MANY_REQUESTS, True),
        (HTTPStatus.INTERNAL_SERVER_ERROR, True),
    ],
)
def test_should_retry(patch_base_class, http_status, should_retry):
    response_mock = MagicMock()
    response_mock.status_code = http_status
    stream = RazorpayStream()
    assert stream.should_retry(response_mock) == should_retry


def test_backoff_time(patch_base_class):
    response_mock = MagicMock()
    stream = RazorpayStream()
    expected_backoff_time = None
    assert stream.backoff_time(response_mock) == expected_backoff_time
