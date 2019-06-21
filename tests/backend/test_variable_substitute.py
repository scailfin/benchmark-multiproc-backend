"""Test functionality of the multiprocess backend function that substitutes
referebces to variables in the workflow specifications commands.
"""

from unittest import TestCase

import os
import shutil

from benchtmpl.io.files.base import FileHandle
from benchtmpl.workflow.template.base import TemplateHandle
from benchtmpl.workflow.template.loader import DefaultTemplateLoader

import benchproc.backend.engine as mp
import benchtmpl.error as err


TEMPLATE_FILE = 'tests/files/multi-step-template.yaml'


class TestVariableSubstitution(TestCase):
    """Test utility function of the multiprocess backend engine."""
    def test_expand_parameters(self):
        """Test parameter expansion."""
        template = DefaultTemplateLoader().load(TEMPLATE_FILE)
        arguments = {
            'code': template.get_argument(
                identifier='code',
                value=FileHandle(filepath='code/runme.py')
            ),
            'names': template.get_argument(
                identifier='names',
                value=FileHandle(filepath='data/myfriends.txt')
            ),
            'sleeptime': template.get_argument(
                identifier='sleeptime',
                value=11
            ),
            'waittime': template.get_argument(
                identifier='waittime',
                value=22
            )
        }
        self.assertEqual(
            mp.get_commands(template=template, arguments=arguments),
            [
                'python "runme.py" --inputfile "data/names.txt" --outputfile "results/greetings.txt" --sleeptime 11',
                'wait 22',
                'python "code/eval.py" --inputfile "results/greetings.txt" --outputfile results.json'
            ]
        )
        # Default values
        arguments = {
            'names': template.get_argument(
                identifier='names',
                value=FileHandle(filepath='data/myfriends.txt')
            )
        }
        self.assertEqual(
            mp.get_commands(template=template, arguments=arguments),
            [
                'python "code/helloworld.py" --inputfile "data/names.txt" --outputfile "results/greetings.txt" --sleeptime 10',
                'wait 5',
                'python "code/eval.py" --inputfile "results/greetings.txt" --outputfile results.json'
            ]
        )
        # Error cases
        del template.workflow_spec['inputs']['parameters']['inputfile']
        with self.assertRaises(err.InvalidTemplateError):
            mp.get_commands(template=template, arguments=arguments)


if __name__ == '__main__':
    import unittest
    unittest.main()
