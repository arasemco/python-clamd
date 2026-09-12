#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for clamd module."""
from io import BytesIO
from typing import Generator, Union, Tuple, List

import clamd
from contextlib import contextmanager
import tempfile
import shutil
import os
import stat

import pytest

mine = stat.S_IREAD | stat.S_IWRITE
other = stat.S_IROTH
execute = stat.S_IEXEC | stat.S_IXOTH


@contextmanager
def mkdtemp(*args, **kwargs) -> Generator[Union[str, bytes], None, None]:
    """Create temporary directory and clean up after."""
    temp_dir = tempfile.mkdtemp(*args, **kwargs)
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@pytest.fixture
def unix_socket(clamd_unix_config) -> clamd.ClamdUnixSocket:
    """Fixture for ClamdUnixSocket."""
    return clamd.ClamdUnixSocket(**clamd_unix_config)


@pytest.fixture
def unix_socket_timeout(clamd_unix_config) -> clamd.ClamdUnixSocket:
    """Fixture for ClamdUnixSocket with timeout."""
    conf = clamd_unix_config.copy()
    conf['timeout'] = 20
    return clamd.ClamdUnixSocket(**conf)


@pytest.fixture
def network_socket(clamd_network_config) -> clamd.ClamdNetworkSocket:
    """Fixture for ClamdNetworkSocket."""
    return clamd.ClamdNetworkSocket(**clamd_network_config)


@pytest.fixture
def eicar_file() -> Generator[str, None, None]:
    """Fixture creating a temporary file with EICAR test virus."""
    with tempfile.NamedTemporaryFile('wb', prefix="python-clamd", delete=False) as f:
        f.write(clamd.EICAR)
        f.flush()
        os.fchmod(f.fileno(), mine | other)
        yield f.name
    os.unlink(f.name)


@pytest.fixture
def eicar_files() -> Generator[Tuple[Union[str, bytes], List[str]], None, None]:
    """Fixture creating multiple EICAR files in a temp directory."""
    with mkdtemp(prefix="python-clamd") as d:
        files = []
        for i in range(10):
            path = os.path.join(str(d), f"file{i}")
            with open(path, 'wb') as f:
                f.write(clamd.EICAR)
                os.fchmod(f.fileno(), mine | other)
                files.append(path)
        os.chmod(d, mine | other | execute)
        yield d, files


@pytest.mark.xfail(reason="Working on...")
def test_version():
    import re
    assert hasattr(clamd, '__version__'), "No __version__ attribute"
    assert isinstance(clamd.__version__, str), f"__version__ must be string, got '{type(clamd.__version__)}'"
    assert re.match(r'^\d+(\.\d+)+(\.\d+)?$', clamd.__version__), f"Invalid version format: {clamd.__version__}"


class TestClamdUnixSocket:
    """Tests for ClamdUnixSocket."""

    def test_ping(self, unix_socket):
        """Test ping command."""
        assert unix_socket.ping() == 'PONG'

    def test_version(self, unix_socket):
        """Test version command."""
        assert unix_socket.version().startswith("ClamAV")

    def test_reload(self, unix_socket):
        """Test reload command."""
        assert unix_socket.reload() == 'RELOADING'

    def test_scan(self, unix_socket, eicar_file):
        """Test scanning a single file."""
        expected = {eicar_file: ('FOUND', 'Eicar-Test-Signature')}
        assert unix_socket.scan(eicar_file) == expected

    def test_scan_clean_file(self, unix_socket):
        """Test scanning a clean file."""
        with tempfile.NamedTemporaryFile('wb', prefix="clean") as f:
            f.write(b"clean file content")
            f.flush()
            os.chmod(f.name, 0o644)
            expected = {f.name: ('OK', None)}
            assert unix_socket.scan(f.name) == expected

    @pytest.mark.parametrize("filename", [
        "python-clamdλ",
        "python-clamd_unicode_测试",
        "python-clamd_normal",
    ])
    def test_unicode_scan(self, unix_socket, filename):
        """Test scanning files with Unicode names."""
        with tempfile.NamedTemporaryFile('wb', prefix=filename) as f:
            f.write(clamd.EICAR)
            f.flush()
            os.fchmod(f.fileno(), mine | other)
            expected = {f.name: ('FOUND', 'Eicar-Test-Signature')}
            assert unix_socket.scan(f.name) == expected

    def test_multiscan(self, unix_socket, eicar_files):
        """Test multiscan on directory."""
        d, files = eicar_files
        results = unix_socket.multiscan(d)
        for filepath in files:
            assert results[filepath] == ('FOUND', 'Eicar-Test-Signature')
        assert len(results) == len(files)

    def test_instream_eicar(self, unix_socket):
        """Test instream with EICAR virus."""
        expected = {'stream': ('FOUND', 'Eicar-Test-Signature')}
        assert unix_socket.instream(BytesIO(clamd.EICAR)) == expected

    def test_instream_clean(self, unix_socket):
        """Test instream with clean content."""
        assert unix_socket.instream(BytesIO(b"foo")) == {'stream': ('OK', None)}

    def test_instream_empty(self, unix_socket):
        """Test instream with empty content."""
        assert unix_socket.instream(BytesIO(b"")) == {'stream': ('OK', None)}

    def test_stats(self, unix_socket):
        """Test stats command."""
        stats = unix_socket.stats()
        assert "POOLS" in stats
        assert "STATE" in stats

    def test_contscan(self, unix_socket, eicar_file):
        """Test contscan command."""
        expected = {eicar_file: ('FOUND', 'Eicar-Test-Signature')}
        assert unix_socket.contscan(eicar_file) == expected

    def test_shutdown(self, unix_socket):
        """Test shutdown command (skip if not running as root)."""
        assert unix_socket.shutdown() is None

