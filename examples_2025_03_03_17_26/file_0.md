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

---

7:56
Next, let's take a look at just a few of  the ways where everything can go wrong.
8:00
Let's just take a look at a few different scenarios.
8:02
One, running normally on just a single CPU.
8:06
And the other running multiprocessing  using the pool stuff that we just talked about.
8:11
In the normal case, I'll just map the given  function `do_work` over the given set of items.
8:15
And then convert it to a list.
8:17
And in the multiprocessing case, we'll use `pool.map`.
8:20
Pitfall number 1
8:21
Trying to use multiprocessing in a situation
8:24
where the overhead of creating  processes and communicating between them
8:28
is greater than the cost of just doing the computation.
8:31
Suppose all we wanted was a quick calculation, like multiplying by 10.
8:35
Let's see how the multiprocessing and normal cases compare.
8:38
Using multiprocessing, it took 0.77 seconds.
8:42
But just doing the computation outright on a single CPU took less than 100th of a second.
8:47
Creating processes and communicating between them can be very expensive.
8:50
So keep that in mind and only apply multiprocessing to things
8:53
that are already taking a long time.
8:56
Pitfall number 2
8:57
Trying to send or receive something across process boundaries that's not picklable.
9:01
Threads share virtual memory.
9:02
So a variable that you create in one thread can be accessed in another thread.
9:07
Processes, on the other hand, have their own address space and do not share virtual memory.
9:12
Without specifically using something like shared memory,
9:15
a process cannot access variables from another process.
9:18
The way multiprocessing gets around this is by serializing everything using pickle.
9:23
It then uses an inter-process communication method like a pipe,
9:26
to send bytes from one process to another.
9:29
The takeaway is that you can't send anything that isn't picklable.
9:32
If you try, you'll get an error like this.
9:34
In this case, this lambda function, `lambda x: x + 1`, is not a picklable object.
9:39
Of course, the same thing goes for the result objects.
9:41
You can't return anything that's not picklable.
9:44
Pitfall number 3: Trying to send too much data.
9:48
Remember, all the items that you're using need to be serialized and sent between processes.
9:52
If you have a lot of data, like NumPy arrays, then this can be a big slowdown.
9:56
Instead of passing the data from process to process,
9:59
consider sending a message like a string
10:02
that informs the other process how to create the data on its own.
10:06
For instance, in our audio example,
10:08
we didn't read the wave files here and then send them over.
10:11
Instead, we just passed the file name and had the separate process load the file itself.
10:16
Pitfall number 4
10:17
Using multiprocessing when there's a lot of shared computation between tasks.
10:21
Here's a basic Fibonacci implementation.
10:24
We want to compute the first ten thousand Fibonacci numbers.
10:27
We go ahead and try our  experiment, and what do you know?
10:30
Doing it on eight cores was actually faster than doing it on one.
10:34
But of course, we've been tricked.
10:35
It is a huge waste to be computing these ten thousand Fibonacci numbers
10:39
independent of each other since there's so much overlap.
10:41
If we just changed our implementation to reuse shared computation,
10:44
then we could compute the first ten thousand Fibonacci numbers instantly.
10:49
And pitfall number 5: Not optimizing the chunk size.
10:53
`map`, `imap`, and `imap_unordered` all take a chunk size parameter.
10:58
Instead of submitting each item as a separate task for the pool, items are split into chunks.
11:04
Then, when a worker grabs more work, it grabs an entire chunk of work.
11:08
Bigger chunks allow individual workers to have to take less trips back to the pool to get more work.
11:13
However, there's also a trade-off because a bigger chunk means
11:16
that you have to copy more items at once across process boundaries.
11:21
This could potentially cause you to run out of memory if your chunk size is too large.
11:25
If you're running out of memory, consider setting a smaller chunk size.
11:28
And also consider using `imap` or `imap_unordered` instead of `map`.
11:32
Remember, `map` keeps all of the answers in memory in a list.
11:35
Whereas, `imap` and `imap_unordered` can give you results as they come in
11:38
rather than storing all of the results all at once.
11:42
So, a larger chunk size tends to be faster but uses more memory.
11:45
And a smaller chunk size uses less memory but is slower.
11:49
So, if you really want to optimize the performance as much as you reasonably can in Python,  
11:53
then don't forget to optimize  that chunk size parameter as well.
