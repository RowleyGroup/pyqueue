from CommandContainerInterface import CommandContainerInterface


class ShellCommands(CommandContainerInterface):
    def __init__(self, name='Shell Commands'):
        self.commands = []
        self._name = name

    def __getattr__(self, name):
        def function(*args):
            self.commands.append('%s %s' % (name, ' '.join(args)))
            return self

        return function

    def append(self, command):
        self.commands.append(command)
        return self

    def get_name(self):
        return self._name

    def __str__(self):
        return '\n'.join(self.commands)
