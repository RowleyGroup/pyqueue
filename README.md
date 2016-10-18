# PBS-Generator
A python library for submitting calculations to a [Portable Batch System](https://en.wikipedia.org/wiki/Portable_Batch_System) (PBS) queuing system.

This library supports configuration of job attributes such as walltime, node requirements, and dependencies. It can automatically submit calculations on remote systems.

# Installation
You can use pip to install the package:

```
pip install pbs-generator
```

If you get errors while installation of cryptography, follow [these instructions](http://stackoverflow.com/a/37781781/1543737).

# Usage

## CLI

Once you have the package installed, you will have access to a command-line program called `nicesub`. This program takes two arguments, `ssh_url` and `command`. You should run this command on your local machine and this script will upload the files and submit the jobs with the corresponding command for each file through an SSH connection. If your public key is authorized you won't need need to enter your password, otherwise you can use -p option that will prompt for password input.

For instance, we want to run gaussian for a bunch of `.gjf` input files. All we need to do is to specify the input files with `--files` option and wildcards and then use `$INPUT_FILE` in the command. Note that, the command containing `$INPUT_FILE` should be placed inside single quotations to prevent local variable expansion.

```
nicesub user@host 'g09 < $INPUT_FILE > "$INPUT_NAME.out"' --files '*.gjf' -d /global/scratch/user/foo/bar
```

## API

To create a new PBS script with some shell commands, you should make an instance of `Pbs` and `ShellCommands`.

```python
from pbs_generator import Pbs, ShellCommands

commands = ShellCommands()
commands.cd('/work/foo/bar')

pbs = Pbs(commands)
```

We can either print out the pbs or submit it to qsub:

```python
# Print the script
print pbs

# Submit the job
pbs.submit()
```

### Chainability
All the command container methods are chainable, meaning that you can call them chained together in a single statement.

```python
commands.cd('/work/foo/bar').append('orca input_file.inp').append('program arg1 arg2')
```

### Specify nodes and processors
```python
# Runs the job in serial
pbs.serial()

# Runs the job with `n` processors on 1 node (OpenMP)
pbs.open_mp(n)

# Runs the job with `m` processors on any nodes
pbs.mpi(m)

# Runs the job on `n` nodes with `m` processors per each node
pbs.hybrid(n, m)
```

### Custom PBS commands
```python
pbs.add_pbs_command('-l nodes=5:ppn=12+nodes=1:ppn=1')
```

### Job dependency
Job dependency is done simply by calling `depends` method on `Pbs` object:

```python
job_1.submit()

job_2.depends(job_1).submit()

# Or if you want an afterany dependency
job_2.depends(job_1, Pbs.DEPENDENCY_AFTER_ANY).submit()
```

### Environment modules
You can create an instance of `Modules` for managing the environment modules. Note that you should pass the command containers in the right order.

```python
modules = Modules()
modules.purge()
modules.load('gaussian')
modules.load('orca')

commands = ShellCommands()

pbs = Pbs(modules, commands)
```

### API
#### `Pbs.name(name)`
Sets a user specified name for the job so you can track it easier.

#### `Pbs.wall_time(time)`
Sets the wall time limit with the following format:

* `1d`: 1 day
* `12h`: 12 hours
* `15m`: 15 minutes

#### `Pbs.cpu_time(time)`
Sets the cpu time limit. The input time formatting is the same as wall time. If you use one of the `serial`, `open_mp`, `mpi` or `hybrid` preset functions, this parameter will be set automatically according to allocated resources and the wall time.

#### `Pbs.serial()`
Requests 1 processor on 1 node.

#### `Pbs.open_mp(M)`
Requests M processors on the same node. This should be used for jobs that use shared memory parallelization (e.g., OpenMP) or when communication across an interconnect severely impacts job performance.

#### `Pbs.mpi(N)`
Requests for N processors which may be running on any nodes. This mode of parallelization is suitable for Message Passing Interface (MPI) jobs.

#### `Pbs.hybrid(N, M)`
Requests for N nodes with M processors.

#### `Pbs.depends(pbs, [dependency_type])`
Make a dependency to another job

#### `ShellCommands.append()`
Append a command to the command container.:

```
commands.append('program arg1 arg2')
```

#### `Modules.purge()`
Requests for purging all the loaded modules.

#### `Modules.load(name)`
Loads an environment modules.

#### `Modules.unload(name)`
Unloads an environment modules.
