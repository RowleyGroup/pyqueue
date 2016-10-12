import re
from subprocess import Popen, PIPE, STDOUT
from CommandContainers.PbsCommand import PbsCommands


class Pbs:
    DEPENDENCY_AFTER_OK = 'afterok'
    DEPENDENCY_AFTER_ANY = 'afterany'

    def __init__(self, *commands):
        self.pbs_commands = PbsCommands()
        self.commands = commands
        self.submitted = False
        self.dependency = None

    def get_string(self):
        parts = []

        for command in (self.pbs_commands,) + self.commands:
            string = command.get_header() + '\n' + command.__str__()
            parts.append(string)

        return '\n\n'.join(parts)

    def depends(self, job, type=DEPENDENCY_AFTER_OK):
        if not isinstance(job, Pbs):
            raise Exception('Given argument should be an instance of Pbs')

        self.dependency = job
        self.dependency_type = type
        return self

    def submit(self, program='qsub'):
        input = self.get_string()

        if isinstance(self.dependency, Pbs):
            if self.dependency.submitted:
                command = [program, '-W', 'depend=%s:%s' % (self.dependency_type, self.dependency.id)]
            else:
                raise Exception(
                    'The job that you are trying to submit, is dependent on another job that is not submitted yet.'
                )
        else:
            command = program

        p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout = p.communicate(input=input)[0]
        p.stdin.close()

        self.id = re.search('(\d+)', stdout).group(1)
        self.submitted = True
        return self

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
