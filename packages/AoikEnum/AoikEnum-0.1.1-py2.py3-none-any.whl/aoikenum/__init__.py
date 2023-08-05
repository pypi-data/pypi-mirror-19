# coding: utf-8
"""
Package.
"""
from __future__ import absolute_import

# Local imports
from . import aoikenum as _aoikenum


# Support usage like:
# `from aoikenum import enum`
# instead of:
# `from aoikenum.aoikenum import enum`
#
# The use of `getattr` aims to bypass `pydocstyle`'s `__all__` check.
#
# For `aoikenum.aoikenum`'s each public attribute name
for key in getattr(_aoikenum, '__all__'):
    # Store the attribute in this module
    globals()[key] = getattr(_aoikenum, key)

# Delete the module reference
del _aoikenum
