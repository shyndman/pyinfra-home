# Testing Home Infrastructure Operations

This directory contains tests for the home infrastructure operations.

## Test Structure

The tests are organized as follows:

```
tests/
├── __init__.py
├── conftest.py                # Test fixtures and configuration
├── operations/
│   ├── __init__.py
│   ├── nala.fetch/
│   │   ├── fetch_auto.json
│   │   ├── fetch_with_all_options.json
│   │   ├── fetch_with_country.json
│   │   └── fetch_with_fetches.json
│   ├── nala.packages/
│   │   ├── add_package.json
│   │   └── remove_package.json
│   └── nala.update/
│       ├── update_cached.json
│       └── update_nocache.json
├── pyinfra_test_utils.py     # Test utilities for pyinfra operations
├── README.md                 # This file
└── test_operations.py        # Test runner for operations
```

## Test Cases

Each operation has a directory under `tests/operations/` named after the operation (e.g., `nala.fetch`). Inside each directory, there are JSON files that define test cases.

Each test case JSON file has the following structure:

```json
{
  "args": [],                 // Positional arguments to pass to the operation
  "kwargs": {                 // Keyword arguments to pass to the operation
    "auto": true
  },
  "facts": {                  // Facts to mock on the host
    "DebPackages": {}
  },
  "commands": [               // Expected commands that should be generated
    "nala fetch --auto"
  ]
}
```

## Running Tests

To run all tests:

```bash
python -m pytest
```

To run tests for a specific operation:

```bash
python -m pytest tests/test_operations.py::TestNalaFetch
```

To run tests with verbose output:

```bash
python -m pytest -v
```

To run tests with coverage reporting (using the configuration in pyproject.toml):

```bash
python -m pytest --cov=src --cov-report=term --cov-report=html
```

To run tests and exclude slow tests:

```bash
python -m pytest -m "not slow"
```

## Adding New Tests

To add tests for a new operation:

1. Create a directory for the operation under `tests/operations/` (e.g., `tests/operations/nala.new_operation/`)
2. Create JSON test case files in the directory
3. Add a test class in `tests/test_operations.py`:

```python
class TestNalaNewOperation(TestNalaOperation):
    """Test the nala.new_operation operation."""

    def test_new_operation(self):
        """Test the new_operation with various test cases."""
        self.run_operation_tests(nala.new_operation)
```

## Test Utilities

The `pyinfra_test_utils.py` file contains utilities for testing operations, including:

- `PyinfraTestState`: A stub for the pyinfra State class
- `PyinfraTestHost`: A stub for the pyinfra Host class
- `create_host()`: A function to create a host with mocked facts
- `parse_commands()`: A function to parse commands into a JSON-serializable format
- `assert_commands()`: A function to assert that commands match the expected commands

## Test Fixtures

The `conftest.py` file contains fixtures that are available to all tests:

- `pyinfra_state`: A fixture that provides a PyinfraTestState instance
- `pyinfra_host`: A fixture that provides a PyinfraTestHost instance
- `facts`: A fixture that provides an empty facts dictionary
- `host_with_facts`: A fixture that provides a PyinfraTestHost instance with facts
