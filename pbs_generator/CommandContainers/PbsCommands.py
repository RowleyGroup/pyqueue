from CommandContainerInterface import CommandContainerInterface
import re


class PbsCommands(CommandContainerInterface):
    TYPE_SERIAL = 0
    TYPE_OPEN_MP = 1
    TYPE_MPI = 2
    TYPE_HYBRID = 3

    def __init__(self, name='Portable Batch System Commands'):
        self.command_container_name = name
        self.commands = []

    def get_name(self):
        return self.command_container_name

    def serial(self):
        self.type = PbsCommands.TYPE_SERIAL
        return self

    def open_mp(self, processors):
        self.type = PbsCommands.TYPE_OPEN_MP
        self.processors_per_node = processors
        return self

    def mpi(self, nodes):
        self.type = PbsCommands.TYPE_MPI
        self.nodes = nodes
        return self

    def hybrid(self, nodes, processors_per_node):
        self.type = PbsCommands.TYPE_HYBRID
        self.nodes = nodes
        self.processors_per_node = processors_per_node
        return self

    def queue(self, queue):
        self._queue = queue
        return self

    def accounting_group(self, accounting_group):
        self._accounting_group = accounting_group
        return self

    def name(self, name):
        self._name = ''.join(ch for ch in name if ch.isalnum())[:15]
        return self

    def memory_per_process(self, memory_per_process):
        self._memory_per_process = memory_per_process

    def wall_time(self, time):
        self._wall_time = time
        return self

    def cpu_time(self, time):
        self._cpu_time = time
        return self

    def job_array_size(self, size):
        self._job_array_size = size

    def add_pbs_command(self, string):
        self.commands.append(string)

    def add_attribute(self, key, value):
        self.commands.append('#PBS -l %s=%s' % (key, value))

    def __str__(self):
        lines = []

        # Prepare the part of PBS Commands for processors and nodes
        if hasattr(self, 'type'):
            if self.type == PbsCommands.TYPE_SERIAL:
                lines.append('#PBS -l nodes=1:ppn=1')
                lines.append('#PBS -l procs=1')
            elif self.type == PbsCommands.TYPE_OPEN_MP:
                lines.append('#PBS -l nodes=1:ppn=%d' % self.processors_per_node)
            elif self.type == PbsCommands.TYPE_MPI:
                lines.append('#PBS -l nodes=%d:ppn=1' % self.nodes)
                lines.append('#PBS -l procs=%d' % self.nodes)
            elif self.type == PbsCommands.TYPE_HYBRID:
                lines.append('#PBS -l nodes=%d:ppn=%d' % (self.nodes, self.processors_per_node))

        if hasattr(self, '_name'):
            lines.append('#PBS -N %s' % self._name)

        if hasattr(self, '_accounting_group'):
            lines.append('#PBS -A %s' % self._accounting_group)

        if hasattr(self, '_queue'):
            lines.append('#PBS -q %s' % self._queue)

        if hasattr(self, '_wall_time'):
            lines.append('#PBS -l walltime=%s' % format_time_limit(self._wall_time))

            if not hasattr(self, '_cpu_time'):
                time = None

                if hasattr(self, 'type'):
                    if self.type == PbsCommands.TYPE_SERIAL:
                        time = self._wall_time
                    elif self.type == PbsCommands.TYPE_OPEN_MP:
                        time = self.processors_per_node * timespec_to_seconds(self._wall_time)
                    elif self.type == PbsCommands.TYPE_MPI:
                        time = self.nodes * timespec_to_seconds(self._wall_time)
                    elif self.type == PbsCommands.TYPE_HYBRID:
                        time = self.nodes * self.processors_per_node * timespec_to_seconds(self._wall_time)

                if time is not None:
                    lines.append('#PBS -l cput=%s' % format_time_limit(time))

        if hasattr(self, '_cpu_time'):
            lines.append('#PBS -l cput=%s' % format_time_limit(self._cpu_time))

        if hasattr(self, '_memory_per_process'):
            lines.append('#PBS -l pvmem=%s' % self._memory_per_process)

        if hasattr(self, '_job_array_size'):
            lines.append('#PBS -t %s' % self._job_array_size)

        return '\n'.join(lines)


def timespec_to_seconds(string):
    string = str(string)

    pattern = '^(\d+)([dhm]?)$'
    coefficients = {'d': 86400, 'h': 3600, 'm': 60, '': 3600}

    results = re.search(pattern, string)

    if results is not None:
        digits = int(results.group(1))
        unit = results.group(2)

        return digits * coefficients[unit]
    else:
        raise Exception('The given time "%s" is invalid.' % string)


def format_time_limit(input):
    if isinstance(input, str):
        seconds = timespec_to_seconds(input)
    else:
        seconds = int(input)

    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%02d:%02d:%02d' % (h, m, s)
