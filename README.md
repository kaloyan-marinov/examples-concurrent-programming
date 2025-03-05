# Introduction

At PyCon 2017, there was a talk by Miguel Grinberg
which was called "Asynchronous Python for the Complete Beginner".
The talk can be accessed via [this link](
    https://www.youtube.com/watch?v=iG6fr81xHKA
).

The following table is taken out of the talk;
it provides <u>a comparison of different styles/types of concurrent programming</u>:

|                          | multiple processes  | multiple threads    | asynchronous programming
| ------------------------ | ------------------- | ------------------- | ------------------------
| Optimize waiting periods | yes                 | yes                 | yes
|                          | (pre-emptive)       | (pre-emptive)       | (cooperative)
| Use all CPU cores        | yes                 | no                  | no
| Scalability              | low                 | medium              | high
|                          | (ones/tens)         | (hundreds)          | (thousands+)
| Use blocking standard-library functions | yes  | yes                 | no
| GIL interference         | no                  | some                | no

# Remarks about the non-trivial points

The preceding table compares processes, threads, and async on a number of categories.

(1) "Non-blocking, doing something while a task waits" is NOT exclusive to async.

   - processes and threads can do that pretty well too

   - in the case of processes,
     it's the operating system doing it;
     that is what the term **_pre-emptive_** stands for

   - in the case of threads,
     it's the operating system doing it;
     once again,
     that is what the term **_pre-emptive_** stands for

   - in the case of async,
     it's your chosen async framework (e.g. `asyncio`, `gevent`, `eventlet`) doing it;

(2) Many time people combine processes with one of the other two,
    which is actually a pretty good idea.

   - you create a multi-threaded program or an async program

   - you run that program as many as times as CPU cores you have

(3) The category about scalability is an interesting one.

   - if you're running multiple processes,
     each process will have
     (a) a copy of the Python interpreter; plus
     (b) all the resources that it uses; plus
     (c) a copy of your code, your application; plus
     (d) all the resources that you use;
     so, all of that is going to be duplicated
    
     so, if you start new instances,
     you're going to find that
     pretty soon you're going to probably run out of memory
     for the following reason:
     you cannot run a lot of Python processes on a normal computer

   - threads are a little bit more lightweight than processes;
     you can instantiate much more threads than processes;

   - async is done all in Python space;
     there are no resources at the operating-system level that are used;
     so these are extremely lightweight;

     (

        YouTube
        >>
        PyCon 2016
        >>
        Miguel Grinberg - Flask at Scale - PyCon 2016
        >>
        01:02:27 - 01:12:53

        https://www.youtube.com/watch?v=tdIIJuPh3SI
     
     ):
     "these" refers to data structures in the Python context;
     Python runs one thread,
     but what runs within that thread are all those "green threads"
     and there's a scheduler that comes with any async framework that
     decides how to switch between all those miniature "fake threads";
     you switch when you call certain functions;
     if you want to trigger a switch on purpose -
     which is sometimes necessary (e.g. the task is not I/O-bound),
     the way to do that is to call the `sleep` function from the async framework
     (but <u>not</u> the `time.sleep` function from the Python Standard Library);

(4) W.r.t. functions from the Python Standard Library
    that are implemented as blocking functions

   - processes and threads can use those functions without a problem
     (because the operating system knows how to deal with those)

   - since the async style of concurrent programming
     is enabled by your chosen async framework
     (rather than by the operating system),
     your program <u>has to</u> use
     the framework's replacements for the blocking standard-library functions
     (instead of those standard-library functions)

(5) GIL interference

   - the GIL causes some problems with threads

   - there are a lot of applications that are not affected by the GIL, namely
     (a) those that do not use threads, or
     (b) those that do use use threads but are mostly I/O-bound

if you have threads that are blocked on I/O, they don't hold the GIL;
so, if a thread goes to wait,
the operating system will be able to give access to another thread without any problems

the best argument for going with the async style of concurrent programming is
when you need <u>massive scaling</u>
(
so this will be servers that are going to be very busy;
want to handle lots of clients without having to buy more hosting,
which can become very expensive very quickly
)

# How to run the examples

```bash
examples-concurrent-programming $ python3 --version
Python 3.8.3
```


```bash
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2017_09_09_12_15/ex_parallelization.py
```

```bash
examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2017_09_09_12_16/message_passing/example_1.py



examples-concurrent-programming $ PYTHONPATH=. \
    python3 \
    examples_2017_09_09_12_16/example_1.py

# ...
```

```
the source for everything within `examples-concurrent-programming/examples_2025_03_03_15_36/` is:
(
    youtube
    >>
    Corey Schafer
    >>
    Python Threading Tutorial: Run Code Concurrently Using the Threading Module
)

each script within that folder has a docstring,
which contains an example of how to run that script
```

```
the source for everything within `examples-concurrent-programming/examples_2025_03_03_16_52/` is:
(
    youtube
    >>
    Corey Schafer
    >>
    Python Multiprocessing Tutorial: Run Code in Parallel Using the Multiprocessing Module
)

each script within that folder has a docstring,
which contains an example of how to run that script
```

```
the source for everything within `examples-concurrent-programming/examples_2025_03_03_17_26/` is:
(
    youtube
    >>
    mCoding
    >>
    Unlocking the CPU cores in Python (multiprocessing)
)

each script within that folder has a docstring,
which contains an example of how to run that script
```
