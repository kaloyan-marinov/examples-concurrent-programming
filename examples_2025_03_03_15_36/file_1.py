"""
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2025_03_03_15_36/file_1.py
starting to sleep for 1 second(s)
slept for 1 second(s)
starting to sleep for 1 second(s)
slept for 1 second(s)
the execution of the main script finished after 2.01 seconds(s)
"""

import time


def do_something(seconds: float) -> str:
    print(f"starting to sleep for {seconds} second(s)")

    time.sleep(seconds)

    return f"slept for {seconds} second(s)"


if __name__ == "__main__":
    time_start = time.perf_counter()

    result_1 = do_something(1)
    print(result_1)
    result_2 = do_something(1)
    print(result_2)

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
