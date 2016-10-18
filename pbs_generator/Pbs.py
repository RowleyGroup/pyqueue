import re
import paramiko
from subprocess import Popen, PIPE, STDOUT
from CommandContainers.PbsCommands import PbsCommands


class Pbs:
    DEPENDENCY_AFTER_OK = 'afterok'
    DEPENDENCY_AFTER_ANY = 'afterany'

    def __init__(self, *commands):
        self.pbs_commands = PbsCommands()
        self.commands = commands
        self.submitted = False
        self.dependency = None
        self.id = None

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

    def run_command(self, command, pipe_in):
        p = Popen(command, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        stdout = p.communicate(input=pipe_in)[0]
        p.stdin.close()

        return stdout

    def submit(self, program='qsub'):
        input = self.get_string()

        if isinstance(self.dependency, Pbs):
            if not self.dependency.submitted:
                self.dependency.submit()

            command = [program, '-W', 'depend=%s:%s' % (self.dependency_type, self.dependency.id)]
        else:
            command = program

        stdout = self.run_command(command, input)

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

    def get_name(self):
        return self.pbs_commands._name

    def __str__(self):
        return self.get_string()


class SshPbs(Pbs):
    def __init__(self, *commands, **kwargs):
        assert 'ssh' in kwargs
        assert isinstance(kwargs.get('ssh'), paramiko.SSHClient)
        Pbs.__init__(self, *commands)
        self.ssh = kwargs.get('ssh')

    def run_command(self, command, pipe_in):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        stdin.write(input)
        stdin.flush()
        stdin.channel.shutdown_write()
        return stdout.read()
