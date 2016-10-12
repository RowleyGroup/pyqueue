#!/usr/bin/env python

from pbs_generator import Pbs, Modules, ShellCommands

modules = Modules().purge().load(['orca/3.0'])
commands = ShellCommands().cd('/work/foo/bar').orca('water.inp')
pbs = Pbs(modules, commands).wall_time(24)
print pbs