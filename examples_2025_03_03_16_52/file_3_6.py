"""
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2025_03_03_16_52/file_3_6.py
starting to sleep for 5 second(s)
starting to sleep for 4 second(s)
starting to sleep for 3 second(s)
starting to sleep for 2 second(s)
starting to sleep for 1 second(s)
slept for 5 second(s)
slept for 4 second(s)
slept for 3 second(s)
slept for 2 second(s)
slept for 1 second(s)
the execution of the main script finished after 5.45 seconds(s)
"""

import concurrent.futures
import time

from examples_2025_03_03_15_36.file_1 import do_something


if __name__ == "__main__":

    time_start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as p_p_e:
        second_amounts = [5, 4, 3, 2, 1]

        # The following still gets the function executions to take place concurrently,
        # but returns the results in the order
        # in which the function executes were scheduled/started.
        results = p_p_e.map(do_something, second_amounts)

        for r in results:
            print(r)

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
