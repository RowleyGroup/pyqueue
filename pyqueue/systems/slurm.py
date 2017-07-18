"""
SLURM module
"""

from datetime import datetime
from ..job import JobInterface
from ..utils import strfdelta, get_user_information
from ..enums import DependencyTypes
from .. import __version__


class SlurmPrinter(object):
    """
    This class is meant to generate the job submission script from a Job object
    """

    def __init__(self):
        pass

    @staticmethod
    def get_dependency_type(_type):
        """
        Get the dependency type string for SlurmPrinter

        :rtype: str
        """
        if _type == DependencyTypes.AFTER:
            return 'after'
        elif _type == DependencyTypes.AFTER_ANY:
            return 'afterany'
        elif _type == DependencyTypes.AFTER_CORR:
            return 'aftercorr'
        elif _type == DependencyTypes.AFTER_NOT_OK:
            return 'afternotok'
        elif _type == DependencyTypes.AFTER_OK:
            return 'afterok'
        else:
            return None

    @staticmethod
    def get_header():
        """
        Makes the header section for the scripts

        :rtype: str
        """
        username, userid, uname = get_user_information()

        header = '''\
# This Slurm batch script was generated
# By user: %s (%s)
# On host: %s
# At date: %s
# Using: Pyqueue v%s

''' % (username, userid, uname, datetime.now().strftime('%a. %B  %w %X %Y'), __version__)

        return header

    def generate(self, job):
        """
        Generates a job submission script from a job object

        :param job: An instance of JobInterface
        :type job: pyqueue.job.JobInterface
        """

        options = job.get_options().copy()
        job_name = options.pop('name', None)
        job_account = options.pop('account', None)
        job_walltime = options.pop('walltime', None)
        job_mem_per_cpu = options.pop('mem_per_cpu', None)
        job_memory = options.pop('memory', None)
        job_working_directory = options.pop('working_directory', None)
        job_error_path = options.pop('error_path', None)
        job_output_path = options.pop('output_path', None)
        job_dependency = options.pop('depending', None)
        job_shell = options.pop('shell', '/bin/bash')
        job_custom_options = options.pop('__custom__', [])

        directives_lines = []

        if job_name is not None:
            directives_lines.append('--job-name=%s' % job_name)

        if job_account is not None:
            directives_lines.append('--account=%s' % job_account)

        if job_working_directory is not None:
            directives_lines.append('--workdir=%s' % job_working_directory)

        if job_error_path is not None:
            directives_lines.append('--error=%s' % job_error_path)

        if job_output_path is not None:
            directives_lines.append('--output=%s' % job_output_path)

        if job_walltime is not None:
            directives_lines.append('--time=%s' %
                                    strfdelta(job_walltime, '%H:%M:%S'))

        if job_mem_per_cpu is not None:
            directives_lines.append('--mem-per-cpu=%d' % job_mem_per_cpu)

        if job_memory is not None:
            directives_lines.append('--mem=%d' % job_memory)

        if job_dependency is not None:
            master = job_dependency['job']
            dependency_type = SlurmPrinter.get_dependency_type(
                job_dependency['dependency_type']
            )
            job_id = master.get_id() if isinstance(master, JobInterface) else master

            directives_lines.append(
                '--dependency=%s:%s' %
                (dependency_type, job_id)
            )

        for custom_option in job_custom_options:
            directives_lines.append(custom_option)

        directives = '\n'.join([
            '#SBATCH %s' % directive for directive in directives_lines
        ])

        commands = '\n'.join([
            '\n'.join(command_container.get_commands()) for command_container in job.get_commands()
        ])

        script = '#!%s\n' % job_shell
        script += SlurmPrinter.get_header()
        script += directives
        script += '\n\n'
        script += commands

        return script


class SlurmLocalSubmitter(object):
    """
    This class is for submitting Slurm jobs locally
    The host machine should have slurm installed and running
    """

    def __init__(self, printer=None):
        self._printer = printer if printer is not None else SlurmPrinter()

    def submit(self, job):
        """
        Submits a given job

        :param job: The job to submit
        :type job: pyqueue.job.JobInterface
        """
        from subprocess import Popen, PIPE
        script = self._printer.generate(job)
        process = Popen('sbatch', stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout, sterr = process.communicate(input=script)
        process.stdin.close()


class SlurmRemoteSubmitter(object):
    """
    This class is for submitting Slurm jobs remotely via SSH
    """

    def __init__(self, ssh, printer=None):
        self._printer = printer if printer is not None else SlurmPrinter()
        self._ssh = ssh

    def submit(self, job):
        """
        Submits a given job

        :param job: The job to submit
        :type job: pyqueue.job.JobInterface
        """
        script = self._printer.generate(job)
        stdin, stdout, stderr = self._ssh.exec_command('sbatch')
        stdin.write(script)
        stdin.flush()
        stdin.channel.shutdown_write()
        return stdout.read()
