# This file is part of the Reproducible Open Benchmarks for Data Analysis
# Platform (ROB).
#
# Copyright (C) 2019 NYU.
#
# ROB is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Test functionality of the multiprocess backend function that substitutes
referebces to variables in the workflow specifications commands.
"""

import os
import pytest

from benchtmpl.io.files.base import FileHandle
from benchtmpl.workflow.parameter.value import TemplateArgument
from benchtmpl.workflow.template.base import TemplateHandle
from benchtmpl.workflow.template.loader import DefaultTemplateLoader

import benchproc.engine as mp
import benchtmpl.error as err


DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_FILE = os.path.join(DIR, './.files/multi-step-template.yaml')


class TestVariableSubstitution(object):
    """Test utility function of the multiprocess backend engine."""
    def test_expand_parameters(self):
        """Test parameter expansion."""
        template = DefaultTemplateLoader().load(TEMPLATE_FILE)
        arguments = {
            'code': TemplateArgument(
                parameter=template.get_parameter('code'),
                value=FileHandle(filepath='code/runme.py')
            ),
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(filepath='data/myfriends.txt')
            ),
            'sleeptime': TemplateArgument(
                parameter=template.get_parameter('sleeptime'),
                value=11
            ),
            'waittime': TemplateArgument(
                parameter=template.get_parameter('waittime'),
                value=22
            )
        }
        commands = mp.get_commands(template=template, arguments=arguments)
        CMDS = [
            'python "runme.py" --inputfile "data/names.txt" --outputfile "results/greetings.txt" --sleeptime 11',
            'wait 22',
            'python "code/eval.py" --inputfile "results/greetings.txt" --outputfile results.json'
        ]
        assert commands == CMDS
        # Default values
        arguments = {
            'names': TemplateArgument(
                parameter=template.get_parameter('names'),
                value=FileHandle(filepath='data/myfriends.txt')
            )
        }
        commands = mp.get_commands(template=template, arguments=arguments)
        CMDS = [
            'python "code/helloworld.py" --inputfile "data/names.txt" --outputfile "results/greetings.txt" --sleeptime 10',
            'wait 5',
            'python "code/eval.py" --inputfile "results/greetings.txt" --outputfile results.json'
        ]
        assert commands == CMDS
        # Error cases
        del template.workflow_spec['inputs']['parameters']['inputfile']
        with pytest.raises(err.InvalidTemplateError):
            mp.get_commands(template=template, arguments=arguments)
