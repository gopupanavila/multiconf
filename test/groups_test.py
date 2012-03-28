# Copyright 2012 Lars Hupfeldt Nielsen, Hupfeldt IT
# This code is free for anybody to use

import sys
sys.path.append('../..')

from multiconf.multiconf import ConfigRoot, ConfigItem
from multiconf.multiconf import Env, EnvGroup

prod = Env('prod')
dev2ct = Env('dev2CT')
dev2st = Env('dev2ST')
g_dev = EnvGroup('g_dev', dev2st, dev2ct)

valid_envs = [g_dev, prod]

def config(env):
    with ConfigRoot(env, valid_envs) as conf:
        conf.prod.a = "hello"
        conf.g_dev.a = "hi"
        print 'conf.a:', conf.a
    
        with ConfigItem(repeat=True) as c:
            c.prod.a = "hello nested"
            c.g_dev.a = "hi nested"

        return conf

def test(env):
    conf = config(env)
    
    print "----", env, "----"
    print 'conf.a', conf.a
    print 'conf.ConfigItems[0].a', conf.ConfigItems[0].a
    print

test(prod)
test(dev2ct)
