""" PrintDebug
    ...small module that helps with debug printing.
    -Christopher Welborn 08-21-2014
"""
from __future__ import print_function, with_statement

import inspect
import os.path
import sys


try:
    from colr import (
        auto_disable as colr_auto_disable,
        Colr as C,
    )
    colr_auto_disable()
except ImportError:
    C = None

__version__ = '0.3.0'

__all__ = [
    '__version__',
    'DebugColrPrinter',
    'DebugPrinter',
    'debug',
    'debug_enable',
    'default_format',
    'enabled',
    'get_frame',
    'get_lineinfo',
    'printobject',
    'LineInfo',
    'suppress',
]

default_format = '{filename}:{lineno:>5} {name:>25}(): '
if C is None:
    default_colr_format = None
else:
    default_colr_format = C('').join(
        C('{filename}:', fore='yellow'),
        C('{lineno:>5} ', fore='blue'),
        C('{name:>25}', fore='magenta'),
        C('(): '),
    )

# Module-level flag to disable debug() and DebugPrinter().debug().
# Better called through debug_enable(True/False)
_enabled = True


def debug_enable(enabled=True):
    """ Re-enable the debug function (if it was disabled).
        Disable it if enabled=False.
    """
    global _enabled
    _enabled = enabled


def enabled():
    """ Access to global _enabled value. """
    return _enabled


def _ensure_level(level=0):
    """ Ensure the level argument is a non-negative integer, defaulting to 0
        on errors.
    """
    try:
        l = abs(level)
    except TypeError:
        return 0
    return l


def get_frame(level=0):
    """ Gets a previous frame for inspecting or getting source code info from.
    """
    level = _ensure_level(level)

    frame = inspect.currentframe()
    # Go back some number of frames if needed.
    while level > -1:
        if frame is None:
            raise ValueError('`level` is too large, there is no frame.')
        frame = frame.f_back
        level -= 1
    if frame is None:
        raise ValueError('`level` is too large, there is no frame.')
    return frame


def get_lineinfo(level=0):
    """ Gets information about the current line.
        If level is given, we will go back some frames.
        This is because we usually want to know where thing() was called,
        not where get_lineinfo() was called.
    """
    # Account for get_lineinfo() itself.
    return LineInfo.from_frame(get_frame(level=level + 1))


def debug(*args, **kwargs):
    """ Wrapper for print() that adds file, line, and func info.
        Possibly raises a ValueError if the `level` argument is too large,
        and there is no frame at the desired level.

        Arguments:
            same as print()

        Keyword Arguments:
            same as print()
            ..also:
                align        : Omit the line info but use it's width as
                               indention.
                back         : Alias for `level`, will be deprecated soon.
                basename     : Whether to use just the base name of the file.
                               Default: False
                fmt          : .format() string for line info.
                               Default: printdebug.default_format
                level        : Number of frames to go back.
                               Default: 1
                ljustwidth   : str.ljust() value for line info.
                               Default: 40
                parent       : Parent class to include name for methods.
    """
    if not args:
        return None
    elif not _enabled:
        if debug.should_raise:
            raise DebugNotEnabled()
        return None

    # Use stderr by default.
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr

    # Include parent class name when given.
    parent = pop_or(kwargs, 'parent')

    # Go back more than once when given.
    backlevel = _ensure_level(pop_or(kwargs, 'level', 0))
    # Account for call to debug().
    backlevel += 1

    # Get format string.
    fmt = pop_or(kwargs, 'fmt', default_format)

    # Get ljust level.
    ljustwidth = pop_or(kwargs, 'ljustwidth', 40)

    # Are we omitting the line info, and just aligning with the end of it?
    align = pop_or(kwargs, 'align', False)

    info = get_lineinfo(level=backlevel)
    usebasename = pop_or(kwargs, 'basename', True)
    fname = os.path.split(info.filename)[-1] if usebasename else info.filename

    if parent:
        func = '{}.{}'.format(parent.__class__.__name__, info.name)
    else:
        func = info.name

    # Patch args to stay compatible with print().
    pargs = list(args)
    lineinfo = fmt.format(
        filename=fname,
        lineno=info.lineno,
        name=func).ljust(ljustwidth)

    # Is this a continuation from a previous line?
    # Getting this for debug(), re-setting for print().
    kwargs['end'] = kwargs.get('end', '\n')
    willcontinue = (not kwargs['end'].endswith('\n'))
    continued = debug.continued.get(kwargs['file'], False)
    if align or continued:
        debug.continued[kwargs['file']] = willcontinue
        if align:
            pargs[0] = ''.join((' ' * len(lineinfo), pargs[0]))
        print(*pargs, **kwargs)
        return None
    debug.continued[kwargs['file']] = willcontinue

    text = kwargs.get('sep', ' ').join((str(s) for s in pargs))
    line = ''.join((str(lineinfo), text))
    print(line, **kwargs)


