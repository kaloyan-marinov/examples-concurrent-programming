import concurrent.futures
import time

from file_1 import do_something


if __name__ == "__main__":

    time_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as t_p_e:
        second_amounts = [5, 4, 3, 2, 1]

        # Schedule several executions of a function.
        futures = [t_p_e.submit(do_something, s_a) for s_a in second_amounts]

        # The following iterator yields the results of the threads,
        # as they are completed.
        for f in concurrent.futures.as_completed(futures):
            print(f.result())

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
