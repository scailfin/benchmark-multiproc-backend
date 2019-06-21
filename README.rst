===========================================================
Simple Workflow Engine for Reproducible Benchmark Templates
===========================================================

.. image:: https://api.travis-ci.org/scailfin/benchmark-multiproc-backend.svg?branch=master
   :target: https://travis-ci.org/scailfin/benchmark-multiproc-backend?branch=master

.. image:: https://coveralls.io/repos/github/scailfin/benchmark-multiproc-backend/badge.svg?branch=master
   :target: https://coveralls.io/github/scailfin/benchmark-multiproc-backend?branch=master

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://github.com/scailfin/benchmark-multiproc-backend/blob/master/LICENSE



About
=====

This repository contains the implementation of a simple workflow engine that is capable to execute `parameterized workflow specifications <https://github.com/scailfin/benchmark-templates>`_ for the *Reproducible Open Benchmarks for Data Analysis Platform (ROB)*.

The workflow engine runs each workflow step as a subprocess in Python.

**DISCLAIMER**: This engine is primarily intended for testing purposes. It is not recommended to be used as the workflow engine in production systems.
