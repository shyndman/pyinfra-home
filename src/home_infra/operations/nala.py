"""
Operations for managing packages with nala.

Nala is a frontend for libapt-pkg that aims to improve the experience of
using apt by providing a cleaner interface, faster downloads through
parallel downloading, and better error messages.

Note: Some type checking warnings remain due to incomplete type information
for the pyinfra API. These warnings do not affect functionality.
"""

from typing import Generator, List, Optional, Union

from pyinfra.api.host import Host
from pyinfra.api.operation import operation
from pyinfra.api.state import State
from pyinfra.facts.apt import AptSources, SimulateOperationWillChange
from pyinfra.facts.deb import DebPackage, DebPackages
from pyinfra.facts.files import File
from pyinfra.facts.server import Date


@operation()
def fetch(
    state: State,
    host: Host,
    auto: bool = False,
    country: Optional[str] = None,
    fetches: Optional[int] = None,
) -> Generator[str, None, None]:
    """
    Fetch fast mirrors to improve download speed.

    + auto: Run fetch uninteractively
    + country: Specify country to limit mirror search (2 letter ISO code)
    + fetches: Number of mirrors to fetch (defaults to 3 with --auto)
    """
    command = ["nala", "fetch"]

    if auto:
        command.append("--auto")

    if country:
        command.extend(["-c", country])

    if fetches:
        command.extend(["--fetches", str(fetches)])

    yield " ".join(command)


@operation()
def update(
    state: State, host: Host, cache_time: Optional[int] = None
) -> Generator[str, None, None]:
    """
    Updates nala repositories.

    + cache_time: cache updates for this many seconds
    """
    if cache_time:
        # If cache_time is provided, check when apt was last updated
        cache_info = host.get_fact(File, "/var/lib/apt/periodic/update-success-stamp")

        # Time in seconds since last apt update
        now = host.get_fact(Date)
        if cache_info and cache_info["mtime"]:
            time_since_update = now - cache_info["mtime"]
            # Convert timedelta to seconds for comparison
            if time_since_update.total_seconds() < cache_time:
                return

        yield "nala update -y"

        # Touch the update success stamp
        yield "mkdir -p /var/lib/apt/periodic"
        yield "touch /var/lib/apt/periodic/update-success-stamp"
    else:
        yield "nala update -y"


@operation()
def upgrade(state: State, host: Host) -> Generator[str, None, None]:
    """
    Upgrades all nala packages.
    """
    will_change = host.get_fact(SimulateOperationWillChange, "upgrade")
    if not will_change:
        return

    yield "nala upgrade -y"


@operation()
def full_upgrade(state: State, host: Host) -> Generator[str, None, None]:
    """
    Updates all nala packages, employing full-upgrade.
    """
    will_change = host.get_fact(SimulateOperationWillChange, "dist-upgrade")
    if not will_change:
        return

    yield "nala full-upgrade -y"


