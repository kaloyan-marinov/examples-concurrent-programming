# Table of contents

1. [Introduction](#introduction)

2. [Background](#background)

3. [The Global Interpreter Lock (GIL) in CPython](#the-global-interpreter-lock-gil-in-cpython)

4. [Remarks about non-trivial aspects of concurrent programming](#remarks-about-non-trivial-aspects-of-concurrent-programming)

5. [How to run the examples](#how-to-run-the-examples)

6. [Bibliography](#bibliography)

---

Section 1 draws a distinctions
between sequential programming and concurrent programming.
It goes on to compare different styles of concurrent programming.

At the risk of increasing this file's word count,
Section 2 recalls the notions of processes and threads,
which are of considerable importance in the context of computer programming.

Section 3 builds on the background recalled in Section 2
by describing the Global Interpreter Lock (GIL).
The GIL is a feature of the _CPython_ implementation of Python.
A good working understanding of the GIL is important
for anyone who wishes to do concurrent programming in Python.

Section 4 remarks on
non-trivial aspects of the different styles of concurrent programming.

Section 5 explains how to run the code examples within this repository.



# Introduction

In the context of computer programming,
the resource in [1] draws a distinction between these types of programming:

(A) <u>sequential programming</u>

   - the program runs in a known/deterministic/"stable" order,
     <b>_one statement at a time_</b>

(B) <u>concurrent programming</u>

   - the program runs in a way that allows it to "do multi-tasking"

   - the reason for the quotation marks in the preceding bulletpoint
     is that
     there are different subtypes/styles of concurrent programming;
     depending
     on the style used to implement a computer program
     and
     on the hardware used to run the computer program,
     one of two things can take place:

     <b>_EITHER the hardware simply gives the illusion of "doing multi-tasking",_</b>

     <b>_OR the hardware actually does run multiple instructions simultaneously_</b>

   - be advised that,
     even if the hardware simply gives the illusion of "doing multi-tasking",
     the time required to run a program based on concurrency techniques
     _might_ be less than
     the time required to run an equivalent program based on the sequential technique

---

The following table is taken out of the resource in [2].
It provides <u>a comparison of different styles of concurrent programming</u>:

|                          | multiple processes  | multiple threads    | asynchronous programming
| ------------------------ | ------------------- | ------------------- | ------------------------
| Optimize waiting periods | yes                 | yes                 | yes
|                          | (pre-emptive)       | (pre-emptive)       | (cooperative)
| Use all CPU cores        | yes                 | no                  | no
| Scalability              | low                 | medium              | high
|                          | (ones/tens)         | (hundreds)          | (thousands+)
| Use blocking standard-library functions | yes  | yes                 | no
| GIL interference         | no                  | some                | no



# Background

In the context of computer programming,
the following notions are of considerable importance:
<u>processes</u> and <u>threads (of execution)</u>.

What follows is taken out of the resource in [3].

To get our bearings,
let us begin by pointing out a commonality between processes and threads:
both are ways of "doing multi-tasking".

A process:

   - is a computing construct
     that represents an environment (or a context),
     within which a computer program is executed

   - has its own virtual memory or an address space

Threads:

   - are computing constructs that exist within a process

   - share their encompassing process's address space,
     but each thread has its own stack memory and its own set of instructions

   - can access global variables defined in the program

   - can access heap memory

How do process communicate with each other?

   - a file on disk

   - shared memory

   - message pipe

Differences between processes and threads:

   - an error or memory leak in one process
     will not hurt
	 the execution of another process

   - that is not necessarily the case for threads

---

The resource in [1] makes some additionals points about threads.
Those points are as follows.

   - threads are spawned by a main program

   - threads may interrupt one another

   - threads may communicate (important) information
     to one another or to the main program in several ways;
     some of those ways are by:
     (a) creating "events";
     (b) passing information as arguments;

   - threads must safeguard against modifying the same code
     in multiple places or in an undesired order;
     that is called <u>synchronization</u>

   - <u>a lock</u> is a synchronization mechanism
     for enforcing access to sensitive/critical areas of program code -
     such as:

        - shared memory

        - global data/variables

      ```python
      # Thread 1
      x = 0
      x_lock = threading.Lock()
      with x_lock:
          x = x + 1 # critical section



      # Thread 2
      x = 0
      x_lock = threading.Lock()
      with x_lock:
          x = x - 2 # critical section
      ```




# The Global Interpreter Lock (GIL) in CPython

TBD



# Remarks about non-trivial aspects of concurrent programming

Recall that
the [Introduction](#introduction) section contains a table
that compares processes, threads, and async on a number of categories.

The talk, which that table was taken out of, makes
some remarks about non-trivial aspects of concurrent programming.
Those remarks are as follows.

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
the source for everything within `examples-concurrent-programming/examples_2025_03_03_17_26/` is
the resource in [4]

each script within that folder has a docstring,
which contains an example of how to run that script
```



# Bibliography

[1]

(
YouTube
\>>
Standford Scholar
\>>
Python: 3.2 - Multi threading
)

https://www.youtube.com/watch?v=xz3KgbftMes

[2]

(
YouTube
\>>
PyCon 2017
\>> Miguel Grinberg Asynchronous Python for the Complete Beginner PyCon 2017
)

https://www.youtube.com/watch?v=iG6fr81xHKA

[3]

(
YouTube
\>>
codebasics
\>> Difference between Multiprocessing and Multithreading
)

https://www.youtube.com/watch?v=oIN488Ldg9k

[4]

(
YouTube
\>>
mCoding
\>>
Unlocking the CPU cores in Python (multiprocessing)
)

https://www.youtube.com/watch?v=X7vBbelRXn0
