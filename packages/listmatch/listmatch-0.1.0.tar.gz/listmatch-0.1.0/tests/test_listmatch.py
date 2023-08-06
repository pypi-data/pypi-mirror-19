#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_listmatch
----------------------------------

Tests for `listmatch` module.
"""


from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import assert_that, is_not
import unittest

from listmatch import (
    concat,
    options,
    zero_or_more,
    one_or_more,
    maybe,
    atom
)


class ListMatchMatcher(BaseMatcher):
    def __init__(self, list):
        self.list = list

    def _matches(self, matcher):
        return matcher.match(self.list)

    def describe_to(self, description):
        description.append_text('matches list ') \
                   .append_text(self.list)


def matches(item):
    return ListMatchMatcher(item)


def is_a(x):
    return x == 'a'


def is_even(x):
    return x % 2 == 0


class TestListmatch(unittest.TestCase):
    def test_basic(self):
        assert_that(atom(is_a), matches(['a']))
        assert_that(atom(is_a), is_not(matches(['b'])))

        assert_that('a' + atom('b'), matches('ab'))
        assert_that('a' + atom('b'), is_not(matches('a')))

        assert_that(concat(), matches([]))
        assert_that(concat(), is_not(matches('a')))

        assert_that(concat(atom('a')), matches(['a']))

        assert_that(options(), is_not(matches([])))
        assert_that(options(), is_not(matches('a')))

        assert_that(options('a', 'b'), matches(['a']))
        assert_that(options('a', 'b'), is_not(matches(['c'])))

        assert_that(zero_or_more(is_even), matches([]))
        assert_that(zero_or_more(is_even), matches([0, 2, 4]))
        assert_that(zero_or_more(is_even), is_not(matches([0, 3, 4])))

        example = zero_or_more('a') + one_or_more('b' | ('c' + maybe('d')))
        assert_that(example, matches(['a', 'a', 'b', 'c', 'c', 'd']))
        assert_that(example, matches(['b', 'c', 'c', 'd']))
        assert_that(example, matches(['a', 'a', 'b', 'b', 'c', 'c', 'd']))
        assert_that(example, is_not(matches(['a', 'a', 'b', 'b', 'd'])))
        assert_that(example, is_not(matches(['a', 'a'])))
