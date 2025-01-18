# Definitions

__Task template definition__ - a dictionary with task attributes. Definitions might contain placeholders
which will be replaced with actual values in runtime

__Task template class__ - a subclass of [BaseTaskTemplate](../src/taskcask/task_templates/task_template.py)
class which represents the _task template definition_ as Python object.

__Task template__ - an instance of _task template class_


__Execution environment__ - an environment where a task runs.
It can be a local machine, remote server (SSH), Docker container, etc