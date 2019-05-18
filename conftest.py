"""
For pytest 
initialise a text database and profile
"""
from __future__ import absolute_import
import tempfile
import shutil
import pytest
import os

from aiida.manage.fixtures import fixture_manager


def get_backend_str():
    """ Return database backend string.

    Reads from 'TEST_AIIDA_BACKEND' environment variable.
    Defaults to django backend.
    """
    from aiida.backends.profile import BACKEND_DJANGO, BACKEND_SQLA
    backend_env = os.environ.get('TEST_AIIDA_BACKEND')
    # pylint: disable=no-else-return
    if not backend_env:
        return BACKEND_DJANGO
    elif backend_env in (BACKEND_DJANGO, BACKEND_SQLA):
        return backend_env

    raise ValueError(
        "Unknown backend '{}' read from TEST_AIIDA_BACKEND environment variable"
        .format(backend_env))


@pytest.fixture(scope='session', autouse=True)
def aiida_profile():
    """setup a test profile for the duration of the tests"""
    with fixture_manager() as fixture_mgr:
        yield fixture_mgr


@pytest.fixture(scope='function', autouse=True)
def clear_database(aiida_profile):
    """clear the database after each test"""
    yield
    aiida_profile.reset_db()


@pytest.fixture(scope='function')
def new_workdir():
    """get a new temporary folder to use as the computer's workdir"""
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


@pytest.fixture(scope='function')
def aiida_computer(new_workdir):
    """get an AiiDA computer.
    
    :return: The computer node
    :rtype: :py:class:`aiida.orm.Computer`
    """
    from aiida.orm import Computer
    name = 'localhost-test'

    computer = Computer(
        name=name,
        description='localhost computer set up by aiida_diff tests',
        hostname=name,
        workdir=new_workdir,
        transport_type='local',
        scheduler_type='direct')
    computer.store()
    computer.configure()

    return computer


@pytest.fixture(scope='function')
def aiida_code(aiida_computer):
    """get an AiiDA code.
    
    :return: The code node
    :rtype: :py:class:`aiida.orm.Code`
    """
    from aiida.orm import Code
    from aiida_diff.tests import executables, get_path_to_executable
    entry_point = 'diff'

    try:
        executable = executables[entry_point]
    except KeyError:
        raise KeyError(
            "Entry point {} not recognized. Allowed values: {}".format(
                entry_point, list(executables.keys())))

    path = get_path_to_executable(executable)
    code = Code(
        input_plugin_name=entry_point,
        remote_computer_exec=[aiida_computer, path],
    )
    code.label = executable
    code.store()

    return code
