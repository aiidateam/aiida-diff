""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import os
import aiida_diff.tests as tests
import pytest


# pylint: disable=unused-argument
@pytest.mark.process_execution
def test_process(new_database, new_workdir):
    """Test running a calculation
    note this does not test that the expected outputs are created of output parsing"""
    from aiida.plugins import DataFactory, CalculationFactory
    from aiida.engine import run_get_node

    # get code
    code = tests.get_code(entry_point='diff')

    # Prepare input parameters
    DiffParameters = DataFactory('diff')
    parameters = DiffParameters({'ignore-case': True})

    from aiida.orm import SinglefileData
    file1 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file1.txt'))
    file2 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file2.txt'))

    # set up calculation
    options = {
        "resources": {
            "num_machines": 1,
            "num_mpiprocs_per_machine": 1,
        },
        "max_wallclock_seconds": 30,
    }

    inputs = {
        'code': code,
        'parameters': parameters,
        'file1': file1,
        'file2': file2,
        'metadata': {
            'options': options,
            'label': "aiida_diff test",
            'description': "Test job submission with the aiida_diff plugin",
        },
    }

    _result, node = run_get_node(CalculationFactory('diff'), **inputs)

    print(node.outputs)
