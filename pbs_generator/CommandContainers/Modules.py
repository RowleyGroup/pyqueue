from CommandContainerInterface import CommandContainerInterface


class Modules(CommandContainerInterface):
    def __init__(self):
        self._purge = False
        self.loaded_modules = []
        self.unloaded_modules = []

    def purge(self):
        self._purge = True
        return self

    def get_name(self):
        return 'Modules'

    def load(self, module):
        if isinstance(module, list):
            self.loaded_modules = self.loaded_modules + module
        else:
            self.loaded_modules.append(module)

        return self

    def unload(self, module):
        if isinstance(module, list):
            self.unloaded_modules = self.unloaded_modules + module
        else:
            self.unloaded_modules.append(module)

        return self

    def __str__(self):
        lines = []

        if self._purge:
            lines.append('module purge')

        lines = lines + map(lambda module: 'module unload %s' % module, self.unloaded_modules)
        lines = lines + map(lambda module: 'module load %s' % module, self.loaded_modules)

        return '\n'.join(lines)
