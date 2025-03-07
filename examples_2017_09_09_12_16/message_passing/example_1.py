"""
A more complex example shows how to manage several workers
consuming data from a JoinableQueue instance
and passing results back to the parent process.

The "poison pill technique" is used to stop the workers:
    After setting up the real tasks,
    the main program adds one “stop” value per worker to the job queue.
    
    When a worker encounters the special value,
    it breaks out of its processing loop.
    
The main process uses the task queue's join() method to wait for all of the tasks to finish
before processing the results.
"""

import multiprocessing
import time


class ConsumerProcess(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        # since this subclasss overrides __init__(),
        # it must make sure that the base-class constructor is called
        # *before* doing anything else to the process
        multiprocessing.Process.__init__(self)

        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print("%s: Exiting" % proc_name)
                self.task_queue.task_done()
                break
            print("%s: %s" % (proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take some time to do the work
        return "%s * %s = %s" % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return "%s * %s" % (self.a, self.b)


if __name__ == "__main__":
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print("Creating %d consumers" % num_consumers)
    consumers = [ConsumerProcess(tasks, results) for i in range(num_consumers)]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print("Result:", result)
        num_jobs -= 1
