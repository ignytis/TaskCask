# Task Cask

A tool to run pre-configured processes.

## Status

Early WIP

## Usage

See the example [config](examples/config/config.yaml.jinja2) and [task template definitions file](examples/task_templates/system_commands.yaml.jinja2)

```bash
$ export TASKCASK_CONFIG=$PWD/examples/config/config.yaml.jinja2
$ tcask run example.system_commands.say_hello_world.with_env

2025-02-11 00:15:06,245 PID 26104 [INFO] taskcask.operations.run: Running a command...
Hello, John Doe! It's 2025-02-11T12:15:06. Sample: target_local_env_value. Deployment is: demo

2025-02-11 00:15:06,248 PID 26104 [INFO] taskcask.operations.run: Execution started at 2025-02-11 00:15:06.247525 and finished at 2025-02-11 00:15:06.247525. Time elapsed: 0:00:00.001310
```

## Ideas for development

- Pre- and post-execute hooks for exteral systems