@operation()
def packages(
    state: State,
    host: Host,
    packages: Optional[Union[str, List[str]]] = None,
    present: bool = True,
    latest: bool = False,
    no_recommends: bool = False,
    allow_downgrades: bool = False,
    extra_install_args: str | None = None,
    extra_uninstall_args: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Install/remove/update packages with nala.

    + packages: list of packages to ensure
    + present: whether the packages should be installed
    + latest: whether to upgrade packages without a specified version
    + no_recommends: don't install recommended packages
    + allow_downgrades: allow downgrading packages with version (--allow-downgrades)
    + extra_install_args: additional arguments to the nala install command
    + extra_uninstall_args: additional arguments to the nala uninstall command

    Versions:
        Package versions can be pinned like apt: ``<pkg>=<version>``
    """
    if packages is None:
        packages = []
    elif isinstance(packages, str):
        packages = [packages]

    # No packages? Nothing to do
    if not packages:
        return

    # Get all installed packages
    current_packages: dict[str, str] = host.get_fact(DebPackages) or {}

    # Install packages
    if present:
        # Build the install command
        install_command = ["nala", "install", "-y"]

        if no_recommends:
            install_command.append("--no-install-recommends")

        if allow_downgrades:
            install_command.append("--allow-downgrades")

        if extra_install_args:
            install_command.append(extra_install_args)

        # Get packages that need installing
        need_installing: list[str] = []

        for package in packages:
            # If no version specified, and not latest, check if any version exists
            if "=" not in package and not latest:
                if package not in current_packages:
                    need_installing.append(package)
            # If version specified (or latest), we need to check against that
            else:
                if "=" in package:
                    name, version = package.split("=", 1)
                else:
                    name = package
                    version = None

                current_version = current_packages.get(name)

                # No version, or not the version we want?
                if not current_version or (version and current_version != version):
                    need_installing.append(package)
                # Package installed, but we want the latest and the fact tells us it's not
                elif not version and latest:
                    need_installing.append(package)

        if need_installing:
            yield " ".join(install_command + need_installing)

    # Remove packages
    else:
        # Build the uninstall command
        uninstall_command = ["nala", "remove", "-y"]

        if extra_uninstall_args:
            uninstall_command.append(extra_uninstall_args)

        # Get packages that need removing
        need_removing = []

        for package in packages:
            if "=" in package:
                name, _ = package.split("=", 1)
            else:
                name = package

            if name in current_packages:
                need_removing.append(name)

        if need_removing:
            yield " ".join(uninstall_command + need_removing)


@operation()
def deb(state: State, host: Host, src: str, present: bool = True) -> Generator[str, None, None]:
    """
    Add/remove .deb file packages.

    + src: filename or URL of the .deb file
    + present: whether or not the package should exist on the system

    Note:
        When installing, ``nala install -f`` will be run to install any unmet dependencies.

    URL sources with ``present=False``:
        If the ``.deb`` file isn't downloaded, pyinfra can't remove any existing
        package as the file won't exist until mid-deploy.
    """
    # If source is a URL
    if src.startswith(("http://", "https://")):
        # Generate a temp filename (with .deb extension to match Debian)
        # Use a simple temporary filename since we can't access state.get_temp_filename
        temp_filename = f"/tmp/pyinfra_deb_{src.split('/')[-1]}"

        # Download the file
        yield f"wget -O {temp_filename} {src}"

        # Override src with our temp file
        src = temp_filename

    # Get information about the package
    info = host.get_fact(DebPackage, src)

    # Will we install the package? Only if present and the package is not already installed
    install = present
    if info and present:
        current_packages: dict[str, str] = host.get_fact(DebPackages) or {}
        if info["name"] in current_packages and current_packages[info["name"]] == info["version"]:
            install = False

    # Install the package with nala -f
    if install:
        yield f"nala install -y {src}"
        yield "nala install -f -y"  # Install any missing dependencies

    # Remove the package
    elif not install and present is False:
        if info:
            yield f"nala remove -y {info['name']}"
        else:
            yield f"# No package information found for {src}"


@operation()
def repo(
    state: State,
    host: Host,
    src: str,
    present: bool = True,
    filename: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    Add/remove apt repositories.

    + src: apt source string eg ``deb http://X hardy main``
    + present: whether the repo should exist on the system
    + filename: optional filename to use ``/etc/apt/sources.list.d/<filename>.list``.
      By default uses ``/etc/apt/sources.list``.
    """
    # Get the source list
    apt_sources = host.get_fact(AptSources)

    if present:
        if src in apt_sources:
            return

        if filename:
            yield f"echo '{src}' > /etc/apt/sources.list.d/{filename}.list"
        else:
            yield f"echo '{src}' >> /etc/apt/sources.list"

    else:
        if src not in apt_sources:
            return

        if filename:
            # If we know the filename, use sed to remove the line
            yield (f"sed -i '/^{src}$/d' /etc/apt/sources.list.d/{filename}.list")
        else:
            # Otherwise, use sed to remove the line from sources.list
            yield f"sed -i '/^{src}$/d' /etc/apt/sources.list"
