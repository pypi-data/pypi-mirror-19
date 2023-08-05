"""
    pai_parser.tokenizer
    ~~~~~~~~~~~~~~~~~~~~

    Module for parsing strings into a collection of tokens.
"""

import shlex


__all__ = ['tokenize', 'tokenize_iter']


DEFAULT_DELIMITER = ':'


def tokenize(data, delimiter=DEFAULT_DELIMITER):
    """
    Create a list of tokens parsed from the given data string.

    :param data: String to parse
    :param delimiter: Delimiter to split on; default: ":"
    :return: List containing all tokens
    """
    return list(tokenize_iter(data, delimiter))


def tokenize_iter(data, delimiter=DEFAULT_DELIMITER):
    """
    Create an iterator that yields tokens parsed from given data string.

    :param data: String to parse
    :param delimiter: Delimiter to split on; default: ":"
    :return: Object that implements the iterator protocol
    """
    return iter(_lexer(data, delimiter))


def _lexer(data, delimiter=DEFAULT_DELIMITER):
    """
    Create a :class:`~shlex.shlex` instance used to parse a delimited, positional argument string.

    :param data: String to parse
    :param delimiter: Delimiter to split on; default: ":"
    :return: :class:`~shlex.shlex` instance of parsed data string
    """
    if isinstance(data, bytes):
        data = data.decode('utf-8')
    if not isinstance(data, str):
        raise ValueError('Expected bytes/str; got {}'.format(type(data)))

    lexer = shlex.shlex(data)
    lexer.whitespace = delimiter
    lexer.whitespace_split = True

    return lexer
