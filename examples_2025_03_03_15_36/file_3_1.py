import threading
import time

from file_1 import do_something


if __name__ == "__main__":
    time_start = time.perf_counter()

    t_1 = threading.Thread(
        target=do_something,
        args=(1,),
    )
    t_2 = threading.Thread(
        target=do_something,
        args=(1,),
    )

    t_1.start()
    t_2.start()

    # Enforce that both `Thread`s should finish executing
    # before the Python interpreter goes on to execute the rest of the main script
    t_1.join()
    t_2.join()

    time_final = time.perf_counter()

    main_script_duration = round(time_final - time_start, 2)
    print(
        f"the execution of the main script finished after {main_script_duration} seconds(s)"
    )
