"""Addon Loader module"""

from os import path
import pkgutil
import imp
from ..Utils.deepgetattr import deepgetattr
from ..Utils.logger import Logger


class Loader(object):
    """Addon Loader"""

    def __init__(self, addon_path="{}/Tsaotun/addons/".format(path.expanduser("~"))):
        self.__locate(addon_path)

    def __locate(self, addon_path):
        """Locate addon path"""
        if path.exists(addon_path):
            self.addon_path = addon_path
        else:
            Logger.logError("addon path not found: {}.".format(addon_path))
            raise RuntimeError

    def load(self, tsaotun):
        """Load addons"""
        module_names = [n for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
        addons = {}
        for module_name in module_names:
            try:
                f, filename, description = imp.find_module(
                    module_name, [self.addon_path])
                mod = imp.load_module(
                    module_name, f, filename, description)
                for k, v in mod.__override__.iteritems():
                    addons["{}|{}".format(k, v)] = deepgetattr(
                        mod, "{}.{}".format(k, v))
            except ImportError as e:
                Logger.logError(e)
                raise RuntimeError

        tsaotun.push(**addons)

    def addons(self, filters=None):
        """List addons"""
        enabled = 'true'
        if filters:
            return [{'Addon':n, 'Enabled': enabled} for _, n, _ in pkgutil.iter_modules(
                ["{}".format(self.addon_path)]) if filters["active"][0] == enabled]
        else:
            return [{'Addon':n, 'Enabled': enabled} for _, n, _ in pkgutil.iter_modules(
                ["{}".format(self.addon_path)])]
