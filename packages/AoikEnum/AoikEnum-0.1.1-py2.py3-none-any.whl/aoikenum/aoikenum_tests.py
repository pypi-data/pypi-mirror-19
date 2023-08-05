# coding: utf-8
"""
This module contains tests.
"""
from __future__ import absolute_import

# External imports
import pytest

# Internal imports
from aoikenum import enum


def test_enum_case_int():
    """
    Test `enum` class decorator for int enumeration class.
    """
    # Create enumeration class
    @enum
    class Value(int):
        """
        Enumeration class.
        """

        ONE = 1
        TWO = 2

    # ----- Use enumeration instance -----
    assert Value.ONE == 1
    assert Value.ONE.name == 'ONE'
    assert repr(Value.ONE) == 'ONE'

    assert Value.TWO == 2
    assert Value.TWO.name == 'TWO'
    assert repr(Value.TWO) == 'TWO'

    # ----- Create enumeration instance from enumeration value -----
    one = Value(1)
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value(2)
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from enumeration instance -----
    one = Value(Value.ONE)
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value(Value.TWO)
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from invalid value -----
    with pytest.raises(ValueError) as exc_info:
        Value(0)

    assert exc_info.value.args[0] == (
        'Invalid value: 0'
        '\nValid values:'
        '\nValue.ONE == 1'
        '\nValue.TWO == 2'
    )


def test_enum_case_float():
    """
    Test `enum` class decorator for float enumeration class.
    """
    # Create enumeration class
    @enum
    class Value(float):
        """
        Enumeration class.
        """

        ONE = 1.0
        TWO = 2.0

    # ----- Use enumeration instance -----
    assert Value.ONE == 1.0
    assert Value.ONE.name == 'ONE'
    assert repr(Value.ONE) == 'ONE'

    assert Value.TWO == 2.0
    assert Value.TWO.name == 'TWO'
    assert repr(Value.TWO) == 'TWO'

    # ----- Create enumeration instance from enumeration value -----
    one = Value(1.0)
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value(2.0)
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from enumeration instance -----
    one = Value(Value.ONE)
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value(Value.TWO)
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from invalid value -----
    with pytest.raises(ValueError) as exc_info:
        Value(0)

    assert exc_info.value.args[0] == (
        'Invalid value: 0'
        '\nValid values:'
        '\nValue.ONE == 1.0'
        '\nValue.TWO == 2.0'
    )


def test_enum_case_str():
    """
    Test `enum` class decorator for str enumeration class.
    """
    # Create enumeration class
    @enum
    class Value(str):
        """
        Enumeration class.
        """

        ONE = '1'
        TWO = '2'

    # ----- Use enumeration instance -----
    assert Value.ONE == '1'
    assert Value.ONE.name == 'ONE'
    assert repr(Value.ONE) == 'ONE'

    assert Value.TWO == '2'
    assert Value.TWO.name == 'TWO'
    assert repr(Value.TWO) == 'TWO'

    # ----- Create enumeration instance from enumeration value -----
    one = Value('1')
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value('2')
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from enumeration instance -----
    one = Value(Value.ONE)
    assert one == Value.ONE
    assert one.name == 'ONE'
    assert repr(one) == 'ONE'

    two = Value(Value.TWO)
    assert two == Value.TWO
    assert two.name == 'TWO'
    assert repr(two) == 'TWO'

    # ----- Create enumeration instance from invalid value -----
    with pytest.raises(ValueError) as exc_info:
        Value('0')

    assert exc_info.value.args[0] == (
        "Invalid value: '0'"
        '\nValid values:'
        "\nValue.ONE == '1'"
        "\nValue.TWO == '2'"
    )
