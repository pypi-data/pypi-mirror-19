"""
    pai_parser.slicer
    ~~~~~~~~~~~~~~~~~

    Module for creating slices from iterables.
"""

import itertools


__all__ = ['SliceIterableEmpty', 'SliceIterableExhausted', 'iter_slice']


class SliceIterableEmpty(Exception):
    """
    Raised when attempting to slice an iterable that has no items.
    """


class SliceIterableExhausted(Exception):
    """
    Raised when an iterable is exhausted before the expected number of items has been sliced.
    """


def iter_slice(iterable, n, slice_cls=tuple):
    """
    Attempt to consume N items from the given iterable.

    :param iterable: Iterable to consume
    :param n: Number of items to consume from iterable
    :param slice_cls: Type to store the sliced items
    :return: An N-element collection of 'slice_cls' type.
    """
    # Attempt to consume 'n' items from the iterable.
    items = slice_cls(itertools.islice(iterable, n))

    if not items:
        raise SliceIterableEmpty()

    if len(items) < n:
        raise SliceIterableExhausted('Insufficient items; got {}, expected {}'.format(len(items), n))

    return items
