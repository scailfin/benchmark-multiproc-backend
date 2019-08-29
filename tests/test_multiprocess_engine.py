# This file is part of the Reproducible Open Benchmarks for Data Analysis
# Platform (ROB).
#
# Copyright (C) 2019 NYU.
#
# ROB is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Test functinality of the multiprocess backend."""

import os
import pytest
import time

from benchproc.engine import MultiProcessWorkflowEngine
from benchtmpl.io.files.base import FileHandle
from benchtmpl.workflow.parameter.value import TemplateArgument
from benchtmpl.workflow.template.repo import TemplateRepository

import benchtmpl.error as err


DIR = os.path.dirname(os.path.realpath(__file__))
DATA_FILE = os.path.join(DIR, './.files/names.txt')
TEMPLATE_FILE = os.path.join(DIR, './.files/template/template.yaml')
TEMPLATE_WITH_INVALID_CMD = os.path.join(DIR, './.files/template/template-invalid-cmd.yaml')
TEMPLATE_WITH_MISSING_FILE = os.path.join(DIR, './.files/template/template-missing-file.yaml')
UNKNOWN_FILE = os.path.join(DIR, './.files/.tmp/no/file/here')
WORKFLOW_DIR = os.path.join(DIR, './.files/template')


class TestMultiprocessWorkflowEngine(object):
    """Test executing workflows from templates using the multiprocess workflow
    engine.
    """

    def test_run_helloworld(self, tmpdir):
        """Execute the helloworld example."""
        repo = TemplateRepository(base_dir=os.path.join(str(tmpdir), 'repo'))
        template = repo.add_template(
            src_dir=WORKFLOW_DIR,
            template_spec_file=TEMPLATE_FILE
        )
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(DATA_FILE)
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=3
            )
        }
        engine_dir = os.path.join(str(tmpdir), 'engine')
        engine = MultiProcessWorkflowEngine(base_dir=engine_dir, run_async=True)
        # Run workflow asyncronously
        run_id, _ = engine.execute(template, arguments)
        while engine.get_state(run_id).is_active():
            time.sleep(1)
        state = engine.get_state(run_id)
        self.validate_run_result(state)
        # Remove run resources (can be called multiple times as long as the
        # task is not active)
        engine.remove_run(run_id)
        engine.remove_run(run_id)
        # Getting the state of a removed run raises an error
        with pytest.raises(err.UnknownRunError):
            engine.get_state(run_id)
        # Cancel run
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(DATA_FILE)
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=30
            )
        }
        run_id, _ = engine.execute(template, arguments)
        while engine.get_state(run_id).is_active():
            # Removing resources will raise an error
            with pytest.raises(RuntimeError):
                engine.remove_run(run_id)
            # Cancel the run
            engine.cancel_run(run_id)
            break
        with pytest.raises(err.UnknownRunError):
            engine.get_state(run_id)
        # Remove run resources does not raise an error now
        engine.remove_run(run_id)
        # Run workflow syncronously
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(DATA_FILE)
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=1
            )
        }
        engine = MultiProcessWorkflowEngine(base_dir=engine_dir, run_async=False)
        sync_run_id, state = engine.execute(template, arguments)
        assert run_id != sync_run_id
        self.validate_run_result(state)
        self.validate_run_result(state)
        state = engine.get_state(sync_run_id)
        # Remove run resources (can be called multiple times as long as the
        # task is not active)
        engine.remove_run(run_id)

    def test_run_with_invalid_cmd(self, tmpdir):
        """Execute the helloworld example with an invalid shell command."""
        # Execution fails if a file that is referenced by the workflow does not
        # exist in the created workspace
        repo = TemplateRepository(base_dir=os.path.join(str(tmpdir), 'repo'))
        template = repo.add_template(
            src_dir=WORKFLOW_DIR,
            template_spec_file=TEMPLATE_WITH_INVALID_CMD
        )
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(DATA_FILE)
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=3
            )
        }
        # Run workflow syncronously
        engine = MultiProcessWorkflowEngine(
            base_dir=os.path.join(str(tmpdir), 'engine'),
            run_async=False,
            verbose=True
        )
        sync_run_id, state = engine.execute(template, arguments)
        assert state.is_error()
        assert len(state.messages) > 0
        state = engine.get_state(sync_run_id)
        assert state.is_error()
        assert len(state.messages) > 0


    def test_run_with_missing_file(self, tmpdir):
        """Execute the helloworld example with a reference to a missing file."""
        # Execution fails if a file that is referenced by the workflow does not
        # exist in the created workspace
        repo = TemplateRepository(base_dir=os.path.join(str(tmpdir), 'repo'))
        template = repo.add_template(
            src_dir=WORKFLOW_DIR,
            template_spec_file=TEMPLATE_WITH_MISSING_FILE
        )
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(DATA_FILE)
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=3
            )
        }
        # Run workflow syncronously
        engine = MultiProcessWorkflowEngine(
            base_dir=os.path.join(str(tmpdir), 'engine'),
            run_async=False
        )
        sync_run_id, state = engine.execute(template, arguments)
        assert state.is_error()
        assert len(state.messages) > 0
        state = engine.get_state(sync_run_id)
        assert state.is_error()
        assert len(state.messages) > 0
        # An error is raised if the input file does not exist
        with pytest.raises(IOError):
            engine.execute(
                template=template,
                arguments={
                    'names': TemplateArgument(
                        parameter=template.get_parameter('names'),
                        value=FileHandle(UNKNOWN_FILE)
                    ),
                    'sleeptime': TemplateArgument(
                        parameter=template.get_parameter('sleeptime'),
                        value=3
                    )
                }
            )

    def validate_run_result(self, state):
        """Validate the results of a run of the helloworld workflow."""
        assert state.is_success()
        assert len(state.resources) == 1
        assert 'results/greetings.txt' in state.resources
        greetings = list()
        with open(state.resources['results/greetings.txt'].filepath, 'r') as f:
            for line in f:
                greetings.append(line.strip())
        assert len(greetings) == 2
        assert greetings[0] == 'Hello Alice!'
        assert greetings[1] == 'Hello Bob!'
