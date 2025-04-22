"""
Configuration and fixtures for pytest.

This module contains configuration and fixtures that are available to all tests.
"""

from typing import Any, Dict, Generator

import pytest

from .pyinfra_test_utils import FactsDict, PyinfraTestHost, PyinfraTestState


@pytest.fixture
def pyinfra_state() -> PyinfraTestState:
    """
    Fixture that provides a PyinfraTestState instance.

    This fixture can be used in tests to get a fresh PyinfraTestState instance
    for each test.

    Returns:
        PyinfraTestState: A fresh PyinfraTestState instance.
    """
    return PyinfraTestState()


@pytest.fixture
def pyinfra_host(pyinfra_state: PyinfraTestState) -> PyinfraTestHost:
    """
    Fixture that provides a PyinfraTestHost instance.

    This fixture can be used in tests to get a fresh PyinfraTestHost instance
    for each test. The host is associated with the state provided by the
    pyinfra_state fixture.

    Args:
        pyinfra_state: The PyinfraTestState instance to associate with the host.

    Returns:
        PyinfraTestHost: A fresh PyinfraTestHost instance.
    """
    return PyinfraTestHost()


@pytest.fixture
def facts() -> Dict[str, Any]:
    """
    Fixture that provides an empty facts dictionary.

    This fixture can be used in tests to get a fresh facts dictionary for each
    test. The dictionary can be populated with facts for testing.

    Returns:
        Dict[str, Any]: An empty facts dictionary.
    """
    return {}


@pytest.fixture
def host_with_facts(facts: FactsDict) -> Generator[PyinfraTestHost, None, None]:
    """
    Fixture that provides a PyinfraTestHost instance with facts.

    This fixture can be used in tests to get a fresh PyinfraTestHost instance
    with facts for each test. The facts are provided by the facts fixture.

    Args:
        facts: The facts to associate with the host.

    Yields:
        PyinfraTestHost: A fresh PyinfraTestHost instance with facts.
    """
    host = PyinfraTestHost(facts=facts)
    yield host
