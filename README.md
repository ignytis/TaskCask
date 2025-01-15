# Task Cask

A tool to run pre-configured processes.

## Status

Early WIP

## Usage

```bash
$ tcask run example.system_commands.say_hello_world.with_env

2025-01-15 23:45:08,692 PID 55838 [INFO] taskcask.operations.run: Running a command...
Hello, John Doe! It's 2025-01-15T11:45:08
```

## Ideas for development

- Running on different environments like remote SSH, Docker, Kubernetes, etc (`tcask run some_command@some_env`)
- Python executor
- Compilation into executable configs or files for remote systems
- Parameter handling from CLI
- Pre- and post-execute hooks for exteral systems
- Execution parameter configuration (files, overrides via parameters)