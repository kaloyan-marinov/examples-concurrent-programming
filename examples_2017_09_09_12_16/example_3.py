"""
By default, the main program will not exit until all of the children have exited.
However, there are times when it is useful to be able to
start a background process which runs without blocking the main program from exiting - e.g.:
    a) in services where there may not be an easy way to interrupt the worker
    b) in services where letting it die in the middle of its work does not lose or corrupt data
       (for example, a task that generates “heart beats” for a service monitoring tool)

To mark a process as a daemon, set its daemon attribute with a boolean value.
The default is for processes to not be daemons, so passing True turns the daemon mode on.
"""

import multiprocessing
import time
import sys


THREE_PIECE_FORMAT_STRING = "{0:<30} {1:<50} {2:<30}"


def func_for_daemon_process():
    curr_process = multiprocessing.current_process()

    # print("Starting : %r, %r" % (curr_process.pid, curr_process.name))
    print(
        THREE_PIECE_FORMAT_STRING.format(
            "Starting", curr_process.pid, curr_process.name
        )
    )
    sys.stdout.flush()

    time.sleep(2)

    # print("Exiting  : %r, %r" % (curr_process.pid, curr_process.name))
    print(
        THREE_PIECE_FORMAT_STRING.format("Exiting", curr_process.pid, curr_process.name)
    )
    sys.stdout.flush()


def func_for_non_daemon_process():
    curr_process = multiprocessing.current_process()

    # print("Starting : %r, %r" % (curr_process.pid, curr_process.name))
    print(
        THREE_PIECE_FORMAT_STRING.format(
            "Starting", curr_process.pid, curr_process.name
        )
    )
    sys.stdout.flush()

    # print("Exiting  : %r, %r" % (curr_process.pid, curr_process.name))
    print(
        THREE_PIECE_FORMAT_STRING.format("Exiting", curr_process.pid, curr_process.name)
    )
    sys.stdout.flush()


def do_not_wait_for_daemon(func_for_daemon_proc, func_for_non_daemon_proc):
    """
    Before the main program exits, the func_for_daemon_process process is terminated automatically
    in order to avoid leaving orphaned processes running.
    (You can verify this by looking for the process id value printed when you run the program,
    and then checking for that process with a command like ps.)
    """
    print(THREE_PIECE_FORMAT_STRING.format("state", "process id (pid)", "process name"))
    print(THREE_PIECE_FORMAT_STRING.format("-----", "----------------", "------------"))

    d = multiprocessing.Process(
        name="func_for_daemon_proc", target=func_for_daemon_proc
    )
    d.daemon = True

    n = multiprocessing.Process(
        name="func_for_non_daemon_proc", target=func_for_non_daemon_proc
    )
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()

    """
    The output does not include the “Exiting” message from the func_for_daemon_process process,
    since all of the non-func_for_daemon_process processes (including the main program) exit
    before the func_for_daemon_process process wakes up from its 2-second sleep.
    """


def do_wait_for_daemon_processes(func_for_daemon_proc, func_for_non_daemon_proc):
    """
    To wait until a process has completed its work and exited, use the join() method.
    """
    print(THREE_PIECE_FORMAT_STRING.format("state", "process id (pid)", "process name"))
    print(THREE_PIECE_FORMAT_STRING.format("-----", "----------------", "------------"))

    d = multiprocessing.Process(
        name="func_for_daemon_proc", target=func_for_daemon_proc
    )
    d.daemon = True

    n = multiprocessing.Process(
        name="func_for_non_daemon_proc", target=func_for_non_daemon_proc
    )
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()

    # make the main process wait for the func_for_daemon_process to exit
    # (which will force the func_for_daemon_process process to print an “Exiting” message)
    print("d.is_alive()", d.is_alive())
    d.join()
    print("d.is_alive()", d.is_alive())
    n.join()


if __name__ == "__main__":
    should_wait_for_daemon = False

    if should_wait_for_daemon is False:
        print("will NOT wait for func_for_daemon_process process")
        print()

        do_not_wait_for_daemon(func_for_daemon_process, func_for_non_daemon_process)
    else:
        print("will wait for func_for_daemon_process process")
        print()

        do_wait_for_daemon_processes(
            func_for_daemon_process, func_for_non_daemon_process
        )
