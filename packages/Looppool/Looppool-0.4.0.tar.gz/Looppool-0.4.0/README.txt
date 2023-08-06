.. image:: https://drone.io/bitbucket.org/saaj/looppool/status.png
    :target: https://drone.io/bitbucket.org/saaj/looppool/latest
.. image:: https://codecov.io/bitbucket/saaj/looppool/branch/default/graph/badge.svg
    :target: https://codecov.io/bitbucket/saaj/looppool/branch/default 
.. image:: https://badge.fury.io/py/Looppool.png
    :target: https://pypi.python.org/pypi/Looppool

********
Looppool
********
Looppool is a Python 3 package for running worker process pool of Tornado IO loops. It's useful
for a heavy asynchronous application which doesn't fit into single process due to increasing
CPU usage and suffers from IO loop blocking (see ``set_blocking_log_threshold`` [1]_).

It was developed as a part of performance optimisation of a Tornado data extraction application.
The application mixed IO-bound and CPU-bound tasks. Moreover, the CPU-bound tasks were highly
coupled with IO loop. Because of such coupling much simpler approach of ``concurrent.futures`` 
[3]_ wouldn't have helped.

Design
======
A picture worth a thousand words.

.. image:: https://bytebucket.org/saaj/looppool/raw/default/manual/overview.png
    :target: https://bbcdn.githack.com/saaj/looppool/raw/default/manual/overview.seq.violet.html

A few observations and notes:

1. Messages are off-loaded to IO loops immediately but task and result queues are
   protected by semaphores to not off-load more tasks on IO loops than the queue size. 
2. In fact there are ``n`` task queue, a queue per worker. Task messages are distributed
   evenly between workers.  
3. ``add_callback`` [2]_ is safe (and only safe) method to pass control from other
   thread to IO loop's thread.
4. Because queue message handlers (``fn1`` and ``fn2``) are called from IO loop
   they can be coroutines.
5. ``Pool`` stops its workers by sending ``PoisonPill`` task message per worker.

Worker
======
There is a base class for  a ``Worker``. It represents a process worker that runs its own
Tornado IO loop. It processes task messages and puts them in result queue (or just puts without 
receiving anything). It requires override of ``_process_message(self, task)`` in a subclass 
and mandates that once the task is done, ``self._task_done()`` is called (directly in 
``try-finally`` or with ``@task_done``), like::

    def _process_message(self, task):
        try:
            result = 'some processing'
            self._put_nowait(result)
        finally:
            self._task_done()

``WorkerSubclass._process_message`` may be plain function or coroutine. More details are 
available in the package's unit test module [5]_.

.. note::
    For ``Pool.process_message`` there is also requirement to call ``result_done`` argument
    once message is done. You can also wrap  it with ``@task_done`` in simple case when
    result is considered ingested on return of ``process_message``.
    
    Both requirements are bound to semaphores that limit running tasks and pending results. 
    It also affects how pool is stopped as it waits for running tasks to complete. 

Stateful worker
---------------
If you want to run stateful workers, for instance, use some periodically calculated lookup table,
but don't want to calculate it in every workers (e.g. burden of maintaining database connection),
you can send ``n`` tasks and each of ``n`` workers is guaranteed to receive it.

You can also send messages to workers individually. ``Pool.put_nowait`` has optional argument
``worker_num``.

.. note::
    If your process start method [4]_ is *fork* (default on \*nix platforms), you can share
    some static data from parent process.

Installation
============
.. sourcecode:: bash

    pip install Looppool
    
Usage
=====
.. note::
    Note that the following example has 1-to-1 correspondence of input to output messages.
    Because worker has IO loop at its disposal, it can, for example, subscribe to something 
    by input message and put results later without task message.

.. sourcecode:: python

    #!/usr/bin/env python3
    
    
    import looppool
    from tornado import gen, ioloop, httpclient
    
    
    class FetchWorker(looppool.Worker):
        
        _http_client = None
        '''Tornado asynchronous HTTP client'''
      
        
        def _initialise(self):
            self._http_client = httpclient.AsyncHTTPClient()
        
        @looppool.task_done
        @gen.coroutine
        def _process_message(self, url):
            response = yield self._http_client.fetch(url)
            self._put_nowait((url, response.headers.get('server')))
    
    
    @looppool.task_done
    def process_message(result, result_done):
        print(result)
    
    
    @gen.coroutine
    def main():
        loop = ioloop.IOLoop.instance()
        pool = looppool.Pool(loop, pool_size = 4, worker_class = FetchWorker)
        pool.process_message = process_message
        pool.start()
        
        urls = [
            'https://python.org/',
            'http://tornadoweb.org/',
            'https://google.com/',
            'https://stackoverflow.com/',
        ]
        list(map(pool.put_nowait, urls))
        
        pool.stop()
    
    
    if __name__ == '__main__':
        ioloop.IOLoop.instance().run_sync(main)

