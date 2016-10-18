from CommandContainerInterface import CommandContainerInterface


class PbsCommands(CommandContainerInterface):
    TYPE_SERIAL = 0
    TYPE_OPEN_MP = 1
    TYPE_MPI = 2
    TYPE_HYBRID = 3

    def __init__(self):
        self.commands = []

    def get_name(self):
        return 'Portable Batch System Commands'

    def serial(self):
        self.type = PbsCommands.TYPE_SERIAL
        return self

    def open_mp(self, processors):
        self.type = PbsCommands.TYPE_OPEN_MP
        self.processors_per_node = processors
        return self

    def mpi(self, nodes):
        self.type = PbsCommands.TYPE_OPEN_MP
        self.nodes = nodes
        return self

    def hybrid(self, nodes, processors_per_node):
        self.type = PbsCommands.TYPE_OPEN_MP
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

    def wall_time(self, hours=24, minutes=0, seconds=0):
        self._wall_time = '%02d:%02d:%02d' % (hours, minutes, seconds)

    def cpu_time(self, hours=24, minutes=0, seconds=0):
        self._cpu_time = '%02d:%02d:%02d' % (hours, minutes, seconds)

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
            lines.append('#PBS -l walltime=%s' % self._wall_time)

        if hasattr(self, '_cpu_time'):
            lines.append('#PBS -l cput=%s' % self._cpu_time)

        if hasattr(self, '_job_array_size'):
            lines.append('#PBS -t %s' % self._job_array_size)

        return '\n'.join(lines)
