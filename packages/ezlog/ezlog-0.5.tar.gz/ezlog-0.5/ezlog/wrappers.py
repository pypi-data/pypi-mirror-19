import inspect
import logging
from timeit import default_timer as timer


default_log_level = logging.DEBUG
'''
Override for default logging level.
'''

default_performance_measure = False
'''
Override default behavior for measuring performance or not.
'''

default_logging = logging
'''
Override default logger.
'''

default_eps = 0.001
'''
Limit for prevent spamming extremely low measurements.
'''

default_one_line_log = False
'''
Override default logging style.
If True - log only one line (Called (args), result)
If False(default) - log in 2 lines (Calling... Done).
'''

default_log_arguments = True
'''
Override default settings to log arguments or not.
'''

default_log_result = False
'''
Override default settings to log function result or not.
'''


def __format_args(*args, **kwargs):
    args_str = str()
    kwargs_str = str()
    if len(args) != 0:
        args_str = " with args: {}".format(args)
    if len(kwargs) != 0:
        kwargs_str = " with kwargs: {}".format(kwargs)
    return args_str + kwargs_str


def __wrapper_impl(name, arg_fmt, f, opt, *args, **kwargs):
    log = opt.get("logger", default_logging)
    level = opt.get("level", default_log_level)
    measure = opt.get("measure", default_performance_measure)
    one_line = opt.get("one_line", default_one_line_log)
    log_arguments = opt.get("log_arguments", default_log_arguments)
    log_result = opt.get("log_result", default_log_result)

    if not log_arguments:
        arg_fmt = str()

    if not one_line:
        log.log(level, "Calling '{}'{}:".format(name, arg_fmt))
    try:
        if measure:
            start = timer()
        rv = f(*args, **kwargs)
        mesr_str = str()
        if measure:
            stop = timer()
            delta = stop - start
            if delta > default_eps:
                mesr_str = " and took: {}".format(delta)

        if one_line:
            prefix = "Call '{}'{} ".format(name, arg_fmt)
        else:
            prefix = "Done"

        if rv is None or not log_result:
            log.log(level, "{} '{}'{}".format(prefix, name, mesr_str))
        else:
            log.log(level, "{} '{}', with result: '{}'{}"
                    .format(prefix, name, rv, mesr_str))
        return rv
    except:
        log.exception("Done '{}' with exception")
        raise


def log_call(**opt):
    '''
    Wrapper to log function call.
    Not applicable to class member logging.

    Keyword arguments:

     level: int
      Default = ezlog.default_log_level
      Set log level for this call.

     one_line: bool
      Default = ezlog.default_one_line_log
      Allow to set different logging style.
      If True - log will be performed after call and looks like:
       'Called 'name', 'args' with result'
      If False - log will be performed before start and after start.

     log_arguments: bool
      Default = ezlog.default_log_arguments
      Should log function arguments or not.

     log_result: bool
      Default = ezlog.log_result
      Should log function result or not (if possible)

     measure: bool
      Default = ezlog.default_performance_measure
      Allow turn on or of performance measuring for this call.

     logger:
      Default = ezlog.default_logging
      Specify logger to be used.
      Expecting module or class with
       .log(int, str)
       .exception(str) functions.

    Example:
    ```python
    >>> @log_call() # Make sure you dont forget about ()
    ... def test(a, b):
    ...  print("test call")
    ...  return 4
    >>>  test(2, "test")

    DEBUG:root:Calling 'test' with arguments (2, "test")
    test call
    DEBUG:root:Done 'test' with result '4'
    ```
    '''
    def decorator(f):
        name = f.__name__

        def log_call_wrapper(*args, **kwargs):
            arg_fmt = __format_args(*args, **kwargs)
            return __wrapper_impl(name, arg_fmt, f, opt, *args, **kwargs)
        return log_call_wrapper
    return decorator


def log_member_call(**opt):
    '''
    Log call of class member function.
    (Not applicable for static or non class functions).
    For details see log_call.

    Example:
    ```python
    >>> class Test:
    ...  @log_member_call() # Make sure you dont forget about ()
    ...  def test(self, a, b):
    ...   print("test call")
    ...   return 4
    >>> t = Test()
    >>> t.test(2, "test")

    DEBUG:root:Calling 'Test.test' with arguments (2, "test")
    test call
    DEBUG:root:Done 'Test.test' with result '4'
    ```

    ```python
    class Test:
        @log_member_call(level = logging.CRITICAL)
        def test(self, a, b):
            print("test call {}, {}".format(a,b))
            return 4
    t = Test()
    print(t.test(2, "test"))
    CRITICAL:root:Calling 'Test.test' with args: (2, 'test'):
    test call 2, test
    CRITICAL:root:Done 'Test.test'
    ```
    '''
    def decorator(f):
        def log_member_call_wrapper(slf, *args, **kwargs):
            name = "{}.{}".format(slf.__class__.__qualname__, f.__name__)
            arg_fmt = __format_args(*args, **kwargs)
            return __wrapper_impl(name, arg_fmt, f, opt, slf, *args, **kwargs)
        return log_member_call_wrapper
    return decorator
