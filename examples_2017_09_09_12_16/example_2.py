"""
Passing arguments to identify or name the process is cumbersome, and unnecessary.

Each multiprocessing.Process instance has a name with a default value that can be changed as the process is created.
Naming processes is useful for keeping track of them,
especially in applications with multiple types of processes running simultaneously.
"""

import multiprocessing
import time
import sys


FORMAT_STRING = "{0:<30} {1:<30}"


def work_quickly():
    curr_process = multiprocessing.current_process()

    # print("Starting : %r" % curr_process.name)
    print(FORMAT_STRING.format("Starting", curr_process.name))
    sys.stdout.flush()

    time.sleep(2)

    # print("Exiting  : %r" % curr_process.name)
    print(FORMAT_STRING.format("Exiting", curr_process.name))
    sys.stdout.flush()


def work_slowly():
    curr_process = multiprocessing.current_process()

    # print("Starting : %r" % curr_process.name)
    print(FORMAT_STRING.format("Starting", curr_process.name))
    sys.stdout.flush()

    time.sleep(4)

    # print("Exiting  : %r" % curr_process.name)
    print(FORMAT_STRING.format("Exiting", curr_process.name))
    sys.stdout.flush()

if __name__ == "__main__":
    print(FORMAT_STRING.format("state", "process name"))
    print(FORMAT_STRING.format("-----", "------------"))

    worker_quick_1 = multiprocessing.Process(name="work_quickly 1", target=work_quickly)
    worker_quick_2 = multiprocessing.Process(name="work_quickly 2", target=work_quickly)
    worker_slow = multiprocessing.Process(target=work_slowly)  # use default name

    worker_slow.start()
    worker_quick_1.start()
    worker_quick_2.start()
