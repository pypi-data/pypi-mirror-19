Hyphenate, using Frank Liang's algorithm.

This module provides a single function to hyphenate words. The
``hyphenate_word`` function takes a string (the word to hyphenate), and
returns a list of parts that can be separated by hyphens. For example::

    >>> from hyphenate import hyphenate_word
    >>> hyphenate_word('hyphenation')
    ['hy', 'phen', 'ation']
    >>> hyphenate_word('supercalifragilistic')
    ['su', 'per', 'cal', 'ifrag', 'ilis', 'tic']
    >>> hyphenate_word('project')
    ['project']

This code, originally written by Ned Batchelder in July 2007, is in the
public domain.



