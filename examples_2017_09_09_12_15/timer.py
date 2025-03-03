import time


class Timer(object):
    """
    This class implements a simple timer for Unix-like systems,
    which measures CPU and wall-clock time durations
    between calls to the start() and stop() methods.
    """

    report_str = "\n".join(
        [
            "cpu : %.5f",
            "wall: %.5f",
        ]
    )

    def __init__(self):
        self.total_cpu = None
        self.total_wall = None
        self.reset()

        self.start_cpu = None
        self.start_wall = None

    def reset(self):
        self.total_cpu = 0.0
        self.total_wall = 0.0

    def start(self):
        self.start_cpu = time.clock()
        self.start_wall = time.time()

    def restart(self):
        self.reset()
        self.start()

    def stop(self):
        cpu_time_since_last_start = time.clock() - self.start_cpu
        wall_time_since_last_start = time.time() - self.start_wall

        self.total_cpu += cpu_time_since_last_start
        self.total_wall += wall_time_since_last_start

    def get_totals(self):
        return self.total_cpu, self.total_wall

    def build_report_of_totals(self):
        return self.report_str % self.get_totals()
