"""
Tests for home_infra operations.
"""

import json
import os
from typing import Any, Callable, cast
from unittest import TestCase

import pytest
from pyinfra.context import ctx_host, ctx_state

from home_infra.operations import nala

from .pyinfra_test_utils import (
    PyinfraTestState,
    assert_commands,
    create_host,
    parse_commands,
)

# These functions are now imported from pyinfra_test_utils


# Define a type for operation functions
OperationFunc = Callable[..., Any]


class TestNalaOperation(TestCase):
    """Base class for testing nala operations."""

    def setUp(self) -> None:
        self.state = PyinfraTestState()
        # Extract the operation name from the class name (e.g., TestNalaFetch -> fetch)
        self.operation_name = self.__class__.__name__.replace("TestNala", "").lower()
        self.test_dir = os.path.join("tests", "operations", f"nala.{self.operation_name}")

    @pytest.fixture(autouse=True)
    def _setup_state(self, pyinfra_state: PyinfraTestState) -> None:
        """Automatically use the pyinfra_state fixture."""
        self.state = pyinfra_state

    def run_operation_tests(self, operation_func: OperationFunc) -> None:
        """Run tests for the given operation function."""
        for filename in os.listdir(self.test_dir):
            if not filename.endswith(".json"):
                continue

            test_path = os.path.join(self.test_dir, filename)
            with open(test_path, "r") as f:
                test_data = json.load(f)

            # Create a host with the test facts
            host = create_host(facts=test_data.get("facts", {}))

            # Get the arguments
            args = test_data.get("args", [])
            kwargs = test_data.get("kwargs", {})

            # Run the operation's inner function directly to avoid the operation wrapper
            with ctx_state.use(self.state):
                with ctx_host.use(host):
                    # We know the _inner function returns a generator of strings
                    output_commands = list(
                        operation_func._inner(self.state, host, *args, **kwargs)  # type: ignore
                    )

            # Parse and check the commands
            commands = parse_commands(output_commands)
            assert_commands(commands, test_data["commands"])


class TestNalaFetch(TestNalaOperation):
    """Test the nala.fetch operation."""

    def test_fetch_operation(self) -> None:
        """Test the fetch operation with various test cases."""
        self.run_operation_tests(cast(OperationFunc, nala.fetch))


class TestNalaUpdate(TestNalaOperation):
    """Test the nala.update operation."""

    def test_update_operation(self) -> None:
        """Test the update operation with various test cases."""
        self.run_operation_tests(cast(OperationFunc, nala.update))


class TestNalaPackages(TestNalaOperation):
    """Test the nala.packages operation."""

    def test_packages_operation(self) -> None:
        """Test the packages operation with various test cases."""
        self.run_operation_tests(cast(OperationFunc, nala.packages))
