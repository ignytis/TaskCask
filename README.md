# Task Cask

A tool to run pre-configured processes.

## Status

Early WIP

## Usage

See the example [config](examples/config/config.tcask) and [task template definitions file](examples/task_templates/system_commands.tcask)

```bash
$ export TASKCASK_CONFIG=$PWD/examples/config/config.tcask
$ tcask run example.system_commands.say_hello_world.with_env

2025-02-11 00:15:06,245 PID 26104 [INFO] taskcask.operations.run: Running a command...
Hello, John Doe! It's 2025-02-11T12:15:06. Sample: target_local_env_value. Deployment is: demo

2025-02-11 00:15:06,248 PID 26104 [INFO] taskcask.operations.run: Execution started at 2025-02-11 00:15:06.247525 and finished at 2025-02-11 00:15:06.247525. Time elapsed: 0:00:00.001310
```

## Ideas for development

- Extendable command list (plugins can add commands via autoload)
- Export into external task execution systems (Set of Bash scripts? [Luigi](https://luigi.readthedocs.io/)? [Dagster](https://dagster.io/)? [Apache Airflow](https://airflow.apache.org/)?)
- Loading the task templates from plugins

## Known issues / TODO

- Executors: map the process-specific exception into some general TaskException
- SSH environment: pass parameters (password / custom path to key etc) into module
