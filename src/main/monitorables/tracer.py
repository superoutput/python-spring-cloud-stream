from monitorables.monitorable import Monitorable
import sys
import inspect
from inspect import signature

class Tracer(Monitorable):
    def __init__(self, microservice, out):
        super().__init__(microservice)
        self._f = open(out, 'a+')
        self._current_filename = ''
        sys.settrace(self.trace_function)

    def fire(self, thread):
        #sys.settrace(self.trace_function)
        pass

    def listen(self, event):
        pass

    def trace_function(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name == 'write':
            return
        line_no = frame.f_lineno
        filename = co.co_filename
        if self._current_filename != filename:
            self._current_filename = filename
            #print(filename)
            self._f.write('%s\n' % filename)
        #print('  line %s\t%s%s' % (line_no, func_name, str(co.co_varnames).replace("'", "").replace(",)", ")")))
        self._f.write('  line %s\t%s%s\n' % (line_no, func_name, str(co.co_varnames).replace("'", "").replace(",)", ")")))
        #if func_name in TRACE_INTO:
        #    return trace_lines
        return

    def trace_lines(self, frame, event, arg):
        if event != 'line':
            return
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        print(' %s line %s'%(func_name, line_no))