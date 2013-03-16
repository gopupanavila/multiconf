#!/usr/bin/python

# Copyright (c) 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# All rights reserved. This work is under a BSD license, see LICENSE.TXT.

import unittest
from oktest import fail, dummy

from .utils import config_error, lineno

from ..envs import EnvFactory, EnvException

ef = EnvFactory()

def ce(line_num, *lines):
    return config_error(__file__, line_num, *lines)

class EnvsTest(unittest.TestCase):

    def env_member_with_same_name_as_self_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                cc11 = ef.Env('cc11')
                errorline = lineno() + 1
                cc11 = ef.EnvGroup('cc11', cc11)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Can't have a member with my own name: 'cc11', members:  [Env('cc11')]"

    def group_member_with_same_name_as_self_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                cc21 = ef.Env('cc21')
                cc22 = ef.EnvGroup('cc22', cc21)
                errorline = lineno() + 1
                cc22 = ef.EnvGroup('cc22', cc22)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Can't have a member with my own name: 'cc22', members:  [EnvGroup('cc22') {\n     Env('cc21')\n}]"

    def repeated_direct_env_member_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                ff1 = ef.Env('ff1')
                errorline = lineno() + 1
                ff2 = ef.EnvGroup('ff2', ff1, ff1)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: Env('ff1') in EnvGroup('ff2') {\n\n}"

    def repeated_direct_group_member_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                gg1 = ef.Env('gg1')
                gg2 = ef.EnvGroup('gg2', gg1)
                errorline = lineno() + 1
                gg3 = ef.EnvGroup('gg3', gg2, gg2)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: EnvGroup('gg2') {\n     Env('gg1')\n} in EnvGroup('gg3') {\n\n}"

    def repeated_nested_env_member_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                hh1 = ef.Env('hh1')
                hh2 = ef.EnvGroup('hh2', hh1)
                errorline = lineno() + 1
                hh3 = ef.EnvGroup('hh3', hh1, hh2)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: Env('hh1') in EnvGroup('hh3') {\n\n}"

    def repeated_nested_env_member_reversed_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                ii1 = ef.Env('ii1')
                ii2 = ef.EnvGroup('ii2', ii1)
                errorline = lineno() + 1
                ii3 = ef.EnvGroup('ii3', ii2, ii1)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: Env('ii1') in EnvGroup('ii3') {\n\n}"

    def repeated_nested_group_member_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                jj1 = ef.Env('jj1')
                jj2 = ef.EnvGroup('jj2', jj1)
                jj3 = ef.EnvGroup('jj3', jj2)
                errorline = lineno() + 1
                jj4 = ef.EnvGroup('jj4', jj3, jj2)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: EnvGroup('jj2') {\n     Env('jj1')\n} in EnvGroup('jj4') {\n\n}"

    def repeated_nested_group_member_reversed_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                jj1 = ef.Env('jj1')
                jj2 = ef.EnvGroup('jj2', jj1)
                jj3 = ef.EnvGroup('jj3', jj2)
                errorline = lineno() + 1
                jj4 = ef.EnvGroup('jj4', jj2, jj3)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Repeated group member: EnvGroup('jj2') {\n     Env('jj1')\n} in EnvGroup('jj4') {\n\n}"

    def env_from_string_undefined_test(self):
        try:
            ef.env("undefined")
            fail ("Expected exception")
        except EnvException as ex:
            assert ex.message == "No such Env: 'undefined'"

    def group_from_string__undefined_test(self):
        try:
            ef.group("undefined")
            fail ("Expected exception")
        except EnvException as ex:
            assert ex.message == "No such EnvGroup: 'undefined'"

    def env_or_group_from_string_undefined_test(self):
        try:
            ef.env_or_group("undefined")
            fail ("Expected exception")
        except EnvException as ex:
            assert ex.message == "No such Env or EnvGroup: 'undefined'"

    def env_name_is_not_a_str_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                _e1 = ef.Env(1)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Env: 'name' must be instance of str, found: int"

    def env_name_is_empty_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                _e1 = ef.Env("")
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Env: 'name' must not be empty"


    def env_name_startswith_underscore_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                _e1 = ef.Env("_a")
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Env: 'name' must not start with '_', got: '_a'"

    def env_name_eq_default_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                _e1 = ef.Env("default")
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "Env: 'default' is a reserved name"

    def group_name_eq_default_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                e1 = ef.Env("e1")
                _g1 = ef.EnvGroup("default", e1)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "EnvGroup: 'default' is a reserved name"

    def no_group_members_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                gg2 = ef.EnvGroup('gg')
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "EnvGroup: No group members specified"

    def group_member_is_not_instanceof_env_test(self):
        try:
            with dummy.dummy_io('stdin not used') as d_io:
                _g = ef.EnvGroup('gg', 1)
                fail ("Expected exception")
        except EnvException as ex:
            sout, serr = d_io
            #assert serr == ce(errorline, "TODO")
            assert ex.message == "EnvGroup:  Group members args must be instance of 'Env' or 'EnvGroup', found: 1"
