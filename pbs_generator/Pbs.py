from CommandContainers.PbsCommand import PbsCommands


class Pbs:
    def __init__(self, *commands):
        self.pbs_commands = PbsCommands()
        self.commands = commands

    def get_string(self):
        parts = []

        for command in (self.pbs_commands,) + self.commands:
            string = command.get_header() + '\n' + command.__str__()
            parts.append(string)

        return '\n\n'.join(parts)

    def __getattr__(self, name):
        def function(*args):
            if name in dir(self.pbs_commands):
                method = getattr(self.pbs_commands, name)
                if callable(method):
                    method(*args)
                    return self

        return function

    def __str__(self):
        return self.get_string()
