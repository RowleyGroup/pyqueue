# PBS-Generator
A python library for generating PBS scripts and submitting them to queue.

# Installation
You can use pip to install the package:

```
pip install pbs-generator
```

# Usage
PBS-Gnerator is created to make it easier to write PBS scripts, submitting them to queue and handling job dependencies.

To create a new PBS script with some shell commands, you should make an instances of `Pbs` and `ShellCommands`.

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

## Chainability
All the command container methods are chainable, meaning that you can call them chained together in a single statement.

```python
commands.cd('/work/foo/bar').command('orca input_file.inp').command('program arg1 arg2')
```

## Specify nodes and processors
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

# Custom PBS commands
```python
pbs.add_pbs_command('-l nodes=5:ppn=12+nodes=1:ppn=1')
```

## Environment modules
You can create an instance of `Modules` for managing the environment modules. Note that you should pass the command containers in the right order.

```python
modules = Modules()
modules.purge()
modules.load('gaussian')
modules.load('orca')

commands = ShellCommands()

pbs = Pbs(modules, commands)
```
## API
### `Pbs.name(name)`
Sets a user specified name for the job so you can track it easier `qstat`.

### `Pbs.wall_time(hours, [minutes], [seconds])`
### `Pbs.cpu_time(hours, [minutes], [seconds])`

### `Pbs.serial()`
Requests for 1 processors on 1 node.

### `Pbs.open_mp(M)`
Requests for M processors on the same node.

### `Pbs.mpi(N)`
Requests for N processors which may be running on any nodes.

### `Pbs.hybrid(N, M)`
Requests for N nodes with M processors.

### `Modules.purge()`
Requests for purging all the loaded modules.

### `Modules.load(name)`
Loads an environment modules.

### `Modules.unload(name)`
Unloads an environment modules.
