"""
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2025_03_03_16_52/file_3_4.py 
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
starting to sleep for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
slept for 1.4 second(s)
the execution of the main script finished after 2.26 seconds(s)
"""

import concurrent.futures
import time

from examples_2025_03_03_15_36.file_1 import do_something


if __name__ == "__main__":

    time_start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as t_p_e:
        # Schedule several executions of a function.
        futures = [t_p_e.submit(do_something, 1.4) for _ in range(10)]

        # The following iterator yields the results of the processes,
        # as they are completed.
        for f in concurrent.futures.as_completed(futures):
            print(f.result())

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
