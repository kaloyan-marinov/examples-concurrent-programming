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

Now, we did still get some speedup here.

And the reason for that is simple.
[
A thread only needs to acquite the GIL to run Python code;
if it calls out to external code that doesn't care about the Python interpreter,
the thread in question can and does release the GIL,
which in turn allows another thread to acquire the GIL and execute its own instructions.
]

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

---


<b>_a few of the ways where everything can go wrong_</b>



<u>Pitfall number 1:</u>

Trying to use `multiprocessing` in a situation where
the overhead of creating processes and communicating between them
is greater than
the cost of just doing the computation.

Creating processes and communicating between them can be very expensive.

So keep that in mind
and
only apply `multiprocessing` to things that are already taking a long time.



<u>Pitfall number 2:</u>

Trying to send or receive something across process boundaries that's not picklable.

Threads share virtual memory. So a variable that you create in one thread can be accessed in another thread.

Processes, on the other hand, have their own address space and <u>do not</u> share virtual memory. Without specifically using something like shared memory, a process cannot access variables from another process.

- The way `multiprocessing` gets around this is by serializing everything using `pickle`. It then uses an inter-process communication method like a `multiprocessing.Pipe` to send bytes from one process to another.

- The takeaway is that you can't send anything that isn't picklable. (If you try, you'll get an error.)

- Of course, the same thing goes for the result objects. You can't return anything that's not picklable.


<u>Pitfall number 3:</u>

Trying to send too much data.

Remember, all the items that you're using need to be serialized and sent between processes.

If you have a lot of data, like `numpy` arrays,
then this can be a big slowdown.

Instead of passing the data from process to process,
consider sending a message like a string
that informs the other process how to create the data on its own.



<u>Pitfall number 4:</u>

Using `multiprocessing` when there's a lot of shared computation between tasks.

It is a huge waste to be computing/processing/performing tasks independently of one other
<u>provided</u> there is considerable overlap among the tasks in question.

In such a situation, it <u>might</u> be worth changing the implementation in a way that re-uses shared computation.



<u>Pitfall number 5:</u>

Each of the `map`, `imap`, and `imap_unordered` methods
that are available on the `multiprocessing.Pool` object
takes a `chunksize` parameter.

- Instead of submitting each item as a separate task for the pool, items are split into chunks.

- Then, when a worker grabs more work, it grabs an entire chunk of work.

- Bigger chunks allow individual workers to have to take fewer trips back to the pool to get more work.

However, there's also a trade-off because a bigger chunk means that you have to copy more items at once across process boundaries.

- This could potentially cause you to run out of memory if your `chunksize` is too large.

- If you're running out of memory, consider setting a smaller `chunksize`.

In summary:

(a)
So, a larger `chunksize` tends to be faster but uses more memory.

(b)
And a smaller `chunksize` uses less memory but is slower.

(c)
So, if you really want to optimize the performance as much as you reasonably can in Python,
then don't forget to optimize the `chunksize` parameter as well.



<u>Pitfall number 6:</u>

And also consider using `imap` or `imap_unordered` instead of `map`.

Remember, `map` keeps all of the answers in memory in a list.

Whereas, `imap` and `imap_unordered` can give you results as they come in rather than storing all of the results all at once.
