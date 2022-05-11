"""pytest fixtures for simplified testing."""
import pytest

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(aiida_profile_clean):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def diff_code(aiida_local_code_factory):
    """Get a diff code."""
    return aiida_local_code_factory(executable="diff", entry_point="diff")
