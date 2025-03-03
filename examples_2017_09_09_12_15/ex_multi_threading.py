"""
source: https://www.youtube.com/watch?v=PJ4t2U15ACo

Given a list of numbers:
    
    print squares

    print their cubes
"""

import time
import threading

from timer import Timer


ARTIFICIAL_TIME_LAG = 0.2


def print_squares(numbers):
    print("executing print_squares()")

    for x in numbers:
        time.sleep(ARTIFICIAL_TIME_LAG)
        y = x**2
        print("square: %.5f" % y)


def print_cubes(numbers):
    print("executing print_cubes()")

    for x in numbers:
        time.sleep(ARTIFICIAL_TIME_LAG)
        y = x**3
        print("cube: %.5f" % y)


def main(verbose=False):

    arr = [2, 17, 8, 9, -1]

    timer = Timer()

    # serial segment
    timer.start()

    print_squares(arr)
    print_cubes(arr)

    timer.stop()

    if verbose:
        print()
        print("serial")
        print(timer.build_report_of_totals())

    # multi-threading
    timer.restart()

    thread_1 = threading.Thread(target=print_squares, args=(arr,))
    thread_2 = threading.Thread(target=print_cubes, args=(arr,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    timer.stop()

    if verbose:
        print()
        print("multi-threading")
        print(timer.build_report_of_totals())


if __name__ == "__main__":
    main(verbose=True)
