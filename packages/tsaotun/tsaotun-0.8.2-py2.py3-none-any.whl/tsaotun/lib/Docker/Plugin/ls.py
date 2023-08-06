"""This module contains `tsaotun plugin ls` class"""

from collections import defaultdict
import pystache
from pytabwriter import TabWriter

from .command import Command
from ....lib.Plugin.loader import Loader

class Ls(Command):
    """This class implements `tsaotun plugin ls` command"""

    name = "plugin ls"
    require = []

    defaultTemplate = '{{Plugin}}\t{{Enabled}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        tw = TabWriter()
        if args["format"] is None:
            tw.padding = [14]
            fm = self.defaultTemplate
            tw.writeln(
                "PLUGIN NAME\tENABLED")
        else:
            fm = args["format"]
        del args["format"]

        if args["filters"]:
            filters = args["filters"]
            args["filters"] = []
            d = defaultdict(list)
            for k, v in filters:
                d[k].append(v)
            args["filters"] = dict(d)

        nodes = loader.plugins(**args)
        if nodes:
            for node in nodes:
                tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
