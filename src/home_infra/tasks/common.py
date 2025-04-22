"""
Common tasks for all hosts.

Note: Some type checking warnings remain due to incomplete type information
for the pyinfra API. These warnings do not affect functionality.
"""

from pyinfra.api.deploy import deploy
from pyinfra.api.host import Host
from pyinfra.api.state import State

from home_infra.operations import nala


@deploy("Install common packages")
def install_common_packages(state: State, host: Host) -> None:
    """
    Install common packages that should be present on all hosts.
    """
    # Update nala repositories
    nala.update(
        name="Update nala repositories",
        cache_time=3600,
    )

    # Install common packages
    nala.packages(
        name="Install common packages",
        packages=[
            "zsh",
            "ripgrep",
            "fd-find",
            "fzf",
            "kitty-terminfo",
            "docker.io",
        ],
    )

    # Install starship prompt
    nala.packages(name="Install starship prompt", packages=["curl", "ca-certificates"])

    # The starship installation requires a separate command
    # Using a raw command instead of yield to avoid return type issues
    from pyinfra.operations import server

    server.shell(
        name="Install starship prompt",
        commands=["curl -sS https://starship.rs/install.sh | sh -s -- --yes"],
    )
