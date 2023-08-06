# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from smonad.types import Functor
from smonad.types import Identity
from smonad.types import Maybe
from smonad.types import Failure, Success
from smonad.types import List

testee = [
    Identity,
    Maybe,
    Failure,
    Success,
    List,
]
test_range = range(-100, 100)
ids = [t.__name__ for t in testee]


def pytest_generate_tests(metafunc):
    if 'functor' in metafunc.funcargnames:
        metafunc.parametrize('functor', testee, ids=ids)


def test_functor_is_abstract():
    with pytest.raises(NotImplementedError):
        Functor(1).fmap(lambda a: a)


def test_fmap_functor_laws(functor):
    identity = lambda a: a
    f = lambda a: a + 1
    g = lambda a: a * 2
    f_g = lambda n: f(g(n))

    for n in test_range:
        ft = functor(n)
        # fmap id == id
        assert ft.fmap(identity) == identity(ft)
        # fmap (f . g) == fmap f . fmap g
        assert ft.fmap(f_g) == ft.fmap(g).fmap(f)
