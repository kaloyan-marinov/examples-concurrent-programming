Wouldn't it be great if we could utilize all of our computing power to get the job done faster?
1:47
There are three big contenders for how to deal with multiple tasks in Python.
1:51
There's asyncio, threading, and multiprocessing.
1:55
As the name suggests, asyncio is primarily concerned with I/O-bound operations.
2:01
Asyncio is built to allow tasks to cooperatively pause themselves.
2:05
And allow other tasks to run,
2:07
particularly while they're doing nothing, just waiting.
2:10
So, if the bulk of your program  time is spent reading or writing to disk
2:13
or waiting on a network connection,
2:15
then asyncio might be a good choice.
2:17
While we're definitely reading and writing files,
2:19
assume, for the sake of the argument,
2:21
that the transformation step, the one we're actually doing raw computation,
2:25
is where the bulk of the time is spent.
2:27
In that case, we'd say we're compute-bound.  And asyncio wouldn't be a good fit.
2:31
Okay, what about using threads?
2:33
In a lot of languages besides Python, using threads would be the answer here.
2:38
The ultimate reason that we didn't see 100% CPU utilization was because
2:42
Python is just running on a single thread on a single CPU.
2:45
That one CPU might have been close to maxed out.
2:48
But the seven others were just sitting idle.
2:50
However, just take a look and see what happens
2:52
when we swap things out for a threading solution.
2:55
Here's the CPU monitor again.
2:57
And let's run it. Okay, here we go.
3:01
Things look like they're going well.
3:03
But we're still only getting 32-31% CPU utilization.
3:07
It was a little bit faster, almost eight seconds, not 12.
3:11
But we still didn't get anywhere close to full CPU utilization.
3:14
With seven extra cores, we should expect things to go six or seven times faster.
3:19
And here's where we get to the big elephant in the room with Python and threads.
3:23
Python, well specifically CPython,
3:25
which is the Python that 99% of you are going to be using,
3:28
has what's called the Global Interpreter Lock (GIL).
3:31
A lock is a parallel processing primitive
3:34
that helps threads prevent themselves from accessing the same data at the same time.
3:38
In particular, to prevent one thread from reading or writing some data
3:42
while another thread is writing to it.
3:43
Only one thread can acquire this lock at a time,
3:46
which is ensured by your operating system and by your actual hardware.
3:50
If two threads are trying to access the same data at the same time,
3:53
one of them will get the lock first, and it's able to do its thing.
3:56
Then it releases the lock, and the other one can grab it.
3:59
Well, as the name suggests,
4:01
the Global Interpreter Lock is a global lock around the entire Python interpreter.
4:07
In order to advance the interpreter state and run any Python code,
4:10
a thread must acquire the GIL.
4:13
So, while it's possible to have multiple Python threads in the same process,
4:16
only one of those threads can  actually be executing any Python code.
4:20
While that's happening, all the other threads just have to sit around and wait.
4:23
Now, we did still get some speedup here.
4:25
And the reason for that is simple.
4:27
You only need to acquire the GIL to run Python code.
4:30
Your Python code can then call out to C code or other external code
4:33
that doesn't care about the interpreter.
4:35
During this time, it can drop the GIL, let another Python thread do its thing.
4:39
And wait on that C code to finish simultaneously.
4:43
In our case, this is what happens when we read and write files to disk.
4:46
At the OS level. It's possible to wait on multiple files to read and write at the same time.
4:51
And that's where the savings is happening here.
4:53
However, for our transform operations, we don't get so lucky.
4:57
Threading in Python can still be useful, mostly for I/O-bound things.
5:00
But it can also be useful in say a GUI application
5:03
where you want to run a long-running calculation
5:05
off the main thread to maintain responsiveness.
5:08
However, in Python, at least for the near future,
5:10
we're not going to be able to use threading to get maximum utilization out of our CPU.
5:15
Therefore, we turn to the third option, multiprocessing, for our compute-bound tasks.
5:20
In our case, it's going to work fantastically
5:22
because all of our tasks are completely independent of each other.
5:25
Processing one audio file has no impact on processing any others.
5:30
While you may eventually need to dive down to the level of managing single processes,
5:34
most of the time, you don't need the process object.
5:37
I'd say 90% of the time, what you really want is a pool object.
5:41
A pool object represents a process pool.
5:44
You just tell it what tasks you want to execute.
5:47
It takes care of creating the processes, scheduling the tasks.
5:50
And collecting the results, all in a thread and process-safe way.
5:54
You can control the maximum number of processes that you want it to start like this.
5:58
But if you just leave it blank, it'll just use one per CPU.
6:01
Each process is its own Python interpreter.
6:04
In particular, they no longer have to fight over the GIL.
6:06
They all own their own GIL.
6:08
We're using a with statement here to ensure that all the processes coordinate and terminate gracefully.
6:14
There are three basic methods that the pool offers.
6:16
map, imap, and imap_unordered.
6:19
`imap_unordered` immediately returns an iterator.
6:22
Then asking for an actual element  of the iterator is what blocks.
6:26
`imap_unordered` will return the results to you in whatever order they finish in.
6:30
So, if some tasks complete quicker, you'll get those back faster.
6:33
Let's see how it goes.
6:39
I don't know if you saw it, but we did have a full spike to 100% CPU utilization.
6:43
And the total time was only three and a half seconds.
6:46
Also, notice that because we used the unordered version, our results did not come back in their original order.
6:52
This is actually part of the reason that I  return the input file name as part of the result.
6:57
If I'm getting things out of order, I need to know which task this corresponded to.
7:01
Let's try again with the normal `imap`.