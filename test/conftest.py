import os
from typing import Dict, Union

import pytest


@pytest.fixture(scope="session")
def clamd_test_config() -> Dict[str, Union[str, int]]:
    return {
        "host": os.getenv("TEST_CLAMD_HOST", "127.0.0.1"),
        "port": int(os.getenv("TEST_CLAMD_PORT", "3310")),
        "path": os.getenv("TEST_CLAMD_SOCKET", "/var/run/clamav/clamd.ctl"),
        "timeout": int(os.getenv("TEST_CLAMD_TIMEOUT", "30")),
    }


@pytest.fixture(scope="session")
def clamd_unix_config(clamd_test_config) -> Dict[str, Union[str, int]]:
    return {k: v for k, v in clamd_test_config.items() if k in ("path", "timeout")}


@pytest.fixture(scope="session")
def clamd_network_config(clamd_test_config) -> Dict[str, Union[str, int]]:
    return {k: v for k, v in clamd_test_config.items() if k in ("host", "port", "timeout")}
