import threading
import time

from file_1 import do_something


if __name__ == "__main__":
    time_start = time.perf_counter()

    threads = []
    for _ in range(10):
        t = threading.Thread(
            target=do_something,
            args=(1.2,),
        )
        t.start()
        threads.append(t)

    # Enforce that both `Thread`s should finish executing
    # before the Python interpreter goes on to execute the rest of the main script
    for t in threads:
        t.join()

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
