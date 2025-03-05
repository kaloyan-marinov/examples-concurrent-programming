# multi-processing vs. multithreading

(
source:
https://www.youtube.com/watch?v=oIN488Ldg9k
)

commonality

   - both are ways of achieving multi-tasking

a process

   - has its own memory within address space

   - constitutes an environment,
     within which multiple threads (of execution) can live

   - has the property that
	 all its threads of execution will share the process's address space
     (but each thread has its own stack memory and its own set of instructions) -
	 global variables defined in the program and heap memory
	 can all be accessed by each thread

how do processes communicate with each other?

   - a file on the disk

   - shared memory

   - message pipe

another difference:

   - an error or memory leak in one process
     will not hurt
	 the execution of another process

   - this is not necessarily the case for threads

# multi-threading in the _CPython_ implementation of Python

(
source:
https://www.youtube.com/watch?v=PJ4t2U15ACo
)

- is a little special
because there is something called the Global Interpreter Lock (GIL)

- the GIL _might_ prevent you from reaping the true benefits of multi-threading

- might still be beneficial - e.g. when you are

  - waiting

  - using I/O-bound operations
	
# multi-threading in Python

(
`./README.md` >> [1]
)

in the context of computer programming,
<u>a thread</u> is short for <u>a thread of execution</u>

analogy (by comparing a computer program to a bee hive)

   - the main program (or thread)

      - acts as the queen bee

      - assigns jobs to worker bee

   - each thread

      - shares access to the program's global variables

      - but maintains its own local variables and code blocks



concurrent programming

   - can be achieved in various ways,
     one of which is multi-threading

   - a multi-threaded program can do multi-tasking -
     but, on a computer with only one CPU, this is simply an illusion

   - this _may_ achieved by assigning each task to a thread

   - computers with multiple-core CPUs
     can actually run
     multiple instructions simultaneously

   - but:
     the _CPython_ implementation of Python
     has a feature called the Global Interpreter Lock (GIL),
     which limits a threaded Python program to run on only one core
     (allowing only one thread/task to be executed at a time;
     therefore, in order to give the illusion of multi-tasking,
     threaded Python programs must rapidly switch between threads)

multi-threading

   - threads

     - are spawned by the main program

     - may interrupt each other

     - may communicate (important) information
       to each other or to the main program
       in several ways;
	     some of those ways are by:
	     (a) creating Events;
	     (b) passing information as arguments;

   - pros

     - more responsive UIs

     - simpler program design (by separating tasks into independent thread bodies)

     - threads can act independently of one another

   - cons

     - faux-parallelism in Python (due to the GIL) :
       _might_ not benefit from any speed improvements

     - can add complexities and severe debugging headaches
       (because of its non-deterministic nature)

   - must safeguard against threads modifying sections of the same code
     in multiple places or in an undesired order;
     in programming, this is called <u>synchronization</u>

   - a <u>lock</u> is a synchronization mechanism
     for enforcing access to a sensitive/critical areas of the program code such as:

       shared memory

       global data/variables

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
