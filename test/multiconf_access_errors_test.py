#!/usr/bin/python

# Copyright 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# This code is free for anybody to use

import unittest
from oktest import ok, test, fail, todo, dummy
from utils import lazy, config_error, lineno

from .. import ConfigRoot, ConfigItem, ConfigException
from ..decorators import nested_repeatables, named_as, repeat
from ..envs import Env, EnvGroup

prod = Env('prod')

def ce(line_num, *lines):
    return config_error(__file__, line_num, *lines)

class ErrorsTest(unittest.TestCase):
    @test("access undefined attribute")
    def _a(self):
        cr = ConfigRoot(prod, [prod])

        try:
            print cr.b
            fail ("Expected exception")
        except ConfigException as ex:
            ok (ex.message) == "ConfigRoot {\n} has no attribute 'b'"

    @test("find_contained_in(named_as) - not found")
    def _b(self):
        @named_as('someitems')
        @nested_repeatables('someitems')
        @repeat()
        class NestedRepeatable(ConfigItem):
            pass

        @named_as('someitemX')
        @nested_repeatables('someitems')
        class X(ConfigItem):
            pass

        @named_as('someitemY')
        class Y(ConfigItem):
            pass

        @nested_repeatables('someitems')
        class root(ConfigRoot):
            pass

        with root(prod, [prod], a=0) as cr:
            NestedRepeatable()
            with X() as ci:
                ci.a(prod=0)
                NestedRepeatable(id='a')
                with NestedRepeatable(id='b') as ci:
                    NestedRepeatable(id='c')
                    with X() as ci:
                        ci.a(prod=1)
                        with NestedRepeatable(id='d') as ci:
                            ci.a(prod=2)
                            with Y() as ci:
                                ci.a(prod=3)

        try:
            cr.someitemX.someitems['b'].someitemX.someitems['d'].someitemY.find_contained_in(named_as='notthere').a
            fail ("Expected exception")
        except ConfigException as ex:
            ok (ex.message) == "Could not find a parent container named as: 'notthere' in hieracy with names: ['someitems', 'someitemX', 'someitems', 'someitemX', 'root']"