# This dict keeps track of whether a line is "continued", based on the last
# `end` parameter, and it does so for each file descriptor used.
debug.continued = {sys.stderr: False}
# Whether debug() should raise DebugNotEnabled() when called while disabled.
debug.should_raise = False


def pop_or(dct, key, default=None):
    """ Like dict.get, except it pops the key afterwards. """
    val = default
    with suppress(KeyError):
        val = dct.pop(key)
    return val


def printobject(obj, file=None, indent=0):
    """ Print a verbose representation of an object.
        The format depends on what kind of object it is.
        Tuples, Lists, and Dicts are recursively formatted according to the
        other rules below.
        Strings will be printed as is.
        Any other type will be printed using str() (Actually '{}'.format(obj))
        Arguments:
            obj      : Object to print.
            file     : Open file object, defaults to sys.stdout.
            indent   : Internal use.
                       Can be used to set initial indention though.
                       Must be an integer. Default: 0
    """
    if file is None:
        file = sys.stdout

    if not hasattr(file, 'write'):
        errfmt = '`file` must have a `write` method. Got: {} ({!r})'
        raise TypeError(errfmt.format(type(file), file))

    if isinstance(obj, dict):
        try:
            objkeys = sorted(obj.keys())
        except TypeError:
            # Mixed key types.
            objkeys = obj.keys()

        for k in objkeys:
            v = obj[k]
            print('{}{}:'.format(' ' * indent, k), file=file)
            if isinstance(v, dict):
                printobject(v, file=file, indent=indent + 4)
            elif isinstance(v, (list, tuple)):
                printobject(v, file=file, indent=indent + 4)
            else:
                print('{}{}'.format(' ' * (indent + 4), v), file=file)
    elif isinstance(obj, (list, tuple)):
        try:
            objitems = sorted(obj)
        except TypeError:
            # Mixed list/tuple
            objitems = obj

        for itm in objitems:
            if isinstance(itm, (list, tuple)):
                printobject(itm, file=file, indent=indent + 4)
            else:
                print('{}{}'.format(' ' * indent, itm), file=file)
    else:
        print('{}{}'.format(' ' * indent, obj), file=file)


class DebugNotEnabled(ValueError):
    """ Used with DebugOnly, to signal that code should not run. """
    pass


