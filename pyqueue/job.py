"""
Job
"""

from datetime import timedelta


class JobInterface(object):
    """
    JobInterface
    """

    def add_custom_option(self, option):
        """
        Adding a custom job option
        """
        raise NotImplementedError

    def add_commands(self, commands):
        """
        Adding a commands object
        """
        raise NotImplementedError

    def get_commands(self):
        """
        Getting all the commands containers for this job
        """
        raise NotImplementedError

    def set_name(self, name):
        """
        Setting a name for a job
        """
        raise NotImplementedError

    def set_walltime(self, walltime):
        """
        Setting a walltime for a job
        """
        raise NotImplementedError

    def set_account(self, account):
        """
        Setting an account name for a job
        """
        raise NotImplementedError

    def get_options(self):
        """
        Getting all the options for this job
        """
        raise NotImplementedError

    def set_id(self, _id):
        """
        Setting the id for this job
        """
        raise NotImplementedError

    def get_id(self):
        """
        Getting the id for this Job
        """
        raise NotImplementedError


class Job(JobInterface):
    """
    A Generic Job Class
    """

    def __init__(self):
        self._options = dict()
        self._options['__custom__'] = []
        self._options['shell'] = '/bin/bash'
        self._command_containers = []
        self._id = None

    def get_options(self):
        """
        Getting the entire options dictionary
        :rtype: dict
        """
        return self._options

    def get_commands(self):
        """
        Getting all the command containers
        :rtype: list
        """
        return self._command_containers

    def add_commands(self, commands):
        """
        Adding a commands object

        >>> cmds = Commands().cd('/foo/bar').program('arg1 arg2')
        >>> job.add_commands(cmds)

        :param commands: The command container object
        :type commands: pyqueue.commands.Commands
        :returns: self
        :rtype: self
        """
        self._command_containers.append(commands)
        return self

    def add_custom_option(self, option):
        """
        Adding a custom job option

        :rtype: self
        """
        self._options['__custom__'].append(option)
        return self

    def set_name(self, name):
        """
        Setting a name for the job

        >>> job.set_name('simulation_%d' % number)

        :param name: Name of the job
        :returns: self
        :rtype: self
        """
        self._options['name'] = name
        return self

    def set_shell(self, shell):
        """
        Setting a executable shell for the job

        :param shell: Path to the executable
        :returns: self
        :rtype: self
        """
        self._options['shell'] = shell
        return self

    def set_account(self, account):
        """
        Setting a account for the job

        >>> job.set_account('ABC_GROUP')

        :param account: Account of the job
        :returns: self
        :rtype: self
        """
        self._options['account'] = account
        return self

    def set_walltime(self, walltime):
        """
        Setting a walltime for the job

        >>> job.set_walltime(datetime.timedelta(hours=2, minutes=30))

        :param walltime: Walltime of the job (an instance of timedelta)
        :returns: self
        :rtype: self
        """
        if not isinstance(walltime, timedelta):
            raise TypeError(
                'walltime must be an instance of datetime.timedelta. %s given' %
                type(walltime)
            )

        self._options['walltime'] = walltime
        return self

    def set_memory_per_cpu(self, mem_per_cpu):
        """
        Setting the memory needed per cputimedelta

        >>> job.set_memory_per_cpu(1024)

        :param mem_per_cpu: The amount of memory required for each allocated cpu block in megabytes
        :returns: self
        :rtype: self
        """
        self._options['mem_per_cpu'] = mem_per_cpu
        return self

    def set_memory(self, memory):
        """
        Setting the real memory required per node

        >>> job.set_memory(1024)

        :param memory: The amount of real memory required per node in megabytes
        :returns: self
        :rtype: self
        """
        self._options['memory'] = memory
        return self

    def set_working_directory(self, working_directory):
        """
        Setting the working directory of the batch script to directory before it is executed

        >>> job.set_working_directory('cd /work/foo/bar')

        :param working_directory: The working directory
        :returns: self
        :rtype: self
        """
        self._options['working_directory'] = working_directory
        return self

    def set_error_path(self, error_path):
        """
        Setting the file name that the batch script's standard error is written to

        >>> job.set_error_path('cd /work/foo/bar')

        :param error_path: The path to a file
        :returns: self
        :rtype: self
        """
        self._options['error_path'] = error_path
        return self

    def set_output_path(self, output_path):
        """
        Setting the file name that the batch script's standard output is written to

        >>> job.set_output_path('cd /work/foo/bar')

        :param output_path: The path to a file
        :returns: self
        :rtype: self
        """
        self._options['output_path'] = output_path
        return self

    def depends_on(self, job, dependency_type):
        """
        Specifying a job dependency

        >>> job.depends_on(job1, enums.DependencyTypes.AFTER_OK)

        :param job: The master job that this job is depended upon. Either a job object or the id str
        :param dependency_type: Type of dependency_type from enums.DependencyTypes
        :returns: self
        :rtype: self
        """
        self._options['depending'] = {
            'job': job,
            'dependency_type': dependency_type
        }
        return self

    def set_id(self, _id):
        """
        Set the id for this Job

        :rtype: str
        """
        self._id = _id

    def get_id(self):
        """
        Get the id for this Job

        :rtype: str
        """
        return self._id
