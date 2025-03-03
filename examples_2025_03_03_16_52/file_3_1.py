"""
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2025_03_03_16_52/file_3_1.py 
starting to sleep for 1.1 second(s)
starting to sleep for 1.1 second(s)
the execution of the main script finished after 1.27 seconds(s)
"""

import multiprocessing
import time


from examples_2025_03_03_15_36.file_1 import do_something


if __name__ == "__main__":
    time_start = time.perf_counter()

    p_1 = multiprocessing.Process(
        target=do_something,
        args=(1.1,),
    )
    p_2 = multiprocessing.Process(
        target=do_something,
        args=(1.1,),
    )

    p_1.start()
    p_2.start()

    # Enforce that both `Process`es should finish executing
    # before the Python interpreter goes on to execute the rest of the main script
    p_1.join()
    p_2.join()

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
