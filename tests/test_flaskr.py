import os
import tempfile

import pytest

import av_dashboard

@pytest.fixture
def client():
    client = av_dashboard.create_app().test_client()
    yield client

def test_simple(client):
    rv = client.get('/')
    assert b'Agile Ventures Dashboard' in rv.data
