'''
Optional functionality.
'''


import resource

from tornado import gen


def get_proc_status(keys = None):
    '''Read current Linux process' status. Examine keys by running 
    ``cat /proc/self/status``.'''
    
    with open('/proc/self/status') as f:
        data = dict(map(str.strip, line.split(':', 1)) for line in f)
    
    return tuple(data[k] for k in keys) if keys else data


class ResourceReporter:
    
    sleep_time = 10
    '''Send reports per given number of seconds'''

    _ioloop = None
    '''Tornado IO loop'''
    
    _statsd = None
    '''Metrics client'''
    
    _prefix = None
    '''Stasd gauge prefix for worker processes monitoring'''
    
    _running = None
    '''Running flag'''
    
    _last_cpu_time = None
    '''Used CPU time form previous iteration'''
    
    _use_proc_status = None
    '''Whether ``/proc/self/status`` is available'''
    
    
    def __init__(self, ioloop, statsd, prefix = 'process'):
        self._ioloop = ioloop
        self._statsd = statsd
        self._prefix = prefix
        
        try:
            get_proc_status()
        except FileNotFoundError:
            self._use_proc_status = False
        else:
            self._use_proc_status = True
    
    def _report_cpu(self, usage, pipe):
        cpu_usage = usage.ru_utime + usage.ru_stime
        if self._last_cpu_time is not None:
            pipe.gauge('{}.cpu'.format(self._prefix), 
                (cpu_usage - self._last_cpu_time) / self.sleep_time)
        self._last_cpu_time = cpu_usage
    
    def _report_memory(self, usage, pipe):
        if self._use_proc_status:
            peak, current = get_proc_status(('VmHWM', 'VmRSS'))
            pipe.gauge('{}.maxrss'.format(self._prefix), int(peak.split(maxsplit = 1)[0]))
            pipe.gauge('{}.rss'.format(self._prefix), int(current.split(maxsplit = 1)[0]))
        else:
            pipe.gauge('{}.maxrss'.format(self._prefix), usage.ru_maxrss)
    
    def _report_ioloop(self, usage, pipe):
        pipe.gauge('{}.ioloop.handler'.format(self._prefix),  len(self._ioloop._handlers or ()))
        pipe.gauge('{}.ioloop.callback'.format(self._prefix), len(self._ioloop._callbacks or ()))
        pipe.gauge('{}.ioloop.timeout'.format(self._prefix),  len(self._ioloop._timeouts or ()))
    
    @gen.coroutine
    def _worker(self):
        while self._running:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            with self._statsd.pipeline() as pipe:
                self._report_cpu(usage, pipe)
                self._report_memory(usage, pipe)
                self._report_ioloop(usage, pipe)
                
            yield gen.sleep(self.sleep_time)
    
    def start(self):
        self._running = True
        self._ioloop.add_callback(self._worker)
    
    def stop(self):
        self._running = False

