import multiprocessing
import time
import sys

from example_3 import func_for_daemon_process, THREE_PIECE_FORMAT_STRING


def return_null():
    return


def return_value():
    return 1


def exit_error():
    sys.exit(1)


def raise_error():
    raise RuntimeError('There was an error!')


def function_to_manually_terminate():
    time.sleep(3)


if __name__ == "__main__":
    print(THREE_PIECE_FORMAT_STRING.format("state", "process id (pid)", "process name"))
    print(THREE_PIECE_FORMAT_STRING.format("-----", "----------------", "------------"))

    p = multiprocessing.Process(target=func_for_daemon_process)

    print(THREE_PIECE_FORMAT_STRING.format("BEFORE:", str(p), p.is_alive()))
    # print("BEFORE:", p, p.is_alive())

    p.start()
    print(THREE_PIECE_FORMAT_STRING.format("DURING:", str(p), p.is_alive()))
    # print("DURING:", p, p.is_alive())

    p.terminate()
    print(THREE_PIECE_FORMAT_STRING.format("TERMINATED:", str(p), p.is_alive()))
    # print("TERMINATED:", p, p.is_alive())

    p.join()
    print(THREE_PIECE_FORMAT_STRING.format("JOINED:", str(p), p.is_alive()))
    # print("JOINED:", p, p.is_alive())


    print()
    print()

    processes = list()
    for f in [return_null, return_value, exit_error, raise_error, function_to_manually_terminate]:
        print('Starting process for', f.__name__)
        p = multiprocessing.Process(target=f, name=f.__name__)
        processes.append(p)

    for p in processes:
        p.start()

    processes[-1].terminate()

    for p in processes:
        p.join()
        print('%s.exitcode = %s' % (p.name, p.exitcode))
