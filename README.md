# Home PyInfra

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
