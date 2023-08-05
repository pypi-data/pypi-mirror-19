"""
    pai_parser.grouper
    ~~~~~~~~~~~~~~~~~~

    Module for creating child groups from iterables.
"""

import itertools


__all__ = ['group', 'group_gen', 'GroupSizeInconsistency']


DEFAULT_GROUP_SIZE = 1


class GroupSizeInconsistency(Exception):
    """
    Exception raised when the number of items consumed from an iterable is not a multiple
    of the specified group size.
    """


def group(iterable, n=DEFAULT_GROUP_SIZE):
    """
    Create a list of N-element tuples from the given iterator.

    :param iterable: Iterable that yields items
    :param n: Size of each group; default: 1
    :return: List of N-element tuples
    """
    return list(group_gen(iterable, n))


def group_gen(iterable, n=DEFAULT_GROUP_SIZE):
    """
    Generator function that yields N-element tuples from the given iterator.

    Raises a :class:`~ValueError` exception when the number of items produced from the iterator is not
    a multiple of N.

    :param iterable: Iterable that yields items
    :param n: Size of each group; default: 1
    :return: Yields N-element tuples until the iterator is exhausted
    """
    if n < 0:
        raise ValueError('n must be greater than zero')

    for grp in itertools.zip_longest(*(iter(iterable),) * n):
        if grp[-1] is None:
            raise GroupSizeInconsistency('iterable can not be split into groups of {}'.format(n))
        yield grp
