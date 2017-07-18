"""
Enums.
"""


try:
    from enum import Enum
except ImportError:
    Enum = object


class MailTypes(Enum):
    """
    MailTypes enum
    """
    ALL = 0
    BEGIN = 1
    END = 2
    FAIL = 3
    REQUEUE = 4


class DependencyTypes(Enum):
    """
    DependencyTypes enum
    """

    # This job can begin execution after the specified jobs have begun
    # execution.
    # SUPPORT: Slurm
    AFTER = 0

    # This job can begin execution after the specified jobs have terminated.
    # SUPPORT: Slurm, PBS
    AFTER_ANY = 1

    # A task of this job array can begin execution after the corresponding
    # task ID in the specified job has completed successfully
    # (ran to completion with an exit code of zero).
    # SUPPORT: Slurm
    AFTER_CORR = 2

    # This job can begin execution after the specified jobs have successfully executed
    # (ran to completion with an exit code of zero).
    # SUPPORT: Slurm, PBS
    AFTER_OK = 3

    # This job can begin execution after the specified jobs have terminated in some failed state
    # (non-zero exit code, node failure, timed out, etc).
    # SUPPORT: Slurm, PBS
    AFTER_NOT_OK = 4

    # This job can begin execution after any previously launched jobs
    # sharing the same job name and user have terminated.
    # SUPPORT: Slurm
    SINGLETON = 4
