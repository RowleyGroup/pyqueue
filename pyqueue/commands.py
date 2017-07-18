"""
Commands
"""


class Commands(object):
    """
    A container for the shell commands
    """

    def __init__(self):
        """
        Initiating a new Commands object
        """
        self._commands = []

    def append(self, command):
        """
        Appending a new command to the command container
        >>> commands.append('cd /foo/bar').append('program arg1 arg2 --option1')

        :param command: The command to be appended
        :returns Commands
        """
        self._commands.append(command)
        return self

    def get_commands(self):
        """
        Returns a list of all commands in this command container

        :rtype: list
        """
        return self._commands

    def __getattr__(self, name):
        """
        Magically enabling using a program name as a method

        >>> commands.cd('/foo/bar').program('arg1 arg2 --options')

        :rtype: function
        """
        def function(*args):
            """
            Takes arguments and appends a command with a
            program name `name` from the upper scope

            :rtype: Commands
            """
            self.append('%s %s' % (name, ' '.join(args)))
            return self

        return function
