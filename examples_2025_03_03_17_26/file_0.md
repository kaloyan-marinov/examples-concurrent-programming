One option for getting a Python program, script, or function to execute faster
<u>might</u> be to utilize all of the computing power (= computing resources = CPU resources)
that are available on the host machine.

In Python, there are three big contenders for how to deal with multiple tasks.
There's `asyncio`, `threading`, and `multiprocessing`.

---

<b>_As the name suggests, `asyncio` is primarily concerned with I/O-bound operations._</b>

(1) `asyncio` is built
    to allow tasks to cooperatively pause themselves
    and allow other tasks to run,
    particularly while they're doing nothing, just waiting.

(2) So, if the bulk of your program time is spent
    reading from disk,
    or writing to disk,
    or waiting on a network connection,
    then `asyncio` might be a good choice.

---

<b>_using multiple threads in Python_</b>

Python is just running on a single thread on a single CPU.

And here's where we get to the big elephant in the room with Python and threads.

Python - well specifically CPython - has what's called <u>the Global Interpreter Lock (GIL)</u>.

> A lock is a synchronization primitive that,
> in concurrent programming based on multiple threads,
> prevents different threads from accessing the same data at the same time.
>
> In particular, to prevent one thread from reading or writing some data
> while another thread is writing to it,
> only one thread can acquire this lock at a time,
> which is ensured by your operating system and by your actual hardware.
>
> If two threads are trying to access the same data at the same time,
> (a) one of them will get the lock first, and it's able to do its thing;
> (b) then it releases the lock;
> and (c) the other one can grab it.

Well, as the name suggests,
the Global Interpreter Lock is
<u>a global lock around the entire Python interpreter</u>.

In order to advance the Python interpreter state and run any Python code,
a thread must acquire the GIL.

So, while it's possible to have multiple threads in the same Python process,
only one of those threads can actually be executing any Python code. (While that's happening, all the other threads just have to sit around and wait.)

Now, we did still get some speedup here.

And the reason for that is simple.

You only need to acquire the GIL to run Python code.
Your Python code can then call out
to C code or other external code that
doesn't care about the Python interpreter;
during that time, it can
(A) drop the GIL,
(B) let another Python thread do its thing,
and (C) wait on that C code to finish simultaneously.

(
For example:

That is what happens when we read and write files to disk.
At the OS level,
it's possible to wait on multiple files to read and write at the same time.

And that's where <u>some</u> execution speedup can be achieved.
)

Threading in Python can still be useful for:

- for I/O-bound things

- in a GUI application, where you want to run a long-running calculation off the main thread to maintain responsiveness.

---

<b>_`multiprocessing` for our compute-bound tasks_</b>

While you may eventually need to dive down to the level of managing single processes,
most of the time you don't need the `multiprocessing.Process` object.

I'd say 90% of the time, what you really want is a `multprocessing.Pool` object.
- It represents a process pool.
- You just tell it what tasks you want to execute.
- It takes care of creating the processes, scheduling the tasks.
- And collecting the results, all in a thread and process-safe way.
- You can control the maximum number of processes (as part of the statement that creates the process pool). But if you just leave it blank, it'll just use one process per CPU.
- It can be used via a `with` statement to ensure that all the processes coordinate and terminate gracefully.

Each process has its own Python interpreter.
- In particular, they no longer have to fight over the GIL.
- They all own their own GIL.
