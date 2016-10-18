import click
import re
import paramiko
import os
import glob
from tabulate import tabulate
from pbs_generator import SshPbs, ShellCommands, PbsCommands

ip_address_regex = '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'
host_name_regex = '[a-zA-Z0-9](?:(?:[a-zA-Z0-9-]*|(?<!-)\.(?![-.]))*[a-zA-Z0-9]+)?'
username_regex = '[a-z_][a-z0-9_-]*[$]?'
port_regex = '[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]'
ssh_url_regex = '(%s)\@(%s|%s)(\:(%s))?' % (username_regex, ip_address_regex, host_name_regex, port_regex)


def parse_ssh_url(url):
    search = re.search(ssh_url_regex, url)
    assert search is not None, 'Entered ssh url is invalid: %s' % url
    username = search.group(1)
    hostname = search.group(2)
    port = int(search.group(7)) if search.group(7) is not None else 22

    return [username, hostname, port]


def get_connection(url, prompt_password=False):
    ssh_known_hosts = os.path.expanduser('~/.ssh/known_hosts')
    ssh_public_key = os.path.expanduser('~/.ssh/id_rsa.pub')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.get_host_keys().load(ssh_known_hosts)
    username, hostname, port = parse_ssh_url(url)

    args = {
        'username': str(username),
        'port': port,
    }

    if prompt_password:
        args['password'] = click.prompt('Enter password for %s@%s' % (username, hostname), hide_input=True)
    else:
        args['key_filename'] = ssh_public_key

    ssh.connect(hostname, **args)
    return ssh


@click.command()
@click.option('-p', is_flag=True, default=False, help='Either prompt you for password or use id_rsa')
@click.option('-d', type=click.Path(), default='~', help='The working directory on remote machine')
@click.option('--files', type=click.Path(),
              help='The files that you want to work with as input files. Use local paths on your machine. '
                   'The files will be automatically copied to the server\n'
                   'You can use wildcard path like:\n --files="inputs/*.inp"\n'
                   'It will automatically loop over all the files and run the command for each file. '
                   'The environment variables `$INPUT_FILE` and `$INPUT_NAME` will be made '
                   'that you can use inside your command'
              )
@click.option('--serial', is_flag=True, help='Requests 1 processor on 1 node.')
@click.option('--openmp', type=click.INT, nargs=1,
              help='This should be used for jobs that use shared memory parallelization '
                   '(e.g., OpenMP) or when communication across an interconnect severely '
                   'impacts job performance.')
@click.option('--mpi', type=click.INT, nargs=1, help='This mode of parallelization is suitable for '
                                                     'Message Passing Interface (MPI) jobs.')
@click.option('--hybrid', type=click.INT, nargs=2, help='Requests for N nodes with M processors.')
@click.option('--attribute', '-a', help='Request node attribute eg. submit -a switch2:xeon')
@click.option('--mpp', help='Memory per process')
@click.option('--queue', '-q', help='Specify a queue to run on')
@click.option('--time', '-t', type=click.STRING, help='Wall time', default='24')
@click.option('--debug', '-D', is_flag=True, help='Don\'t submit job, print debugging info')
@click.option('--job-name', '-j', help='Job name')
@click.argument('ssh_url', type=click.STRING)
@click.argument('command', type=click.STRING, required=True)
def ssh(p, d, files, serial, openmp, mpi, hybrid, mpp, attribute, queue, time, debug, job_name, ssh_url, command):
    ssh = get_connection(ssh_url, p)
    sftp = ssh.open_sftp()

    commands = ShellCommands().cd(d).append(command)
    pbs_command = get_pbs_command(serial, openmp, mpi, hybrid, mpp, attribute, queue, time)

    if files is not None:
        files_array = glob.glob(files)
        jobs = []

        with click.progressbar(files_array, label='Uploading the files' if not debug else 'Printing PBS') as bar:
            for file in bar:
                file_name = os.path.basename(file)
                name, extension = os.path.splitext(file_name)
                remote_file_path = os.path.join(d, file_name)

                export_commands = ShellCommands() \
                    .append('export INPUT_FILE="%s"' % remote_file_path) \
                    .append('export INPUT_NAME="%s"' % name)

                job = SshPbs(pbs_command, export_commands, commands, ssh=ssh).name(name)

                if debug:
                    click.echo('\n\nJob "%s":' % name)
                    click.echo('=' * 58)
                    click.echo(job.get_string())
                    click.echo('=' * 58)
                else:
                    sftp.put(file, remote_file_path)
                    job.submit()
                    job.input_file = file_name
                    jobs.append(job)

        if not debug:
            click.echo('\n')
            table = map(lambda job: [job.input_file, job.get_name(), job.id], jobs)
            click.echo(tabulate(table, headers=['Input file', 'Job name', 'Job ID'], tablefmt="rst"))

    ssh.close()


def get_pbs_command(serial, openmp, mpi, hybrid, mpp, attribute, queue, time):
    pbs_commands = PbsCommands('Common PBS commands from CLI options')

    if openmp:
        pbs_commands.open_mp(openmp)
    elif mpi:
        pbs_commands.mpi(mpi)
    elif hybrid:
        pbs_commands.hybrid(*hybrid)
    elif serial:
        pbs_commands.serial()

    if mpp is not None:
        pbs_commands.memory_per_process(mpp)

    if attribute is not None:
        pbs_commands.add_pbs_command('#PBS -l %s' % attribute)

    if queue is not None:
        pbs_commands.queue(queue).accounting_group(queue)

    if time is not None:
        pbs_commands.wall_time(time)

    return pbs_commands


if __name__ == '__main__':
    ssh()
