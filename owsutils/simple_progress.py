'''
Created on Jan 6, 2011

@author: jpr

Utility for simple Python progress meters.
'''

import time, sys
import locale
locale.setlocale(locale.LC_ALL, '')

class SimpleProgressMeter(object):
    def __init__(self, total):
        self.total = total
        self.count = 0
        self.start_time = time.time()
        self.update_frequency = 1
        self.draw()
    
    def update(self, count=1):
        self.count += count
        
        assert self.count <= self.total
        
        now = time.time()
        if ((now - self.last_update_time > self.update_frequency) or
            self.count == self.total):
            self.draw()
    
    def draw(self):
        # erase the line
        # list of these codes - http://en.wikipedia.org/wiki/ANSI_escape_code
        sys.stderr.write(chr(27) + '[1G') # cursor to 1st column
        sys.stderr.write(chr(27) + '[0K') # erase line
        now = time.time()
        self.last_update_time = now
        
        num_ticks = int(50 * float(self.count) / self.total)
        empty_ticks = 50 - num_ticks
        
        rate = self.count / (now - self.start_time)
        
        sys.stderr.write('[' + '#' * num_ticks
            + ' ' * empty_ticks + '] : %s items/sec, %s of %s' % 
            (locale.format('%0.02f', rate, grouping=True), 
                locale.format('%d', self.count, grouping=True),
                locale.format('%d', self.total, grouping=True)))
        # sys.stdout.flush()
        
        if self.count == self.total:
            sys.stderr.write("\n")

class ProgressMeter(SimpleProgressMeter):
    def __init__(self, total):
        self.message = ""
        SimpleProgressMeter.__init__(self, total)

    def __format_time(self, time_in_secs):
        secs = time_in_secs % 60
        time_in_secs /= 60
        mins = time_in_secs % 60
        hours = time_in_secs / 60

        return "%02d:%02d:%02d" % (hours, mins, secs)

    def paint_line(self, msg):
        sys.stderr.write(chr(27) + '[1G') # cursor to 1st column
        sys.stderr.write(chr(27) + '[0K') # erase line
        sys.stderr.write(msg)

    def set_message(self, msg):
        """ Set a message that shows up on the first line of the display.
        Also triggers a repaint. """
        self.message = msg
        now = time.time()
        if now - self.last_update_time > self.update_frequency:
            self.draw()

    def draw(self):
        # the cursor should be at the beginning of the first line when this
        # starts

        num_ticks = int(50 * float(self.count) / self.total)
        empty_ticks = 50 - num_ticks
        progress_bar = '[' + '#' * num_ticks + ' ' * empty_ticks + ']'

        now = time.time()
        self.last_update_time = now

        try:
            rate = self.count / (now - self.start_time)
            to_go = self.total - self.count
            time_to_go = to_go / rate
            eta_str = self.__format_time(time_to_go)
        except ZeroDivisionError:
            eta_str = "N/A"

        rate_info = "%s items/sec, %s of %s (ETA: %s)" %  (
            locale.format('%0.02f', rate, grouping=True), 
            locale.format('%d', self.count, grouping=True),
            locale.format('%d', self.total, grouping=True),
            eta_str)
        
        self.paint_line(self.message)
        sys.stderr.write("\n")
        self.paint_line(progress_bar)
        sys.stderr.write("\n")
        self.paint_line(rate_info)

        if self.count == self.total:
            sys.stderr.write("\n")
        else:
            sys.stderr.write(chr(27) + '[2F') # up two lines, back to the start

def main():
    pm = ProgressMeter(1000000)

    for i in xrange(1000000):
        for y in xrange(1000):
            pass
        if i % 100000 == 0:
            pm.message = "Item %d" % i

        pm.update()
    print "Just printing some other things here."
    
if __name__ == '__main__':
    main()

