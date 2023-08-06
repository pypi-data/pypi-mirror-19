#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_remoter
----------------------------------

Tests for `remoter` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

from remoter import remoter
from remoter import cli


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
