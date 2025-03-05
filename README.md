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
