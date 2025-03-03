"""
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2025_03_03_15_36/file_3_3.py
starting to sleep for 1.3 second(s)
slept for 1.3 second(s)
the execution of the main script finished after 1.31 seconds(s)
"""

import concurrent.futures
import time

from file_1 import do_something


if __name__ == "__main__":

    time_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as t_p_e:
        # Schedule a function to be executed.
        # The returned value is a "future" object;
        # that object enables us to check in on the execution of our function
        # _after_ it has been scheduled;
        # in particular, that object enables us to check
        # [if] it's running, or if it's done, and also to check the result
        f = t_p_e.submit(do_something, 1.3)

        # The next call causes it to wait aroud
        # until the scheduled function completes.
        r = f.result()

        print(r)

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
