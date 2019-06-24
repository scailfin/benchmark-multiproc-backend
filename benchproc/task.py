# This file is part of the Reproducible Open Benchmarks for Data Analysis
# Platform (ROB).
#
# Copyright (C) 2019 NYU.
#
# ROB is free software; you can redistribute it and/or modify it under the
# terms of the MIT License; see LICENSE file for more details.

"""Methods to execute workflows that are sequences of shell commands."""

import subprocess
import traceback

import benchtmpl.workflow.state as wf


def run(identifier, commands, run_dir, verbose=False):
    """Sequential execution of all steps in the workflow commands list.

    Parameters
    ----------
    identifier: string
        Unique task identifier
    commands: list(string)
        List of commands. Each command is a string that represents a shell
        command
    run_dir: string
        Path to working directory for the task
    verbose: bool, optional
        Print command string to STDOUT if set to True

    Returns
    -------
    string, string, list(string)
    """
    for cmd in commands:
        # Print command if verbose
        if verbose:
            print(cmd)
        try:
            # Each command is expected to be a shell command
            proc = subprocess.run(
                cmd,
                cwd=run_dir,
                shell=True,
                capture_output=True
            )
            if proc.returncode != 0:
                # Return error state. Include STDERR in result
                messages = list()
                messages.append(proc.stderr)
                return identifier, wf.STATE_ERROR, messages
        except Exception as ex:
            # Return error state. Include exception and traceback in result
            messages = list()
            messages.append(str(ex))
            messages.append(traceback.format_exc())
            return identifier, wf.STATE_ERROR, messages
    # Workflow executed successfully
    return identifier, wf.STATE_SUCCESS, list()
