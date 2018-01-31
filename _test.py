import pytest
import socket as s


@pytest.fixture
def socket(request):
    _socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    def socket_teardown():
        _socket.close()
    request.addfinalizer(socket_teardown)
    return _socket


def test_server_connect(socket):
    socket.connect(('127.0.0.1', 8123))
    assert socket
