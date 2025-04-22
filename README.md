# Home PyInfra

[![Tests](https://github.com/shyndman/home_infra/actions/workflows/tests.yml/badge.svg)](https://github.com/shyndman/home_infra/actions/workflows/tests.yml)
[![Lint](https://github.com/shyndman/home_infra/actions/workflows/lint.yml/badge.svg)](https://github.com/shyndman/home_infra/actions/workflows/lint.yml)

A PyInfra v3 project for managing home infrastructure.

## Overview

This project uses PyInfra v3 to automate the deployment and configuration of home infrastructure servers. It includes custom operations for using nala (a better apt frontend) and tasks for setting up common tools and configurations.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- uv (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/shyndman/home_infra.git
cd home_infra

# Set up the Python environment
uv venv
source .venv/bin/activate
uv sync
```

### Development

This project uses several tools to ensure code quality:

- **Type Checking**: Pyright provides static type checking, the same engine used by Pylance in VS Code. Run manually with:
  ```bash
  pyright src/
  ```
  Type checking is also integrated into the pre-commit hooks.

- **Linting**: Ruff is used for linting and code formatting. Run the linter with:
  ```bash
  ruff check .
  ```

  Format code with:
  ```bash
  ruff format .
  ```

- **Testing**: Pytest is used for running tests. Run the tests with:
  ```bash
  pytest
  ```

  To run tests with coverage reporting:
  ```bash
  pytest --cov=src --cov-report=term --cov-report=html
  ```

  The coverage report will be available in the `coverage_html_report` directory.

### Usage

### Bootstrap a New Server

To bootstrap a new server with nala and basic configuration:

```bash
pyinfra <inventory> deploy.py:bootstrap_deployment
```

### Set Up Common Packages

To install common packages and configurations on all hosts:

```bash
pyinfra <inventory> deploy.py:common_setup
```

### Testing with Docker

You can test deployments using Docker containers before applying to real servers:

```bash
pyinfra @docker_staging deploy.py:bootstrap_deployment
```

## Project Structure

- `src/home_infra/operations/`: Custom operations (e.g., nala.py)
- `src/home_infra/tasks/`: Deployment tasks
- `src/home_infra/inventories/`: Host inventories
- `src/home_infra/templates/`: Configuration templates
- `src/home_infra/deploy.py`: Main deployment entry point
- `tests/`: Test files
- `.github/workflows/`: CI/CD workflows

## Continuous Integration

This project uses GitHub Actions for continuous integration:

- **Tests**: Runs pytest with coverage reporting on every push to main and pull requests
- **Lint**: Runs ruff to check code style and formatting on every push to main and pull requests

The status of these workflows is displayed as badges at the top of this README.
