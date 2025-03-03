import concurrent.futures
import time

from file_1 import do_something


if __name__ == "__main__":

    time_start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as t_p_e:
        second_amounts = [5, 4, 3, 2, 1]

        # The following still gets the function executions to take place concurrently,
        # but returns the results in the order
        # in which the function executes were scheduled/started.
        results = t_p_e.map(do_something, second_amounts)

        for r in results:
            print(r)

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
