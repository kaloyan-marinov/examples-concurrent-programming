"""
Source:     Multiprocessing in Python - Rudy Gilmore, Data Scientist, TrueCar
            https://www.youtube.com/watch?v=X2mO1O5Nuwg
"""

# TODO: look into threads, processes, and Python's GIL


from __future__ import print_function
from __future__ import division

import threading
import multiprocessing

from timer import Timer


IND_OF_PRIME_NUM = 20000
INDICES_OF_DESIRED_PRIMES = [i + IND_OF_PRIME_NUM for i in range(4)]


def is_prime(x):
    sqrt_of_x = int(x**0.5) + 1

    for cur_integer in range(2, sqrt_of_x):
        if x % cur_integer == 0:
            return False

    return True


def get_nth_prime(n, q=None):
    """
    :param n:           int

    :param q:           multiprocessing.Queue object
                        enables sharing of data between processes

    :return nth_prime:  int
                        the n-th prime number

    :effect:            if q is provided, nth_prime gets *put* into q
    """
    num_primes_found = 0
    cur_integer = 0

    while num_primes_found < n:
        cur_integer += 1
        is_cur_integer_prime = is_prime(cur_integer)
        num_primes_found += int(is_cur_integer_prime)
    nth_prime = cur_integer

    if q:
        q.put(nth_prime)

    return nth_prime


def main(verbose=False, debug=False):
    """ """

    timer = Timer()

    # serial segment
    timer.start()

    for n in INDICES_OF_DESIRED_PRIMES:
        print(get_nth_prime(n))

    timer.stop()

    if verbose:
        print()
        print("serial")
        print(timer.build_report_of_totals())

    # multi-threading segment
    timer.restart()

    threads = list()
    for n in INDICES_OF_DESIRED_PRIMES:
        t = threading.Thread(target=get_nth_prime, args=(n,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    timer.stop()

    if verbose:
        print()
        print("multi-threading")
        print(timer.build_report_of_totals())

    # multi-processing segment
    timer.restart()

    mp_queue = multiprocessing.Queue()
    processes = list()
    for n in INDICES_OF_DESIRED_PRIMES:
        p = multiprocessing.Process(target=get_nth_prime, args=(n, mp_queue))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    timer.stop()

    if verbose:
        print()
        print("multi-processing")
        print(timer.build_report_of_totals())

    # BEGIN: pool-process segment
    timer.restart()

    mp_pool = multiprocessing.Pool(processes=len(INDICES_OF_DESIRED_PRIMES))
    results = mp_pool.map(get_nth_prime, INDICES_OF_DESIRED_PRIMES)

    timer.stop()

    if verbose:
        print()
        print("pool-process segment")
        print(results)
        print(timer.build_report_of_totals())


# END: function definitions
# -------------------------


if __name__ == "__main__":
    main(verbose=True, debug=True)
