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


class Job(JobInterface):
    """
    A Generic Job Class
    """

    def __init__(self):
        self._options = dict()
        self._options['__custom__'] = []

    def get_options(self):
        """
        Getting the entire options dictionary
        :returns dict
        """

        return self._options

    def add_custom_option(self, option):
        """
        Adding a custom job option
        """
        raise NotImplementedError

    def set_name(self, name):
        """
        Setting a name for the job

        >>> job.set_name('simulation_%d' % number)

        :param name: Name of the job
        :returns self
        """
        self._options['name'] = name
        return self

    def set_account(self, account):
        """
        Setting a account for the job

        >>> job.set_account('ABC_GROUP')

        :param account: Account of the job
        :returns self
        """
        self._options['account'] = account
        return self

    def set_walltime(self, walltime):
        """
        Setting a walltime for the job

        >>> job.set_walltime(datetime.timedelta(hours=2, minutes=30))

        :param walltime: Walltime of the job (an instance of timedelta)
        :returns self
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
        :returns self
        """
        self._options['mem_per_cpu'] = mem_per_cpu
        return self

    def set_memory(self, memory):
        """
        Setting the real memory required per node

        >>> job.set_memory(1024)

        :param memory: The amount of real memory required per node in megabytes
        :returns self
        """
        self._options['memory'] = memory
        return self

    def set_working_directory(self, working_directory):
        """
        Setting the working directory of the batch script to directory before it is executed

        >>> job.set_working_directory('cd /work/foo/bar')

        :param working_directory: The working directory
        :returns self
        """
        self._options['working_directory'] = working_directory
        return self

    def set_error_path(self, error_path):
        """
        Setting the file name that the batch script's standard error is written to

        >>> job.set_error_path('cd /work/foo/bar')

        :param error_path: The path to a file
        :returns self
        """
        self._options['error_path'] = error_path
        return self

    def set_output_path(self, output_path):
        """
        Setting the file name that the batch script's standard output is written to

        >>> job.set_output_path('cd /work/foo/bar')

        :param output_path: The path to a file
        :returns self
        """
        self._options['output_path'] = output_path
        return self
