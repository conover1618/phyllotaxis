import time
class TicToc(object):
    """
    A simple code timer.
    From: http://bfroehle.com/2011/07/simple-timer/
    
    Example
    -------
    >>> with TicToc("Sleeping"):
    ...     time.sleep(2)
    Elapsed time is 2.000073 seconds.
    """
    def __init__(self, id='', do_print = True, print_close=False):
        self.do_print = do_print
        self.id = id
        self.print_close = print_close
    def __enter__(self):
        self.start_time = time.time()
        print "%s" % self.id
        return self
    def __exit__(self, type, value, traceback):
        self.elapsed = time.time() - self.start_time
        if self.do_print:
            if self.print_close:
                print "\t%s\t%f seconds." % (self.id, self.elapsed)
            else:
                print "\tElapsed: %f seconds." % (self.elapsed)