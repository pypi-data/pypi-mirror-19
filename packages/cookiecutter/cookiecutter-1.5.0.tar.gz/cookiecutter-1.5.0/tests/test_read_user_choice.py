# -*- coding: utf-8 -*-

import click
import pytest

from cookiecutter.prompt import read_user_choice

OPTIONS = ['hello', 'world', 'foo', 'bar']


EXPECTED_PROMPT = """Select varname:
1 - hello
2 - world
3 - foo
4 - bar
Choose from 1, 2, 3, 4"""


@pytest.mark.parametrize('user_choice, expected_value', enumerate(OPTIONS, 1))
def test_click_invocation(mocker, user_choice, expected_value):
    choice = mocker.patch('click.Choice')
    choice.return_value = click.Choice(OPTIONS)

    prompt = mocker.patch('click.prompt')
    prompt.return_value = '{}'.format(user_choice)

    assert read_user_choice('varname', OPTIONS) == expected_value

    prompt.assert_called_once_with(
        EXPECTED_PROMPT,
        type=click.Choice(OPTIONS),
        default='1'
    )


def test_raise_if_options_is_not_a_non_empty_list():
    with pytest.raises(TypeError):
        read_user_choice('foo', 'NOT A LIST')

    with pytest.raises(ValueError):
        read_user_choice('foo', [])
