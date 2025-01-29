import os
import platform


def my_fn(*args, **kwargs):
    print("Hello! This is an example function to be loaded by Python Executor.")
    print(f"Some system info: {os.name}, {platform.system()}, {platform.release()}")
    print("Args: ", args)
    print("kwargs: ", kwargs)