Maintenance
===========
Maintaining a process group instead of one process is more tricky thing to do. 
Initially, you may want to see if your pool instance has actually spawned any
processes. Here's what you can do visualise your process tree, which has main process,
one or two (depending on start method) ``multiprocessing`` helper processes, and processes
of your ``looppool`` pools (you can use different pools for different purposes):: 

    htop -p $(pgrep -d"," -g $(pgrep -f "main-process-name-or-its-start-args"))
    
``top`` will also work but is limited to 20 PIDs. Enforcing the process tree stop is also
different. If something goes wrong process tree should be killed like::

    kill -9 -- -$(pgrep -f "main-process-name-or-its-start-args")

Killing only main process will leave helper and worker processes running.

.. note::
    Pool workers intentionally ignore ``SIGINT`` and ``SIGTERM`` because these signals
    propagate to children from parent process and break normal, message-based shutdown.
    
You can improve the names of your worker processes by setting them in worker's 
initialiser with ``setproctitle`` [6]_ (see example below).

Monitoring
----------
Generally it's very important to know how well your application behaves. Even more 
important it is for single-threaded (asynchronous) and multi-process applications.
For the former is critical to know that the process doesn't use 100% CPU except for rare peaks,
which would otherwise impair IO loop's ability to schedule tasks. For the latter CPU usage 
shows how well current number of workers handle the load. This is being said about application
metrics.

``looppool`` comes with build-in ``loopppol.utility.ResourceReporter`` which periodically 
(10 seconds by default) sends metrics as CPU usage, memory usage (RSS) and length of IO 
loop backlogs (``ioloop._handlers``, ``ioloop._callbacks`` and ``ioloop._timeouts``) to 
statsd-compatible server [8]_.  


Logging
-------
Multi-process logging is complicated. Most important part of logging is error reporting.
Sentry [7]_ goes a great solution to error reporting problem. It seamlessly integrates
with ``logging`` and is suggested tool to know what errors occur in your workers.

Instrumentated worker
---------------------
For the following code you will need to run ``pip install raven statsd setproctitle``.

.. sourcecode:: python

    #!/usr/bin/env python3
    
    
    import logging
    
    import looppool
    from looppool.utility import ResourceReporter 
    from statsd import StatsClient
    from raven import Client
    from raven.exceptions import InvalidDsn
    from raven.handlers.logging import SentryHandler
    from setproctitle import setproctitle
    
    
    class InstrumentatedWorker(looppool.Worker):
    
        _resource_reporter = None
        '''CPU, RSS and IO loop stats reporter'''
        
        
        def _initialise(self):
            setproctitle('python APP_NAME POOL_NAME pool worker')
            
            statsd = StatsClient('localhost', 8125, 'APP_PREFIX')
            self._resource_reporter = ResourceReporter(self._ioloop, statsd,
                'worker.instrumentated.process.{}'.format(self._number))
            
            try:
                handler = SentryHandler(Client('SENTRY_DSN'))
                handler.setLevel(logging.WARNING)
            except InvalidDsn:
                logging.exception('Cannot configure Sentry handler')
            else:
                logging.basicConfig(handlers=[handler], level=logging.WARNING)
        
        @looppool.task_done
        def _process_message(self, message):
            self._put_nowait((message, self._number))
            
        def start(self):
            super().start()
            
            self._resource_reporter.start()
            
        def join(self):
            self._resource_reporter.stop()
            
            super().join()


.. [1] http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop.set_blocking_log_threshold
.. [2] http://www.tornadoweb.org/en/stable/ioloop.html#tornado.ioloop.IOLoop.add_callback
.. [3] https://docs.python.org/3/library/concurrent.futures.html
.. [4] https://docs.python.org/3/library/multiprocessing.html#multiprocessing.set_start_method
.. [5] https://bitbucket.org/saaj/looppool/src/default/looppool/test.py
.. [6] https://pypi.python.org/pypi/setproctitle
.. [7] https://pypi.python.org/pypi/sentry
.. [8] https://github.com/etsy/statsd/wiki#server-implementations
