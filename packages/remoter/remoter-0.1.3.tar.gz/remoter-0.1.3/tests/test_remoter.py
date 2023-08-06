#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_remoter
----------------------------------

Tests for `remoter` module.
"""
import pytest

from click.testing import CliRunner

from remoter import cli
from remoter import config
from . import server


@pytest.fixture(scope="module")
def ssh_server():
    with server.Server() as s:
        yield s


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0


def test_connect_and_pwd(ssh_server):
    conf = config.Config('tests/samples/sample.yml')
    out = conf.run()
    assert len(out) > 0


def test_command_line_tasks_run(ssh_server):
    runner = CliRunner()
    result = runner.invoke(cli.main, ['--file', 'tests/samples/sample.yml', 'tasks', 'run'])
    assert result.exit_code == 0
