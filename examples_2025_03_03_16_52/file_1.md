the following is an excerpt from [the official docs about the `threading` module](
    https://docs.python.org/3/library/threading.html
):
> CPython implementation detail:
> In CPython, due to the Global Interpreter Lock,
> only one thread can execute Python code at once
> (even though certain performance-oriented libraries might overcome this limitation).
> If you want your application to make better use
> of the computational resources of multi-core machines,
> you are advised to use `multiprocessing`
> or `concurrent.futures.ProcessPoolExecutor`.
> However, threading is still an appropriate model
> if you want to run multiple I/O-bound tasks simultaneously.

the following is an excerpt from [the official docs about the `multiprocessing` module](
    https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing
):
> <b>See also:</b>
> `concurrent.futures.ProcessPoolExecutor` offers
> a higher level interface to push tasks
> to a background process
> without blocking execution of the calling process.
> Compared to using the `Pool` interface directly,
> the `concurrent.futures` API more readily allows
> the submission of work to the underlying process pool
> to be separated from
> waiting for the results.
