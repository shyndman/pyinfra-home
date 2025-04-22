# PyInfra v3 Project Notes

This document summarizes the discussions and decisions for setting up a PyInfra v3 project for home infrastructure management.

## Project Overview

- **Project Type**: PyInfra v3 for home infrastructure management
- **Package Structure**: uv-managed, with source in the src/home-infra folder
- **Linting**: Using ruff with `ruff check`
- **Formatting**: Using ruff with `ruff format`

## Target Environment

- **Primary Targets**: Local servers
- **Testing Environment**: Docker containers
- **Possible Future Use**: Docker image construction

## Authentication & First Boot

- **Authentication Method**: SSH keys
- **First Boot Process**:
  - Initial access via root password
  - Need to automate:
    - SSH daemon lockdown
    - User setup with SSH keys
    - Secure configuration

## Deployment Goals

Initial deployment will focus on:
- Consistent shell environment across servers
- Common tools installation:
  - zsh
  - ripgrep
  - fd
  - fzf
  - kitty-terminfo
  - starship
  - docker
- Tailscale setup for networking

## Inventory Structure

- **Multiple Groups**: Different server roles
- **Custom Configurations**: Each host may have unique configurations
- **Group-Based Configuration**: Different settings for different server groups

## Configuration Management

- **Configuration Files**: Will need to deploy files like compose.yml
- **Templates**: May use Jinja2 templates for generating configuration with host-specific values

## Deployment Workflow

- **Dependencies**: Operations may depend on results of previous operations
- **Execution Order**: Important for certain tasks
- **Conditional Execution**: Based on the state of the system

## Security Requirements

- **Secret Management**:
  - Using 1Password for secrets
  - Will integrate with the 1Password Python SDK
  - References to secrets in code, expanded during deployment

## Monitoring and Maintenance

- **Future Consideration**: Not immediate priority
- **Potential Solution**: Node Exporter for system metrics
- **Integration**: Can be added to deployment later

## Testing Strategy

- **Staging Environment**: Docker containers
- **Workflow**: Test deployments in containers before applying to real servers

## Rollback Strategy

- **Version Control Based**:
  - Check out previous version of infrastructure code
  - Deploy the previous version
  - System returns to previous state

## Custom Operations

- **Nala for APT**:
  - Create custom operations that use nala instead of apt
  - Bootstrap nala with `nala fetch --auto`
  - Implement operations similar to PyInfra's apt module

## Integration with Other Tools

- **Current Status**: No CI/CD pipelines or other automation needed
- **Future Consideration**: May integrate with other tools as needed

## Proposed Project Structure

```
home-infra/
├── inventories/
│   ├── production.py      # Your actual servers
│   └── docker_staging.py  # Docker containers for testing
├── group_data/
│   ├── all.py             # Common data for all hosts
│   ├── media.py           # Data for media servers
│   └── home_automation.py # Data for home automation
├── operations/
│   └── nala.py            # Custom nala operations
├── tasks/
│   ├── first_boot.py      # First boot configuration
│   ├── common.py          # Common setup for all hosts
│   ├── shell_env.py       # Shell environment setup
│   ├── docker.py          # Docker setup
│   └── tailscale.py       # Tailscale setup
├── templates/
│   ├── sshd_config.j2     # SSH daemon configuration
│   ├── zshrc.j2           # ZSH configuration
│   └── docker-compose.j2.yml # Docker compose template
├── deploy.py              # Main deployment entry point
└── requirements.txt       # Python dependencies
```

## Implementation Notes

### 1Password Integration

Will use the official 1Password Python SDK:
- GitHub: https://github.com/1Password/onepassword-sdk-python
- Integration with PyInfra through custom operations or helpers

### Node Exporter

- Prometheus exporter for hardware and OS metrics
- Can be deployed as part of the infrastructure
- Exposes metrics on port 9100 for Prometheus to scrape

### Rollback Strategy

- Using git for version control of infrastructure code
- Rollback by checking out previous version and redeploying
- Works well for idempotent and reversible operations
- May need additional strategies for data migrations or critical systems
