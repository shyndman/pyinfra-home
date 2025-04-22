"""
Test utilities for pyinfra operations.

This module provides stub classes for testing pyinfra operations without
having to mock every attribute individually.
"""

from typing import Any, Dict, List, Optional, Set, Tuple, Type, TypeVar

T = TypeVar("T")

# Define type aliases for better readability
FactsDict = Dict[str, Any]
CommandsList = List[str]


class PyinfraTestConfig:
    """A complete stub for pyinfra Config."""

    def __init__(self):
        # Global arguments
        self.SUDO = False
        self.SUDO_USER = None
        self.USE_SUDO_LOGIN = False
        self.SUDO_PASSWORD = None
        self.PRESERVE_SUDO_ENV = False
        self.SU_USER = None
        self.USE_SU_LOGIN = False
        self.PRESERVE_SU_ENV = False
        self.SU_SHELL = None
        self.DOAS = False
        self.DOAS_USER = None
        self.SHELL = "/bin/bash"
        self.COMMAND = None
        self.ENV = {}
        self.IGNORE_ERRORS = False
        self.PARALLEL = False


class PyinfraTestState:
    """A complete stub for pyinfra State."""

    def __init__(self) -> None:
        self.inventory = None
        self.config = PyinfraTestConfig()
        self.in_deploy = False
        self.deploy_name: Optional[str] = None
        self.deploy_kwargs: Dict[str, Any] = {}
        self.active = True
        self.op_meta: Dict[str, Any] = {}
        self.is_executing = False
        self.ops: Dict[str, Any] = {}

    def should_check_for_changes(self) -> bool:
        """Mock method that always returns False."""
        return False

    def get_meta_for_host(self, host: "PyinfraTestHost") -> "PyinfraTestHostMeta":
        """Mock method that returns a host meta object."""
        return PyinfraTestHostMeta()

    def set_op_data_for_host(
        self, host: "PyinfraTestHost", op_hash: str, op_data: Any
    ) -> None:
        """Mock method that does nothing."""
        pass


class PyinfraTestHostData:
    """A stub for host data."""

    def __init__(self):
        pass


class PyinfraTestHostMeta:
    """A stub for host meta."""

    def __init__(self):
        self.ops = 0
        self.ops_change = 0
        self.ops_no_change = 0


class PyinfraTestHost:
    """A complete stub for pyinfra Host."""

    def __init__(self, facts: Optional[FactsDict] = None) -> None:
        self.facts: FactsDict = facts or {}
        self.noop_description: Optional[str] = None
        self.in_op: bool = False
        self.in_deploy: bool = False
        self.name: str = "test_host"
        self.host_data: Dict[str, Any] = {}
        self.data = PyinfraTestHostData()
        self.current_deploy_kwargs: Dict[str, Any] = {}
        self.current_deploy_name: Optional[str] = None
        self.current_deploy_data: Dict[str, Any] = {}
        self.current_op_meta: Dict[str, Any] = {}
        self.op_hash_order: List[str] = []
        self.loop_position: Optional[int] = None
        self.op_hashes: Set[str] = set()

    def get_fact(self, fact_cls: Any, *args: Any) -> Any:
        """Get a fact from this host."""
        if args:
            key = f"{fact_cls.__name__}:{args[0]}"
            return self.facts.get(key)
        return self.facts.get(fact_cls.__name__)


def create_host(facts: Optional[FactsDict] = None) -> PyinfraTestHost:
    """Create a PyinfraTestHost with the given facts."""
    return PyinfraTestHost(facts=facts)


def parse_commands(commands: List[str]) -> List[str]:
    """Parse commands into a JSON-serializable format."""
    json_commands: List[str] = []
    for command in commands:
        json_commands.append(command.strip())
    return json_commands


def assert_commands(commands: List[str], wanted_commands: List[str]) -> None:
    """Assert that commands match the expected commands."""
    try:
        assert commands == wanted_commands
    except AssertionError as e:
        import json

        print()
        print("--> COMMANDS OUTPUT:")
        print(json.dumps(commands, indent=4))
        print("--> TEST WANTS:")
        print(json.dumps(wanted_commands, indent=4))
        raise e


class YamlTest(type):
    """Metaclass that creates test methods from YAML files."""

    def __new__(
        mcs, name: str, bases: Tuple[Type[Any], ...], attrs: Dict[str, Any]
    ) -> Type[Any]:
        cls = super(YamlTest, mcs).__new__(mcs, name, bases, attrs)
        return cls
