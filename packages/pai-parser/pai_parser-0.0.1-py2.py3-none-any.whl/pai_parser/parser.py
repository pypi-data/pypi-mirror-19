"""
    pai_parser.parser
    ~~~~~~~~~~~~~~~~~

    Module for parsing shell-safe strings into objects.
"""

from pai_parser import grouper, tokenizer


__all__ = ['parse', 'parse_gen']


DEFAULT_RTL = False
DEFAULT_VISITOR_INTERFACE_METHODS = ['supports', 'visit']


class NullVisitor:
    """
    A simple visitor that just yields back unmodified token groups of size 1.
    """

    @staticmethod
    def supports(group_size, rtl):
        return True

    @staticmethod
    def visit(tokens, group_size, rtl, parent=None):
        return next(tokens, None)


def parse(data, visitor=NullVisitor, delimiter=tokenizer.DEFAULT_DELIMITER,
          group_size=grouper.DEFAULT_GROUP_SIZE, rtl=DEFAULT_RTL):
    """
    Create a list of nodes created by the visitor from the parsed data string.

    When using `rtl=False`, the data stream is lazy evaluated. When using `rtl=True`, the data stream will
    be evaluated and stored in memory before fed into the visitor. This is an artifact of not being able to
    lazy-evaluate an iterable in reverse order.

    :param data: String to parse
    :param visitor: Object that implements the 'visitor interface' to create nodes from parsed token groups
    :param delimiter: Delimiter to split on; Default: ':'
    :param group_size: Size of each group; Default: 1
    :param rtl: Flag indicating if data should be parsed right-to-left; Default: False
    :return: List of nodes created by visitor
    """
    return list(parse_gen(data, visitor, delimiter, group_size, rtl))


def parse_gen(data, visitor=NullVisitor, delimiter=tokenizer.DEFAULT_DELIMITER,
              group_size=grouper.DEFAULT_GROUP_SIZE, rtl=DEFAULT_RTL):
    """
    Generator function that yields nodes created by the visitor from the parsed data string.

    When using `rtl=False`, the data stream is lazy evaluated. When using `rtl=True`, the data stream will
    be evaluated and stored in memory before fed into the visitor. This is an artifact of not being able to
    lazy-evaluate an iterable in reverse order.

    :param data: String to parse
    :param visitor: Object that implements the 'visitor interface' to create nodes from parsed token groups
    :param delimiter: Delimiter to split on; default: ":"
    :param group_size: Size of each group; default: 1
    :param rtl: Flag indicating if data should be parsed right-to-left; Default: False
    :return: Yields nodes created by visitor
    """
    # Check the visitor object implements an interface based on our expectations.
    if not _is_visitor(visitor):
        raise ValueError('object does not implement the visitor interface')

    # Check the visitor object supports the given parse configuration.
    if not visitor.supports(group_size, rtl):
        raise ValueError('visitor does not support group_size and/or rtl')

    # Create iterator that yields token groups in order (conditionally right-to-left).
    tokens = tokenizer.tokenize_iter(data, delimiter)
    if group_size:
        tokens = grouper.group_gen(tokens, group_size)
    if rtl:
        tokens = reversed(list(tokens))

    node = None

    # Continue visiting nodes until we've exhausted all token groups.
    while True:
        node = visitor.visit(tokens, group_size, rtl, node)
        if not node:
            break
        yield node


def _is_visitor(obj, methods=DEFAULT_VISITOR_INTERFACE_METHODS):
    """
    Check if object implements the "visitor" interface.

    :param obj: Object to check
    :param methods: Iterable of method names the object must implement
    :return: `True` if implements interface, `False` otherwise
    """
    return all(callable(getattr(obj, method_name, None)) for method_name in methods)