class TestClamdUnixSocketTimeout:
    """Tests for ClamdUnixSocket with timeout."""

    def test_timeout_set(self, unix_socket_timeout):
        """Test that timeout is properly set."""
        assert unix_socket_timeout.timeout == 20

    def test_ping_with_timeout(self, unix_socket_timeout):
        """Test ping with timeout."""
        assert unix_socket_timeout.ping() == 'PONG'


class TestClamdNetworkSocket:
    """Tests for ClamdNetworkSocket."""

    def test_ping(self, network_socket):
        """Test ping over network."""
        result = network_socket.ping()
        assert result == 'PONG'

    def test_version(self, network_socket):
        """Test version over network."""
        assert network_socket.version().startswith("ClamAV")

    def test_scan(self, network_socket, eicar_file):
        """Test scan over network."""
        expected = {eicar_file: ('FOUND', 'Eicar-Test-Signature')}
        assert network_socket.scan(eicar_file) == expected

    def test_instream(self, network_socket):
        """Test instream over network."""
        expected = {'stream': ('FOUND', 'Eicar-Test-Signature')}
        assert network_socket.instream(BytesIO(clamd.EICAR)) == expected


class TestErrors:
    """Tests for error conditions."""

    def test_cannot_connect_unix(self):
        """Test connection error with invalid Unix socket."""
        path = "/tmp/nonexistent_404.sock"
        with pytest.raises(clamd.ConnectionError, match=r"Error \d+ connecting") as exc_info:
            clamd.ClamdUnixSocket(path).ping()
        assert path in str(exc_info.value)

    def test_cannot_connect_network(self, clamd_network_config):
        """Test connection error with invalid network socket."""
        with pytest.raises(clamd.ConnectionError,
                           match=rf"Error \d+ connecting {clamd_network_config['host']}:9999") as exc_info:
            clamd.ClamdNetworkSocket(host=clamd_network_config['host'], port=9999).ping()
        assert f"Connection refused." in str(exc_info.value)

    def test_response_error(self, unix_socket):
        """Test response error handling."""
        with pytest.raises(clamd.ResponseError):
            unix_socket._parse_response("Invalid response")

    def test_scan_nonexistent_file(self, unix_socket):
        """Test scanning a non-existent file."""
        path = "/tmp/nonexistent_file_xyz123"
        result = unix_socket.scan(path)

        # Assert type
        assert isinstance(result, dict)
        assert len(result) == 1

        # Assert filename
        filename = list(result.keys())[0]
        assert filename == f"{path}: File path check failure"

        # Assert status and reason
        status, reason = result[filename]
        assert status == 'ERROR'
        assert reason == 'No such file or directory.'

    def test_multiscan_nonexistent_directory(self, unix_socket):
        """Test multiscan on non-existent directory."""
        path = "/tmp/nonexistent_dir_xyz123"
        result = unix_socket.multiscan(path)

        # Assert type
        assert isinstance(result, dict)
        assert len(result) == 1

        # Assert filename
        filename = list(result.keys())[0]
        assert filename == f"{path}: File path check failure"

        # Assert status and reason
        status, reason = result[filename]
        assert status == 'ERROR'
        assert reason == 'No such file or directory.'


class TestEICARConstant:
    """Tests for EICAR constant."""

    def test_eicar_content(self):
        """Test EICAR constant content."""
        assert clamd.EICAR == b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'

    def test_eicar_length(self):
        """Test EICAR constant length."""
        assert len(clamd.EICAR) == 68


class TestIntegration:
    """Integration tests."""

    def test_full_workflow(self, unix_socket):
        """Test complete workflow: ping, version, scan, instream."""
        # Ping
        assert unix_socket.ping() == 'PONG'

        # Version
        assert unix_socket.version().startswith("ClamAV")

        # Scan EICAR
        with tempfile.NamedTemporaryFile('wb') as f:
            f.write(clamd.EICAR)
            f.flush()
            os.chmod(f.name, 0o644)
            result = unix_socket.scan(f.name)
            assert result[f.name] == ('FOUND', 'Eicar-Test-Signature')

        # Instream
        result = unix_socket.instream(BytesIO(clamd.EICAR))
        assert result == {'stream': ('FOUND', 'Eicar-Test-Signature')}

    def test_multiple_connections(self, clamd_unix_config):
        """Test multiple simultaneous connections."""
        sockets = [
            clamd.ClamdUnixSocket(**clamd_unix_config),
            clamd.ClamdUnixSocket(**clamd_unix_config),
            clamd.ClamdUnixSocket(**clamd_unix_config)
        ]
        for sock in sockets:
            assert sock.ping() == 'PONG'
        for sock in sockets:
            sock._close_socket()


class TestMissing:
    def test_basic_command_error(self, unix_socket, monkeypatch):
        """Test _basic_command raises ResponseError."""
        monkeypatch.setattr(unix_socket, '_recv_response', lambda: 'ERROR Some error')
        with pytest.raises(clamd.ResponseError):
            unix_socket.ping()

    def test_instream_empty_response(self, unix_socket, monkeypatch):
        """Test instream with empty response."""
        monkeypatch.setattr(unix_socket, '_recv_response', lambda: '')
        result = unix_socket.instream(BytesIO(b"test"))
        assert result is None

    def test_network_socket_connection_error(self):
        """Test network socket connection error."""
        with pytest.raises(clamd.ConnectionError):
            clamd.ClamdNetworkSocket(host='nonexistent.host', port=3310).ping()

    def test_unix_socket_connection_error_permission(self):
        """Test Unix socket permission error."""
        with pytest.raises(clamd.ConnectionError, match=r"Error.*connecting"):
            clamd.ClamdUnixSocket(path="/root/clamd.ctl").ping()  # Permission denied
