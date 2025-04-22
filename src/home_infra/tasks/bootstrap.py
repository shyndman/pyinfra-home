"""
Bootstrap tasks for setting up nala on a fresh system.

Note: Some type checking warnings remain due to incomplete type information
for the pyinfra API. These warnings do not affect functionality.
"""

from pyinfra.api.deploy import deploy
from pyinfra.api.host import Host
from pyinfra.api.state import State
from pyinfra.operations import apt

from home_infra.operations import nala


@deploy("Install nala and fetch fast mirrors")
def install_nala(state: State, host: Host) -> None:
    """
    Install nala package manager and configure it with fast mirrors.

    This is a bootstrap task that should be run before using any nala operations.
    It installs nala using apt and then fetches the fastest mirrors automatically.
    """
    # Update apt repositories
    apt.update(
        name="Update apt repositories",
        cache_time=3600,
    )

    # Install nala
    apt.packages(
        name="Install nala package manager",
        packages=["nala"],
        update=False,  # We already updated above
    )

    # Fetch fast mirrors automatically
    nala.fetch(name="Fetch fast mirrors for nala", auto=True)
