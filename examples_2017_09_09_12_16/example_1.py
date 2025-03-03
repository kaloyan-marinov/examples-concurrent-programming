"""
It is usually useful to be able
to spawn a process with arguments to tell it what work to do.

Unlike with threading, it is only possible to pass arguments to a multiprocessing. Process instance
if all of these arguments are serializable using pickle.

This example passes each worker a number so the output is a little more interesting.
"""

import multiprocessing


def worker_function(num):
    print("this is worker #%d" % num)
    return


if __name__ == "__main__":

    processes = list()
    for i in range(5):
        p = multiprocessing.Process(target=worker_function, args=(i,))
        processes.append(p)

    for p in processes:
        p.start()