class DebugPrinter(object):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """
    def __init__(
            self, fmt=None, ljustwidth=40, basename=True, file=None,
            should_raise=False):
        self.fmt = fmt or default_format
        self.ljustwidth = ljustwidth
        self.basename = basename
        # Use stderr by default.
        self.file = file or sys.stderr
        # Keeps track of line continuations, per file descriptor.
        self.continued = {self.file: False}
        # Whether this single instance is disabled.
        self._enabled = True
        # Whether this instance should raise DebugNotEnabled, when debug()
        # is called while disabled.
        self.should_raise = should_raise

    def debug(self, *args, **kwargs):
        """ Wrapper for print() that adds file, line, and func info. """
        if not args:
            return None
        elif not (self._enabled and _enabled):
            if self.should_raise:
                raise DebugNotEnabled()
            return None
        # Use stderr by default.
        if kwargs.get('file', None) is None:
            kwargs['file'] = self.file

        # Include parent class name when given.
        parent = kwargs.get('parent', None)

        # Go back more than once when given.
        backlevel = _ensure_level(kwargs.get('level', 0))
        # Account for call to debug().
        backlevel += 1
        info = get_lineinfo(level=backlevel)
        if self.basename:
            fname = os.path.split(info.filename)[-1]
        else:
            fname = info.filename

        if parent:
            func = '{}.{}'.format(parent.__class__.__name__, info.name)
        else:
            func = info.name

        # Patch args to stay compatible with print().
        pargs = list(args)
        lineinfo = self.fmt.format(
            filename=fname,
            lineno=info.lineno,
            name=func).ljust(self.ljustwidth)
        text = str(self.transform_text(
            kwargs.get('sep', ' ').join((str(s) for s in pargs))
        ))

        align = pop_or(kwargs, 'align', False)
        # Is this a continuation from a previous line?
        # Getting this for debug(), re-setting for print().
        kwargs['end'] = kwargs.get('end', '\n')
        willcontinue = (not kwargs['end'].endswith('\n'))
        continued = self.continued.get(kwargs['file'], False)
        if align or continued:
            self.continued[kwargs['file']] = willcontinue
            if align:
                text = ''.join((' ' * self.lineinfo_len(lineinfo), text))
            print(text, **kwargs)
            return None
        self.continued[kwargs['file']] = willcontinue

        # lineinfo may be a Colr instance.
        line = ''.join((str(lineinfo), text))

        # Pop all kwargs for this function. Send the rest to print().
        with suppress(KeyError):
            kwargs.pop('back')
        with suppress(KeyError):
            kwargs.pop('level')
        with suppress(KeyError):
            kwargs.pop('parent')

        print(line, **kwargs)

    def disable(self, disabled=True):
        """ Disable this instance. """
        self._enabled = not disabled

    @property
    def disabled(self):
        """ Dynamic property to query this debug printer's enabled/disabled
            value.
        """
        return not self._enabled

    @disabled.setter
    def disabled(self, value):
        self._enabled = not bool(value)

    def enable(self, enabled=True):
        """ Re-enable this instance, if it was disabled. """
        self._enabled = enabled

    @property
    def enabled(self):
        """ Dynamic property to query this debug printer's enabled/disabled
            value.
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = bool(value)

    def lineinfo_len(self, s):
        """ Overridable, returns the length of line info.
            This is needed in subclasses because of escape codes.
        """
        return len(s)

    def transform_text(self, text):
        """ Run a transformation on the actual text before printing. """
        # This is meaningless for DebugPrinter, and a little bit of a hack
        # to make DebugColrPrinter work without reimplementing debug().
        return str(text)


class DebugColrPrinter(DebugPrinter):
    """ A debug printer that remembers it's config on initilization,
        and uses it until changed.
    """
    textcolor = 'green'

    def __init__(
            self, fmt=None, ljustwidth=40, basename=True, file=None,
            should_raise=False):
        if default_colr_format is None:
            # Raise an error on instantiation if colr is not available.
            # At least the Python 2 users can use the regular debug prints.
            if sys.version_info.major < 3:
                errmsg = '\n'.join((
                    'Color is not available in Python 2.',
                    'The colr module is required, but depends on Python 3+.'
                ))
            else:
                errmsg = '\n'.join((
                    'The colr module is required for DebugColrPrinter.',
                    '`colr` is not installed, you can install it with pip.',
                ))
            imperr = ImportError(errmsg)
            imperr.name = 'colr'
            raise imperr

        super(DebugColrPrinter, self).__init__(
            fmt=fmt or default_colr_format,
            ljustwidth=ljustwidth,
            basename=basename,
            file=file,
            should_raise=should_raise,
        )

    def lineinfo_len(self, s):
        """ Return a line length, without escape codes. """
        if hasattr(s, 'stripped'):
            return len(s.stripped())
        return len(s)

    def transform_text(self, text):
        """ Transform all debug text, colorizing it. """
        return C(text, fore=self.textcolor)


class LineInfo(object):
    """ Holds information about where the debug print came from. """
    def __init__(self, filename, name, lineno):
        self.filename = filename
        self.name = name
        self.lineno = lineno

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(k, getattr(self, k))
                for k in ('filename', 'lineno', 'name')
            )
        )

    def __str__(self):
        return default_format.format(
            filename=self.filename,
            name=self.name,
            lineno=self.lineno
        )

    @classmethod
    def from_frame(cls, frame):
        """ Construct a LineInfo from a frame, retrieved with `inspect`. """
        return cls(
            frame.f_code.co_filename,
            frame.f_code.co_name,
            frame.f_lineno
        )

    @classmethod
    def from_level(cls, level=0):
        level = _ensure_level(level)
        # Account for call to from_level.
        level += 1
        return cls.from_frame(get_frame(level=level))


class suppress:
    """Context manager to suppress specified exceptions

    * Borrowed from contextlib.py to use with py2.

    After the exception is suppressed, execution proceeds with the next
    statement following the with statement.

         with suppress(FileNotFoundError):
             os.remove(somefile)
         # Execution still resumes here if the file was already removed
    """

    def __init__(self, *exceptions):
        self._exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        # See http://bugs.python.org/issue12029 for more details
        return (
            exctype is not None and issubclass(exctype, self._exceptions)
        )
