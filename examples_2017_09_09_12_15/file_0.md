# multi-threading in the _CPython_ implementation of Python

(
source:
https://www.youtube.com/watch?v=PJ4t2U15ACo
)

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

multi-threading

   - pros

     - more responsive UIs

     - simpler program design (by separating tasks into independent thread bodies)

     - threads can act independently of one another

   - cons

     - faux-parallelism in Python (due to the GIL) :
       _might_ not benefit from any speed improvements

     - can add complexities and severe debugging headaches
       (because of its non-deterministic nature)
