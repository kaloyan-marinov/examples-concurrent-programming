import multiprocessing
import time


class Consumer(multiprocessing.Process):

    def __init__(self, task_tuple_queue, proxy_for_task_id_2_task_obj):
        multiprocessing.Process.__init__(self)
        self.task_tuple_queue = task_tuple_queue
        self.proxy_for_task_id_2_task_obj = proxy_for_task_id_2_task_obj

    def run(self):
        subprocess_name = self.name

        while True:

            task_tuple = self.task_tuple_queue.get()

            if task_tuple is None:
                # poison pill has been passed in, so shut down the process represented by self
                print("%s: exiting" % subprocess_name)
                self.task_tuple_queue.task_done()
                break
            else:
                task_obj = task_tuple

                # carry out task_obj
                print(task_obj.task_id)
                print(
                    "%s: executing task_id=%r [task_obj.__str__() = %s]"
                    % (subprocess_name, task_obj.task_id, task_obj)
                )
                answer = task_obj()
                self.task_tuple_queue.task_done()
                self.proxy_for_task_id_2_task_obj[task_obj.task_id] = answer

        return


class Task(object):
    def __init__(self, task_id, a, b):
        self.task_id = task_id

        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(0.1)  # pretend to take some time to do the work
        return "%s * %s = %s" % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return "%s * %s" % (self.a, self.b)


def main():

    # establish communication objects
    task_tuples = multiprocessing.JoinableQueue()

    manager = multiprocessing.Manager()
    proxy_for_task_id_2_task_obj = manager.dict()

    # create and start consumer subprocesses
    num_consumers = multiprocessing.cpu_count() * 2
    print("creating %d consumer subprocesses" % num_consumers)
    consumer_subprocesses = [
        Consumer(task_tuples, proxy_for_task_id_2_task_obj)
        for _ in range(num_consumers)
    ]

    for p in consumer_subprocesses:
        p.start()

    # enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        task_id = i
        task_tuples.put(Task(task_id, i, i))

    # add a poison pill for each consumer
    for i in range(num_consumers):
        task_tuples.put(None)

    # wait for all of the tasks to finish
    task_tuples.join()

    # start printing results
    print(proxy_for_task_id_2_task_obj)

    """
    proxy_for_results = dict(proxy_for_results)  # works with next line uncommented as well
    """
    """
    for k in proxy_for_results:  # does NOT work on its own
    """
    format_str = "{0:<10} {1:<20}"
    print()
    print(format_str.format("task_id", "task.__call__()"))
    print(format_str.format("-------", "---------------"))
    for k in proxy_for_task_id_2_task_obj.keys():  # works
        # print(k)
        result = proxy_for_task_id_2_task_obj[k]
        print(format_str.format(k, result))
        # print("result:", result)


if __name__ == "__main__":
    main()
