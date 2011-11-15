'''Wrapper for bitlist.h

Generated with:
c:/Python27/Scripts/ctypesgen.py -lspiceparser bitlist.h debug.h eqn.h equations.h eval.h hash.h list.h list_search.h memory.h mergedup.h names.h netlist.h netlist_dev.h netlist_extract.h netlist_lib.h netlist_spice.h scanner.h -o spiceparser.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, basestring):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return long(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, basestring):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, basestring):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxint):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxint):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxint):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxint):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxint):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxint):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxint):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, basestring):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, basestring):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, unicode, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            return String.from_param(obj._as_parameter_)
    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError,e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname

        else:
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["spiceparser"] = load_library("spiceparser")

# 1 libraries
# End libraries

# No modules

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 35
class struct_bitlist_st(Structure):
    pass

struct_bitlist_st.__slots__ = [
    'qty',
    'qbytes',
    'data',
]
struct_bitlist_st._fields_ = [
    ('qty', c_int),
    ('qbytes', c_int),
    ('data', c_ubyte * 4),
]

bitlist_t = struct_bitlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 35

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 42
if hasattr(_libs['spiceparser'], 'bitlist_new'):
    bitlist_new = _libs['spiceparser'].bitlist_new
    bitlist_new.argtypes = [c_int]
    bitlist_new.restype = POINTER(bitlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 43
if hasattr(_libs['spiceparser'], 'bitlist_free'):
    bitlist_free = _libs['spiceparser'].bitlist_free
    bitlist_free.argtypes = [POINTER(bitlist_t)]
    bitlist_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 44
if hasattr(_libs['spiceparser'], 'bitlist_set'):
    bitlist_set = _libs['spiceparser'].bitlist_set
    bitlist_set.argtypes = [POINTER(bitlist_t), c_int]
    bitlist_set.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 45
if hasattr(_libs['spiceparser'], 'bitlist_test'):
    bitlist_test = _libs['spiceparser'].bitlist_test
    bitlist_test.argtypes = [POINTER(bitlist_t), c_int]
    bitlist_test.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 46
if hasattr(_libs['spiceparser'], 'bitlist_clear'):
    bitlist_clear = _libs['spiceparser'].bitlist_clear
    bitlist_clear.argtypes = [POINTER(bitlist_t), c_int]
    bitlist_clear.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 47
if hasattr(_libs['spiceparser'], 'bitlist_resize'):
    bitlist_resize = _libs['spiceparser'].bitlist_resize
    bitlist_resize.argtypes = [POINTER(bitlist_t), c_int]
    bitlist_resize.restype = POINTER(bitlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 48
if hasattr(_libs['spiceparser'], 'bitlist_scan'):
    bitlist_scan = _libs['spiceparser'].bitlist_scan
    bitlist_scan.argtypes = [POINTER(bitlist_t), c_int]
    bitlist_scan.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 49
if hasattr(_libs['spiceparser'], 'bitlist_copyhead'):
    bitlist_copyhead = _libs['spiceparser'].bitlist_copyhead
    bitlist_copyhead.argtypes = [POINTER(bitlist_t), POINTER(bitlist_t), c_int]
    bitlist_copyhead.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 50
if hasattr(_libs['spiceparser'], 'bitlist_clearall'):
    bitlist_clearall = _libs['spiceparser'].bitlist_clearall
    bitlist_clearall.argtypes = [POINTER(bitlist_t)]
    bitlist_clearall.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 51
if hasattr(_libs['spiceparser'], 'bitlist_setall'):
    bitlist_setall = _libs['spiceparser'].bitlist_setall
    bitlist_setall.argtypes = [POINTER(bitlist_t)]
    bitlist_setall.restype = None

# c:\\mingw\\bin\\../lib/gcc/mingw32/4.5.2/../../../../include/stdlib.h: 364
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'malloc'):
        continue
    malloc = _lib.malloc
    malloc.argtypes = [c_size_t]
    malloc.restype = POINTER(None)
    break

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\debug.h: 43
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'cmdline_read_rc'):
        continue
    cmdline_read_rc = _lib.cmdline_read_rc
    cmdline_read_rc.argtypes = [POINTER(c_int), POINTER(POINTER(POINTER(c_char))), String]
    cmdline_read_rc.restype = POINTER(None)
    break

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\debug.h: 44
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'cmdline_free_rc'):
        continue
    cmdline_free_rc = _lib.cmdline_free_rc
    cmdline_free_rc.argtypes = [POINTER(None)]
    cmdline_free_rc.restype = None
    break

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 40
class struct_list_st(Structure):
    pass

struct_list_st.__slots__ = [
    'q',
    's',
    'm',
    'mode',
    'd',
]
struct_list_st._fields_ = [
    ('q', c_int),
    ('s', c_int),
    ('m', c_int),
    ('mode', c_int),
    ('d', POINTER(None)),
]

list_t = struct_list_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 40

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 47
class struct_listx_st(Structure):
    pass

struct_listx_st.__slots__ = [
    'list',
    'bitmap',
]
struct_listx_st._fields_ = [
    ('list', list_t),
    ('bitmap', POINTER(bitlist_t)),
]

listx_t = struct_listx_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 47

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 72
if hasattr(_libs['spiceparser'], 'listx_init'):
    listx_init = _libs['spiceparser'].listx_init
    listx_init.argtypes = [POINTER(listx_t), c_int, c_int]
    listx_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 73
if hasattr(_libs['spiceparser'], 'listx_qty'):
    listx_qty = _libs['spiceparser'].listx_qty
    listx_qty.argtypes = [POINTER(listx_t)]
    listx_qty.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 74
if hasattr(_libs['spiceparser'], 'listx_data'):
    listx_data = _libs['spiceparser'].listx_data
    listx_data.argtypes = [POINTER(listx_t), c_int]
    listx_data.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 75
if hasattr(_libs['spiceparser'], 'listx_empty'):
    listx_empty = _libs['spiceparser'].listx_empty
    listx_empty.argtypes = [POINTER(listx_t)]
    listx_empty.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 76
if hasattr(_libs['spiceparser'], 'listx_free'):
    listx_free = _libs['spiceparser'].listx_free
    listx_free.argtypes = [POINTER(listx_t), c_int]
    listx_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 77
if hasattr(_libs['spiceparser'], 'listx_alloc'):
    listx_alloc = _libs['spiceparser'].listx_alloc
    listx_alloc.argtypes = [POINTER(listx_t)]
    listx_alloc.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 78
if hasattr(_libs['spiceparser'], 'listx_vdata'):
    listx_vdata = _libs['spiceparser'].listx_vdata
    listx_vdata.argtypes = [POINTER(listx_t), c_int]
    listx_vdata.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 101
if hasattr(_libs['spiceparser'], 'list_element_dup'):
    list_element_dup = _libs['spiceparser'].list_element_dup
    list_element_dup.argtypes = [POINTER(list_t), c_int, c_int]
    list_element_dup.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 102
if hasattr(_libs['spiceparser'], 'list_remove'):
    list_remove = _libs['spiceparser'].list_remove
    list_remove.argtypes = [POINTER(list_t), c_int, POINTER(None)]
    list_remove.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 103
if hasattr(_libs['spiceparser'], 'list_empty'):
    list_empty = _libs['spiceparser'].list_empty
    list_empty.argtypes = [POINTER(list_t)]
    list_empty.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 104
if hasattr(_libs['spiceparser'], 'list_init'):
    list_init = _libs['spiceparser'].list_init
    list_init.argtypes = [POINTER(list_t), c_int, c_int]
    list_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 105
if hasattr(_libs['spiceparser'], 'list_hint'):
    list_hint = _libs['spiceparser'].list_hint
    list_hint.argtypes = [POINTER(list_t), c_int]
    list_hint.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 106
if hasattr(_libs['spiceparser'], 'list_next'):
    list_next = _libs['spiceparser'].list_next
    list_next.argtypes = [POINTER(list_t)]
    list_next.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 107
if hasattr(_libs['spiceparser'], 'list_prev'):
    list_prev = _libs['spiceparser'].list_prev
    list_prev.argtypes = [POINTER(list_t)]
    list_prev.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 108
if hasattr(_libs['spiceparser'], 'list_block_next'):
    list_block_next = _libs['spiceparser'].list_block_next
    list_block_next.argtypes = [POINTER(list_t), c_int]
    list_block_next.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 109
if hasattr(_libs['spiceparser'], 'list_data_func'):
    list_data_func = _libs['spiceparser'].list_data_func
    list_data_func.argtypes = [POINTER(list_t), c_int]
    list_data_func.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 110
if hasattr(_libs['spiceparser'], 'list_contains'):
    list_contains = _libs['spiceparser'].list_contains
    list_contains.argtypes = [POINTER(list_t), POINTER(None)]
    list_contains.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 111
if hasattr(_libs['spiceparser'], 'list_add'):
    list_add = _libs['spiceparser'].list_add
    list_add.argtypes = [POINTER(list_t), POINTER(None)]
    list_add.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 112
if hasattr(_libs['spiceparser'], 'list_index'):
    list_index = _libs['spiceparser'].list_index
    list_index.argtypes = [POINTER(list_t), POINTER(None)]
    list_index.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 113
if hasattr(_libs['spiceparser'], 'list_sort'):
    list_sort = _libs['spiceparser'].list_sort
    list_sort.argtypes = [POINTER(list_t), CFUNCTYPE(UNCHECKED(c_int), POINTER(None), POINTER(None))]
    list_sort.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 114
if hasattr(_libs['spiceparser'], 'list_start'):
    list_start = _libs['spiceparser'].list_start
    list_start.argtypes = [POINTER(list_t)]
    list_start.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 115
if hasattr(_libs['spiceparser'], 'list_copyfrom'):
    list_copyfrom = _libs['spiceparser'].list_copyfrom
    list_copyfrom.argtypes = [POINTER(list_t), POINTER(list_t)]
    list_copyfrom.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 116
if hasattr(_libs['spiceparser'], 'list_shrink'):
    list_shrink = _libs['spiceparser'].list_shrink
    list_shrink.argtypes = [POINTER(list_t)]
    list_shrink.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 117
if hasattr(_libs['spiceparser'], 'list_nextz'):
    list_nextz = _libs['spiceparser'].list_nextz
    list_nextz.argtypes = [POINTER(list_t)]
    list_nextz.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 118
if hasattr(_libs['spiceparser'], 'list_dup'):
    list_dup = _libs['spiceparser'].list_dup
    list_dup.argtypes = [POINTER(list_t), POINTER(list_t)]
    list_dup.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 119
if hasattr(_libs['spiceparser'], 'list_reset'):
    list_reset = _libs['spiceparser'].list_reset
    list_reset.argtypes = [POINTER(list_t)]
    list_reset.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 120
if hasattr(_libs['spiceparser'], 'list_append'):
    list_append = _libs['spiceparser'].list_append
    list_append.argtypes = [POINTER(list_t), POINTER(list_t)]
    list_append.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 121
if hasattr(_libs['spiceparser'], 'list_stdlib_bsearch'):
    list_stdlib_bsearch = _libs['spiceparser'].list_stdlib_bsearch
    list_stdlib_bsearch.argtypes = [POINTER(list_t), POINTER(None), CFUNCTYPE(UNCHECKED(c_int), POINTER(None), POINTER(None))]
    list_stdlib_bsearch.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 123
class struct_sort_func_st(Structure):
    pass

struct_sort_func_st.__slots__ = [
    'tosort',
    'cmpf',
    'aiskey',
    'user',
]
struct_sort_func_st._fields_ = [
    ('tosort', POINTER(list_t)),
    ('cmpf', CFUNCTYPE(UNCHECKED(c_int), POINTER(struct_sort_func_st), POINTER(None), POINTER(None))),
    ('aiskey', c_int),
    ('user', POINTER(None)),
]

sort_func_t = struct_sort_func_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 129

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 131
if hasattr(_libs['spiceparser'], 'list_bsearch'):
    list_bsearch = _libs['spiceparser'].list_bsearch
    list_bsearch.argtypes = [POINTER(sort_func_t), POINTER(None)]
    list_bsearch.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 134
if hasattr(_libs['spiceparser'], 'list_qsort'):
    list_qsort = _libs['spiceparser'].list_qsort
    list_qsort.argtypes = [POINTER(sort_func_t)]
    list_qsort.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 50
class struct_names_st(Structure):
    pass

names_t = struct_names_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 51

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 54
if hasattr(_libs['spiceparser'], 'names_stats'):
    names_stats = _libs['spiceparser'].names_stats
    names_stats.argtypes = [POINTER(names_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        names_stats.restype = ReturnString
    else:
        names_stats.restype = String
        names_stats.errcheck = ReturnString

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 55
if hasattr(_libs['spiceparser'], 'names_lookup'):
    names_lookup = _libs['spiceparser'].names_lookup
    names_lookup.argtypes = [POINTER(names_t), c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        names_lookup.restype = ReturnString
    else:
        names_lookup.restype = String
        names_lookup.errcheck = ReturnString

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 56
if hasattr(_libs['spiceparser'], 'names_check'):
    names_check = _libs['spiceparser'].names_check
    names_check.argtypes = [POINTER(names_t), String]
    names_check.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 57
if hasattr(_libs['spiceparser'], 'names_add'):
    names_add = _libs['spiceparser'].names_add
    names_add.argtypes = [POINTER(names_t), c_int, String]
    names_add.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 58
if hasattr(_libs['spiceparser'], 'names_new'):
    names_new = _libs['spiceparser'].names_new
    names_new.argtypes = []
    names_new.restype = POINTER(names_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 59
if hasattr(_libs['spiceparser'], 'names_free'):
    names_free = _libs['spiceparser'].names_free
    names_free.argtypes = [POINTER(names_t)]
    names_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 60
if hasattr(_libs['spiceparser'], 'names_rehash'):
    names_rehash = _libs['spiceparser'].names_rehash
    names_rehash.argtypes = [POINTER(names_t), c_int]
    names_rehash.restype = None

uchar = c_ubyte # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 30

uint = c_uint # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 36

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 43
class struct_hashbin_st(Structure):
    pass

struct_hashbin_st.__slots__ = [
    'next',
    'size',
]
struct_hashbin_st._fields_ = [
    ('next', POINTER(struct_hashbin_st)),
    ('size', c_int),
]

hashbin_t = struct_hashbin_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 48

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 59
class struct_hash_st(Structure):
    pass

struct_hash_st.__slots__ = [
    'uniq',
    'hashfunc',
    'hashcmp',
    'qbin',
    'bins',
    'qalloc',
    'alloc',
]
struct_hash_st._fields_ = [
    ('uniq', c_int),
    ('hashfunc', CFUNCTYPE(UNCHECKED(uint), c_int, POINTER(None), c_int)),
    ('hashcmp', CFUNCTYPE(UNCHECKED(c_int), c_int, POINTER(None), c_int, POINTER(None))),
    ('qbin', c_int),
    ('bins', POINTER(POINTER(hashbin_t))),
    ('qalloc', c_int),
    ('alloc', POINTER(POINTER(None))),
]

hash_t = struct_hash_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 59

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 67
if hasattr(_libs['spiceparser'], 'hash_new'):
    hash_new = _libs['spiceparser'].hash_new
    hash_new.argtypes = [c_int, CFUNCTYPE(UNCHECKED(uint), c_int, POINTER(None), c_int), CFUNCTYPE(UNCHECKED(c_int), c_int, POINTER(None), c_int, POINTER(None))]
    hash_new.restype = POINTER(hash_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 73
if hasattr(_libs['spiceparser'], 'hash_free'):
    hash_free = _libs['spiceparser'].hash_free
    hash_free.argtypes = [POINTER(hash_t)]
    hash_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 74
if hasattr(_libs['spiceparser'], 'hash_find'):
    hash_find = _libs['spiceparser'].hash_find
    hash_find.argtypes = [POINTER(hash_t), POINTER(None), c_int]
    hash_find.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 75
if hasattr(_libs['spiceparser'], 'hash_add'):
    hash_add = _libs['spiceparser'].hash_add
    hash_add.argtypes = [POINTER(hash_t), POINTER(None), c_int]
    hash_add.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 76
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'hash_alloc'):
        continue
    hash_alloc = _lib.hash_alloc
    hash_alloc.argtypes = [POINTER(hash_t), POINTER(None)]
    hash_alloc.restype = POINTER(None)
    break

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 77
if hasattr(_libs['spiceparser'], 'hash_size'):
    hash_size = _libs['spiceparser'].hash_size
    hash_size.argtypes = [POINTER(None)]
    hash_size.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 81
if hasattr(_libs['spiceparser'], 'hash_strhash'):
    hash_strhash = _libs['spiceparser'].hash_strhash
    hash_strhash.argtypes = [c_int, POINTER(None), c_int]
    hash_strhash.restype = c_uint

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 82
if hasattr(_libs['spiceparser'], 'hash_binhash'):
    hash_binhash = _libs['spiceparser'].hash_binhash
    hash_binhash.argtypes = [c_int, POINTER(None), c_int]
    hash_binhash.restype = c_uint

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 94
class struct_hash_ptrflagstr_st(Structure):
    pass

struct_hash_ptrflagstr_st.__slots__ = [
    'ptr',
    'flag',
]
struct_hash_ptrflagstr_st._fields_ = [
    ('ptr', POINTER(None)),
    ('flag', c_char),
]

hclient_ptrflagstr_t = struct_hash_ptrflagstr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 94

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 96
if hasattr(_libs['spiceparser'], 'hclient_ptrflagstr_hash'):
    hclient_ptrflagstr_hash = _libs['spiceparser'].hclient_ptrflagstr_hash
    hclient_ptrflagstr_hash.argtypes = [c_int, POINTER(None), c_int]
    hclient_ptrflagstr_hash.restype = uint

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 104
if hasattr(_libs['spiceparser'], 'hclient_bobject_hash'):
    hclient_bobject_hash = _libs['spiceparser'].hclient_bobject_hash
    hclient_bobject_hash.argtypes = [c_int, POINTER(None), c_int]
    hclient_bobject_hash.restype = uint

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 105
if hasattr(_libs['spiceparser'], 'hclient_bobject_cmp'):
    hclient_bobject_cmp = _libs['spiceparser'].hclient_bobject_cmp
    hclient_bobject_cmp.argtypes = [c_int, POINTER(None), c_int, POINTER(None)]
    hclient_bobject_cmp.restype = c_int

enum_itemop_e = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPeolist = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPeol_const = (OPeolist + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPeol_valp = (OPeol_const + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPeol_qty = (OPeol_valp + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPlit = (OPeol_qty + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPlitm = (OPlit + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPlitv = (OPlitm + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPlitvm = (OPlitv + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPval = (OPlitvm + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPvalm = (OPval + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPadd = (OPvalm + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPsub = (OPadd + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPmul = (OPsub + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPdiv = (OPmul + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPexp = (OPdiv + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPopen = (OPexp + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

OPclose = (OPopen + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

itemop_t = enum_itemop_e # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 75

eqn_litref_t = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 105

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 113
class struct_eqntokenlit_st(Structure):
    pass

struct_eqntokenlit_st.__slots__ = [
    'lit',
    'ref',
    'cache',
]
struct_eqntokenlit_st._fields_ = [
    ('lit', String),
    ('ref', eqn_litref_t),
    ('cache', c_float),
]

eqntokenlit_t = struct_eqntokenlit_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 113

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 119
class struct_eqntokenval_st(Structure):
    pass

struct_eqntokenval_st.__slots__ = [
    'x',
]
struct_eqntokenval_st._fields_ = [
    ('x', c_float),
]

eqntokenval_t = struct_eqntokenval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 119

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 124
class struct_eqntokenpval_st(Structure):
    pass

struct_eqntokenpval_st.__slots__ = [
    'xp',
]
struct_eqntokenpval_st._fields_ = [
    ('xp', POINTER(c_float)),
]

eqntokenpval_t = struct_eqntokenpval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 124

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 129
class union_lit_val_un(Union):
    pass

union_lit_val_un.__slots__ = [
    'lit',
    'val',
    'pval',
]
union_lit_val_un._fields_ = [
    ('lit', eqntokenlit_t),
    ('val', eqntokenval_t),
    ('pval', eqntokenpval_t),
]

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 135
class struct_eqntoken_st(Structure):
    pass

struct_eqntoken_st.__slots__ = [
    'op',
    'z',
]
struct_eqntoken_st._fields_ = [
    ('op', itemop_t),
    ('z', union_lit_val_un),
]

eqntoken_t = struct_eqntoken_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 135

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 151
class struct_eqntop_st(Structure):
    pass

struct_eqntop_st.__slots__ = [
    'str',
    'last',
    'nodes',
    'nodep',
    'litc',
    'opc',
]
struct_eqntop_st._fields_ = [
    ('str', String),
    ('last', c_char),
    ('nodes', eqntoken_t * 512),
    ('nodep', c_int),
    ('litc', c_int),
    ('opc', c_int),
]

eqntop_t = struct_eqntop_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 151

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 155
class struct_plookup_st(Structure):
    pass

struct_plookup_st.__slots__ = [
    'lookup',
    'user',
]
struct_plookup_st._fields_ = [
    ('lookup', CFUNCTYPE(UNCHECKED(eqn_litref_t), POINTER(struct_plookup_st), String)),
    ('user', POINTER(None)),
]

plookup_t = struct_plookup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 159

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 168
class struct_eqneval_st(Structure):
    pass

struct_eqneval_st.__slots__ = [
    'stack',
    'stackp',
    'list',
]
struct_eqneval_st._fields_ = [
    ('stack', c_float * 512),
    ('stackp', c_int),
    ('list', POINTER(eqntoken_t)),
]

eqneval_t = struct_eqneval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 168

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 178
class struct_eqn_st(Structure):
    pass

struct_eqn_st.__slots__ = [
    'eqn',
]
struct_eqn_st._fields_ = [
    ('eqn', POINTER(eqntoken_t)),
]

eqn_t = struct_eqn_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 178

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 182
if hasattr(_libs['spiceparser'], 'eqn_const'):
    eqn_const = _libs['spiceparser'].eqn_const
    eqn_const.argtypes = [c_float]
    eqn_const.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 183
if hasattr(_libs['spiceparser'], 'debug_eqn'):
    debug_eqn = _libs['spiceparser'].debug_eqn
    debug_eqn.argtypes = [POINTER(None), String, POINTER(eqn_t)]
    debug_eqn.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 184
if hasattr(_libs['spiceparser'], 'eqn_undefined'):
    eqn_undefined = _libs['spiceparser'].eqn_undefined
    eqn_undefined.argtypes = []
    eqn_undefined.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 185
if hasattr(_libs['spiceparser'], 'eqn_valp'):
    eqn_valp = _libs['spiceparser'].eqn_valp
    eqn_valp.argtypes = [POINTER(c_float)]
    eqn_valp.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 186
if hasattr(_libs['spiceparser'], 'eqn_setvalp'):
    eqn_setvalp = _libs['spiceparser'].eqn_setvalp
    eqn_setvalp.argtypes = [POINTER(eqn_t), POINTER(c_float)]
    eqn_setvalp.restype = c_float

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 187
if hasattr(_libs['spiceparser'], 'eqn_is_undefined'):
    eqn_is_undefined = _libs['spiceparser'].eqn_is_undefined
    eqn_is_undefined.argtypes = [eqn_t]
    eqn_is_undefined.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 189
if hasattr(_libs['spiceparser'], 'eqntok_parse'):
    eqntok_parse = _libs['spiceparser'].eqntok_parse
    eqntok_parse.argtypes = [String]
    eqntok_parse.restype = POINTER(eqntoken_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 191
if hasattr(_libs['spiceparser'], 'eqntoken_next'):
    eqntoken_next = _libs['spiceparser'].eqntoken_next
    eqntoken_next.argtypes = [POINTER(eqntoken_t)]
    eqntoken_next.restype = POINTER(eqntoken_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 192
if hasattr(_libs['spiceparser'], 'eqntok_depend'):
    eqntok_depend = _libs['spiceparser'].eqntok_depend
    eqntok_depend.argtypes = [POINTER(eqntoken_t), POINTER(plookup_t)]
    eqntok_depend.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 193
if hasattr(_libs['spiceparser'], 'eqntok_eval'):
    eqntok_eval = _libs['spiceparser'].eqntok_eval
    eqntok_eval.argtypes = [POINTER(c_float), POINTER(eqntoken_t)]
    eqntok_eval.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 194
if hasattr(_libs['spiceparser'], 'parse_float'):
    parse_float = _libs['spiceparser'].parse_float
    parse_float.argtypes = [POINTER(c_ubyte)]
    parse_float.restype = c_float

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 195
if hasattr(_libs['spiceparser'], 'eqntok_copy'):
    eqntok_copy = _libs['spiceparser'].eqntok_copy
    eqntok_copy.argtypes = [POINTER(eqntoken_t)]
    eqntok_copy.restype = POINTER(eqntoken_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 196
if hasattr(_libs['spiceparser'], 'eqn_setval'):
    eqn_setval = _libs['spiceparser'].eqn_setval
    eqn_setval.argtypes = [POINTER(eqn_t), c_float]
    eqn_setval.restype = c_float

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 197
if hasattr(_libs['spiceparser'], 'eqn_getval_'):
    eqn_getval_ = _libs['spiceparser'].eqn_getval_
    eqn_getval_.argtypes = [POINTER(eqn_t)]
    eqn_getval_.restype = c_float

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 199
if hasattr(_libs['spiceparser'], 'eqn_copy'):
    eqn_copy = _libs['spiceparser'].eqn_copy
    eqn_copy.argtypes = [eqn_t]
    eqn_copy.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 200
if hasattr(_libs['spiceparser'], 'eqn_copy_m'):
    eqn_copy_m = _libs['spiceparser'].eqn_copy_m
    eqn_copy_m.argtypes = [eqn_t, c_float]
    eqn_copy_m.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 201
if hasattr(_libs['spiceparser'], 'eqn_empty'):
    eqn_empty = _libs['spiceparser'].eqn_empty
    eqn_empty.argtypes = []
    eqn_empty.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 202
if hasattr(_libs['spiceparser'], 'eqn_parse'):
    eqn_parse = _libs['spiceparser'].eqn_parse
    eqn_parse.argtypes = [POINTER(c_ubyte)]
    eqn_parse.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 204
if hasattr(_libs['spiceparser'], 'eqn_mem_new'):
    eqn_mem_new = _libs['spiceparser'].eqn_mem_new
    eqn_mem_new.argtypes = []
    eqn_mem_new.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 205
if hasattr(_libs['spiceparser'], 'eqn_mem_push'):
    eqn_mem_push = _libs['spiceparser'].eqn_mem_push
    eqn_mem_push.argtypes = [POINTER(None)]
    eqn_mem_push.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 206
if hasattr(_libs['spiceparser'], 'eqn_mem_pop'):
    eqn_mem_pop = _libs['spiceparser'].eqn_mem_pop
    eqn_mem_pop.argtypes = []
    eqn_mem_pop.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 207
if hasattr(_libs['spiceparser'], 'eqn_mem_free'):
    eqn_mem_free = _libs['spiceparser'].eqn_mem_free
    eqn_mem_free.argtypes = [POINTER(None)]
    eqn_mem_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 218
class struct_eqnlist_st(Structure):
    pass

struct_eqnlist_st.__slots__ = [
    'params',
    'eqnlist',
    'cache',
]
struct_eqnlist_st._fields_ = [
    ('params', POINTER(names_t)),
    ('eqnlist', list_t),
    ('cache', list_t),
]

eqnlist_t = struct_eqnlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 218

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 220
if hasattr(_libs['spiceparser'], 'eqnl_depend'):
    eqnl_depend = _libs['spiceparser'].eqnl_depend
    eqnl_depend.argtypes = [POINTER(eqnlist_t), eqn_t]
    eqnl_depend.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 221
if hasattr(_libs['spiceparser'], 'eqnl_free'):
    eqnl_free = _libs['spiceparser'].eqnl_free
    eqnl_free.argtypes = [POINTER(eqnlist_t)]
    eqnl_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 222
if hasattr(_libs['spiceparser'], 'eqnl_init'):
    eqnl_init = _libs['spiceparser'].eqnl_init
    eqnl_init.argtypes = [POINTER(eqnlist_t)]
    eqnl_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 223
if hasattr(_libs['spiceparser'], 'eqnl_evaldep'):
    eqnl_evaldep = _libs['spiceparser'].eqnl_evaldep
    eqnl_evaldep.argtypes = [POINTER(eqnlist_t)]
    eqnl_evaldep.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 224
if hasattr(_libs['spiceparser'], 'eqnl_eval'):
    eqnl_eval = _libs['spiceparser'].eqnl_eval
    eqnl_eval.argtypes = [POINTER(eqnlist_t), eqn_t]
    eqnl_eval.restype = c_float

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 225
if hasattr(_libs['spiceparser'], 'eqnl_add'):
    eqnl_add = _libs['spiceparser'].eqnl_add
    eqnl_add.argtypes = [POINTER(eqnlist_t), eqn_t, String]
    eqnl_add.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 226
if hasattr(_libs['spiceparser'], 'eqnl_eqn'):
    eqnl_eqn = _libs['spiceparser'].eqnl_eqn
    eqnl_eqn.argtypes = [POINTER(eqnlist_t), c_int]
    eqnl_eqn.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 227
if hasattr(_libs['spiceparser'], 'eqnl_find'):
    eqnl_find = _libs['spiceparser'].eqnl_find
    eqnl_find.argtypes = [POINTER(eqnlist_t), String]
    eqnl_find.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 228
if hasattr(_libs['spiceparser'], 'eqnl_define'):
    eqnl_define = _libs['spiceparser'].eqnl_define
    eqnl_define.argtypes = [POINTER(eqnlist_t), c_int, POINTER(c_float)]
    eqnl_define.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 229
if hasattr(_libs['spiceparser'], 'eqnl_is_undefined'):
    eqnl_is_undefined = _libs['spiceparser'].eqnl_is_undefined
    eqnl_is_undefined.argtypes = [POINTER(eqnlist_t), c_int]
    eqnl_is_undefined.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 230
if hasattr(_libs['spiceparser'], 'eqnl_qty'):
    eqnl_qty = _libs['spiceparser'].eqnl_qty
    eqnl_qty.argtypes = [POINTER(eqnlist_t)]
    eqnl_qty.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 231
if hasattr(_libs['spiceparser'], 'eqnl_lookup'):
    eqnl_lookup = _libs['spiceparser'].eqnl_lookup
    eqnl_lookup.argtypes = [POINTER(eqnlist_t), c_int]
    if sizeof(c_int) == sizeof(c_void_p):
        eqnl_lookup.restype = ReturnString
    else:
        eqnl_lookup.restype = String
        eqnl_lookup.errcheck = ReturnString

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 232
if hasattr(_libs['spiceparser'], 'eqnl_autodepend'):
    eqnl_autodepend = _libs['spiceparser'].eqnl_autodepend
    eqnl_autodepend.argtypes = [POINTER(eqnlist_t)]
    eqnl_autodepend.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 167
class struct_eqndef_st(Structure):
    pass

struct_eqndef_st.__slots__ = [
    'name',
    'eqn',
]
struct_eqndef_st._fields_ = [
    ('name', String),
    ('eqn', eqn_t),
]

eqndef_t = struct_eqndef_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 167

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 171
if hasattr(_libs['spiceparser'], 'equation_parse'):
    equation_parse = _libs['spiceparser'].equation_parse
    equation_parse.argtypes = [POINTER(uchar)]
    equation_parse.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 172
if hasattr(_libs['spiceparser'], 'equation_depend'):
    equation_depend = _libs['spiceparser'].equation_depend
    equation_depend.argtypes = [eqn_t, CFUNCTYPE(UNCHECKED(POINTER(c_float)), POINTER(None), String), POINTER(None)]
    equation_depend.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 173
if hasattr(_libs['spiceparser'], 'equation_eval'):
    equation_eval = _libs['spiceparser'].equation_eval
    equation_eval.argtypes = [POINTER(eqn_t)]
    equation_eval.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 174
if hasattr(_libs['spiceparser'], 'equation_empty'):
    equation_empty = _libs['spiceparser'].equation_empty
    equation_empty.argtypes = [eqn_t]
    equation_empty.restype = eqn_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 175
if hasattr(_libs['spiceparser'], 'equation_debug'):
    equation_debug = _libs['spiceparser'].equation_debug
    equation_debug.argtypes = [eqn_t, POINTER(None)]
    equation_debug.restype = None

enum_eval_op_en = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOnone = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOadd = (EOnone + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOsub = (EOadd + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOneg = (EOsub + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOmul = (EOneg + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOdiv = (EOmul + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOmod = (EOdiv + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOleft = (EOmod + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOright = (EOleft + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EObitxor = (EOright + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EObitand = (EObitxor + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EObitor = (EObitand + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EObitnot = (EObitor + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOor = (EObitnot + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOand = (EOor + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOnot = (EOand + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOlist = (EOnot + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOliteral = (EOlist + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOlistitem = (EOliteral + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

EOlast = (EOlistitem + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

eval_op_t = enum_eval_op_en # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 49

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 55
for _lib in _libs.values():
    try:
        eval_op_names = (POINTER(c_char) * (EOlast + 1)).in_dll(_lib, 'eval_op_names')
        break
    except:
        pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 56
for _lib in _libs.values():
    try:
        eval_args_of_op = (c_int * EOlast).in_dll(_lib, 'eval_args_of_op')
        break
    except:
        pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 62
class struct_eval_expr_st(Structure):
    pass

struct_eval_expr_st.__slots__ = [
    'op',
    'args',
]
struct_eval_expr_st._fields_ = [
    ('op', eval_op_t),
    ('args', c_int * 2),
]

eval_expr_t = struct_eval_expr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 62

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 40
class struct_list_psearch_st(Structure):
    pass

struct_list_psearch_st.__slots__ = [
    'user',
    'cmpf',
    'isearchdata',
    'is_sorted',
    'len',
]
struct_list_psearch_st._fields_ = [
    ('user', POINTER(None)),
    ('cmpf', CFUNCTYPE(UNCHECKED(c_int), POINTER(None), POINTER(None), POINTER(None))),
    ('isearchdata', POINTER(c_int)),
    ('is_sorted', c_int),
    ('len', c_int),
]

list_psearch_t = struct_list_psearch_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 40

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 46
class struct_list_search_st(Structure):
    pass

struct_list_search_st.__slots__ = [
    'list',
    'psearch',
]
struct_list_search_st._fields_ = [
    ('list', list_t),
    ('psearch', list_t),
]

list_search_t = struct_list_search_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 46

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 53
class struct_list_search_iterator_st(Structure):
    pass

struct_list_search_iterator_st.__slots__ = [
    'sp',
    'which',
    'last_id',
]
struct_list_search_iterator_st._fields_ = [
    ('sp', POINTER(list_search_t)),
    ('which', c_int),
    ('last_id', c_int),
]

list_search_iterator_t = struct_list_search_iterator_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 53

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 67
if hasattr(_libs['spiceparser'], 'list_search_init'):
    list_search_init = _libs['spiceparser'].list_search_init
    list_search_init.argtypes = [POINTER(list_search_t), c_int, c_int]
    list_search_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 68
if hasattr(_libs['spiceparser'], 'list_search_addrule'):
    list_search_addrule = _libs['spiceparser'].list_search_addrule
    list_search_addrule.argtypes = [POINTER(list_search_t), CFUNCTYPE(UNCHECKED(c_int), POINTER(None), POINTER(None), POINTER(None)), POINTER(None)]
    list_search_addrule.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 69
if hasattr(_libs['spiceparser'], 'list_search_resort'):
    list_search_resort = _libs['spiceparser'].list_search_resort
    list_search_resort.argtypes = [POINTER(list_search_t)]
    list_search_resort.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 70
if hasattr(_libs['spiceparser'], 'list_search_find'):
    list_search_find = _libs['spiceparser'].list_search_find
    list_search_find.argtypes = [POINTER(list_search_t), c_int, POINTER(None), POINTER(list_search_iterator_t)]
    list_search_find.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 71
if hasattr(_libs['spiceparser'], 'list_search_findnext'):
    list_search_findnext = _libs['spiceparser'].list_search_findnext
    list_search_findnext.argtypes = [POINTER(list_search_iterator_t)]
    list_search_findnext.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 72
if hasattr(_libs['spiceparser'], 'list_search_empty'):
    list_search_empty = _libs['spiceparser'].list_search_empty
    list_search_empty.argtypes = [POINTER(list_search_t)]
    list_search_empty.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 76
if hasattr(_libs['spiceparser'], 'list_search_qsort'):
    list_search_qsort = _libs['spiceparser'].list_search_qsort
    list_search_qsort.argtypes = [POINTER(list_search_t), POINTER(list_psearch_t)]
    list_search_qsort.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 31
class struct_memory_chain_st(Structure):
    pass

struct_memory_chain_st.__slots__ = [
    'next',
    'q',
    'qref',
    'data',
    'magic',
]
struct_memory_chain_st._fields_ = [
    ('next', POINTER(struct_memory_chain_st)),
    ('q', c_int),
    ('qref', c_int),
    ('data', c_char * (1024 * 16)),
    ('magic', c_int * 4),
]

memory_chain_t = struct_memory_chain_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 38

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 41
class struct_memory_other_st(Structure):
    pass

struct_memory_other_st.__slots__ = [
    'next',
]
struct_memory_other_st._fields_ = [
    ('next', POINTER(struct_memory_other_st)),
]

memory_other_t = struct_memory_other_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 44

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 50
class struct_memory_head_st(Structure):
    pass

struct_memory_head_st.__slots__ = [
    'head',
    'full',
    'others',
]
struct_memory_head_st._fields_ = [
    ('head', POINTER(memory_chain_t)),
    ('full', POINTER(memory_chain_t)),
    ('others', POINTER(memory_other_t)),
]

memory_t = struct_memory_head_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 50

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 55
if hasattr(_libs['spiceparser'], 'memory_alloc'):
    memory_alloc = _libs['spiceparser'].memory_alloc
    memory_alloc.argtypes = [POINTER(memory_t), c_int]
    memory_alloc.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 56
if hasattr(_libs['spiceparser'], 'memory_free'):
    memory_free = _libs['spiceparser'].memory_free
    memory_free.argtypes = [POINTER(memory_t), POINTER(None)]
    memory_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 57
if hasattr(_libs['spiceparser'], 'memory_freeall'):
    memory_freeall = _libs['spiceparser'].memory_freeall
    memory_freeall.argtypes = [POINTER(memory_t)]
    memory_freeall.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 58
if hasattr(_libs['spiceparser'], 'memory_init'):
    memory_init = _libs['spiceparser'].memory_init
    memory_init.argtypes = [POINTER(memory_t)]
    memory_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 29
class struct_sortlist_st(Structure):
    pass

struct_sortlist_st.__slots__ = [
    'index',
    'sorted',
]
struct_sortlist_st._fields_ = [
    ('index', c_int),
    ('sorted', c_ubyte * 1),
]

sortlist_t = struct_sortlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 29

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 43
class struct_mergedup_st(Structure):
    pass

struct_mergedup_st.__slots__ = [
    'qs',
    'es',
    'qun',
    'run',
    'q',
    'i',
    'flb',
    'last',
    'freelist',
    'data',
]
struct_mergedup_st._fields_ = [
    ('qs', c_int),
    ('es', c_int),
    ('qun', c_int),
    ('run', c_int),
    ('q', c_int),
    ('i', c_int),
    ('flb', c_int),
    ('last', POINTER(sortlist_t)),
    ('freelist', POINTER(c_ubyte)),
    ('data', String),
]

mergedup_t = struct_mergedup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 43

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 45
if hasattr(_libs['spiceparser'], 'mergedup_setbit'):
    mergedup_setbit = _libs['spiceparser'].mergedup_setbit
    mergedup_setbit.argtypes = [POINTER(mergedup_t), c_int]
    mergedup_setbit.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 46
if hasattr(_libs['spiceparser'], 'mergedup_testbit'):
    mergedup_testbit = _libs['spiceparser'].mergedup_testbit
    mergedup_testbit.argtypes = [POINTER(mergedup_t), c_int]
    mergedup_testbit.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 47
if hasattr(_libs['spiceparser'], 'mergedup_alloc'):
    mergedup_alloc = _libs['spiceparser'].mergedup_alloc
    mergedup_alloc.argtypes = [c_int, c_int]
    mergedup_alloc.restype = POINTER(mergedup_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 48
if hasattr(_libs['spiceparser'], 'mergedup_fill'):
    mergedup_fill = _libs['spiceparser'].mergedup_fill
    mergedup_fill.argtypes = [POINTER(mergedup_t), POINTER(c_ubyte), c_int]
    mergedup_fill.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 49
if hasattr(_libs['spiceparser'], 'mergedup_sort'):
    mergedup_sort = _libs['spiceparser'].mergedup_sort
    mergedup_sort.argtypes = [POINTER(mergedup_t)]
    mergedup_sort.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 50
if hasattr(_libs['spiceparser'], 'mergedup_visit'):
    mergedup_visit = _libs['spiceparser'].mergedup_visit
    mergedup_visit.argtypes = [POINTER(mergedup_t), c_int]
    mergedup_visit.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 51
if hasattr(_libs['spiceparser'], 'mergedup_free'):
    mergedup_free = _libs['spiceparser'].mergedup_free
    mergedup_free.argtypes = [POINTER(mergedup_t)]
    mergedup_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 48
class struct_file_line_st(Structure):
    pass

struct_file_line_st.__slots__ = [
    'fileindex',
    'line',
]
struct_file_line_st._fields_ = [
    ('fileindex', c_uint, 8),
    ('line', c_uint, 24),
]

file_line_t = struct_file_line_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 48

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 54
class struct_tokenmap_st(Structure):
    pass

struct_tokenmap_st.__slots__ = [
    'token',
    'str',
]
struct_tokenmap_st._fields_ = [
    ('token', c_int),
    ('str', String),
]

tokenmap_t = struct_tokenmap_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 54

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 57
class struct_card_st(Structure):
    pass

struct_card_st.__slots__ = [
    'next',
    'token',
    'val',
    'str',
]
struct_card_st._fields_ = [
    ('next', POINTER(struct_card_st)),
    ('token', c_int),
    ('val', String),
    ('str', c_char * 4),
]

card_t = struct_card_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 63

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 65
class struct_deck_st(Structure):
    pass

struct_deck_st.__slots__ = [
    'next',
    'card',
    'line',
]
struct_deck_st._fields_ = [
    ('next', POINTER(struct_deck_st)),
    ('card', POINTER(card_t)),
    ('line', file_line_t),
]

deck_t = struct_deck_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 70

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 86
class struct_scanner_def_st(Structure):
    pass

struct_scanner_def_st.__slots__ = [
    'line_stop',
    'eol_continue',
    'bol_continue',
    'convert_case',
    'quote_char',
    'newline',
    'assignment',
    'tokenize',
    'whitespace',
    'commentstart',
]
struct_scanner_def_st._fields_ = [
    ('line_stop', c_char * 32),
    ('eol_continue', c_char * 8),
    ('bol_continue', c_char * 8),
    ('convert_case', c_int),
    ('quote_char', c_char),
    ('newline', c_char),
    ('assignment', c_char),
    ('tokenize', c_char * 8),
    ('whitespace', c_char * 32),
    ('commentstart', c_char * 8),
]

scanner_def_t = struct_scanner_def_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 86

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 88
class struct_scanner_sect_st(Structure):
    pass

struct_scanner_sect_st.__slots__ = [
    'back',
    'tokenizer',
    '_def',
    'cp',
    'dp',
    'dhead',
    'eolstring',
    'lbuf',
    'eoline',
    'line_cont',
]
struct_scanner_sect_st._fields_ = [
    ('back', POINTER(struct_scanner_sect_st)),
    ('tokenizer', POINTER(names_t)),
    ('_def', POINTER(scanner_def_t)),
    ('cp', POINTER(card_t)),
    ('dp', POINTER(deck_t)),
    ('dhead', POINTER(deck_t)),
    ('eolstring', c_int),
    ('lbuf', c_char * 512),
    ('eoline', c_char * 512),
    ('line_cont', c_int),
]

scanner_sect_t = struct_scanner_sect_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 100

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 102
class struct_scanner_input_st(Structure):
    pass

struct_scanner_input_st.__slots__ = [
    'back',
    'next',
    'file_fp',
    'line',
    'index',
]
struct_scanner_input_st._fields_ = [
    ('back', POINTER(struct_scanner_input_st)),
    ('next', POINTER(struct_scanner_input_st)),
    ('file_fp', POINTER(None)),
    ('line', c_int),
    ('index', c_int),
]

scanner_input_t = struct_scanner_input_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 108

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 110
class struct_scanner_st(Structure):
    pass

struct_scanner_st.__slots__ = [
    'strmem',
    'inputp',
    'allinputs',
    'sectp',
    'errdeck',
    'errcard',
    'errfunc',
    'warnfunc',
]
struct_scanner_st._fields_ = [
    ('strmem', memory_t),
    ('inputp', POINTER(scanner_input_t)),
    ('allinputs', POINTER(scanner_input_t)),
    ('sectp', POINTER(scanner_sect_t)),
    ('errdeck', POINTER(deck_t)),
    ('errcard', POINTER(card_t)),
    ('errfunc', CFUNCTYPE(UNCHECKED(None), POINTER(struct_scanner_st), String, c_void_p)),
    ('warnfunc', CFUNCTYPE(UNCHECKED(None), POINTER(struct_scanner_st), String, c_void_p)),
]

scanner_t = struct_scanner_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 121

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 129
if hasattr(_libs['spiceparser'], 'scanner_add_tokens'):
    scanner_add_tokens = _libs['spiceparser'].scanner_add_tokens
    scanner_add_tokens.argtypes = [POINTER(scanner_t), POINTER(tokenmap_t)]
    scanner_add_tokens.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 130
if hasattr(_libs['spiceparser'], 'scanner_reset_tokens'):
    scanner_reset_tokens = _libs['spiceparser'].scanner_reset_tokens
    scanner_reset_tokens.argtypes = [POINTER(scanner_t)]
    scanner_reset_tokens.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 132
if hasattr(_libs['spiceparser'], 'scanner_init'):
    scanner_init = _libs['spiceparser'].scanner_init
    scanner_init.argtypes = [POINTER(scanner_t)]
    scanner_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 133
if hasattr(_libs['spiceparser'], 'scanner_release'):
    scanner_release = _libs['spiceparser'].scanner_release
    scanner_release.argtypes = [POINTER(scanner_t)]
    scanner_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 135
if hasattr(_libs['spiceparser'], 'scanner_input_newfp'):
    scanner_input_newfp = _libs['spiceparser'].scanner_input_newfp
    scanner_input_newfp.argtypes = [POINTER(scanner_t), POINTER(None)]
    scanner_input_newfp.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 136
if hasattr(_libs['spiceparser'], 'scanner_sect_new'):
    scanner_sect_new = _libs['spiceparser'].scanner_sect_new
    scanner_sect_new.argtypes = [POINTER(scanner_t), POINTER(scanner_def_t), POINTER(tokenmap_t)]
    scanner_sect_new.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 137
if hasattr(_libs['spiceparser'], 'scanner_input_release'):
    scanner_input_release = _libs['spiceparser'].scanner_input_release
    scanner_input_release.argtypes = [POINTER(scanner_t)]
    scanner_input_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 138
if hasattr(_libs['spiceparser'], 'scanner_sect_release'):
    scanner_sect_release = _libs['spiceparser'].scanner_sect_release
    scanner_sect_release.argtypes = [POINTER(scanner_t)]
    scanner_sect_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 141
if hasattr(_libs['spiceparser'], 'scanner_def_spice'):
    scanner_def_spice = _libs['spiceparser'].scanner_def_spice
    scanner_def_spice.argtypes = []
    scanner_def_spice.restype = POINTER(scanner_def_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 142
if hasattr(_libs['spiceparser'], 'scanner_def_err'):
    scanner_def_err = _libs['spiceparser'].scanner_def_err
    scanner_def_err.argtypes = [POINTER(scanner_t), String, c_void_p]
    scanner_def_err.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 149
if hasattr(_libs['spiceparser'], 'scanner_parse_all'):
    scanner_parse_all = _libs['spiceparser'].scanner_parse_all
    scanner_parse_all.argtypes = [POINTER(scanner_t)]
    scanner_parse_all.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 150
if hasattr(_libs['spiceparser'], 'scanner_free_all'):
    scanner_free_all = _libs['spiceparser'].scanner_free_all
    scanner_free_all.argtypes = [POINTER(scanner_t)]
    scanner_free_all.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 151
if hasattr(_libs['spiceparser'], 'scanner_parse_line'):
    scanner_parse_line = _libs['spiceparser'].scanner_parse_line
    scanner_parse_line.argtypes = [POINTER(scanner_t)]
    scanner_parse_line.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 152
if hasattr(_libs['spiceparser'], 'parse_binary'):
    parse_binary = _libs['spiceparser'].parse_binary
    parse_binary.argtypes = [POINTER(POINTER(c_char))]
    parse_binary.restype = c_uint

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 156
if hasattr(_libs['spiceparser'], 'parse_error'):
    _func = _libs['spiceparser'].parse_error
    _restype = None
    _argtypes = [POINTER(scanner_t), String]
    parse_error = _variadic_function(_func,_restype,_argtypes)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 157
if hasattr(_libs['spiceparser'], 'parse_warn'):
    _func = _libs['spiceparser'].parse_warn
    _restype = None
    _argtypes = [POINTER(scanner_t), String]
    parse_warn = _variadic_function(_func,_restype,_argtypes)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 158
if hasattr(_libs['spiceparser'], 'scanner_checkvalid'):
    scanner_checkvalid = _libs['spiceparser'].scanner_checkvalid
    scanner_checkvalid.argtypes = [POINTER(deck_t), c_int]
    scanner_checkvalid.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 159
if hasattr(_libs['spiceparser'], 'scanner_debug_all'):
    scanner_debug_all = _libs['spiceparser'].scanner_debug_all
    scanner_debug_all.argtypes = [POINTER(scanner_t), POINTER(None)]
    scanner_debug_all.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 160
if hasattr(_libs['spiceparser'], 'scanner_current_file_line'):
    scanner_current_file_line = _libs['spiceparser'].scanner_current_file_line
    scanner_current_file_line.argtypes = [POINTER(scanner_t)]
    scanner_current_file_line.restype = file_line_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_extract.h: 30
class struct_extract_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 265
class struct_spice_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 63
class struct_geninput_st(Structure):
    pass

struct_geninput_st.__slots__ = [
    'magic',
    'other',
]
struct_geninput_st._fields_ = [
    ('magic', c_int),
    ('other', c_int * 4),
]

geninput_t = struct_geninput_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 63

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 73
class union_netlist_input_un(Union):
    pass

union_netlist_input_un.__slots__ = [
    'p',
    'generic',
    'spice',
    'ext',
]
union_netlist_input_un._fields_ = [
    ('p', POINTER(None)),
    ('generic', POINTER(geninput_t)),
    ('spice', POINTER(struct_spice_st)),
    ('ext', POINTER(struct_extract_st)),
]

netlist_input_t = union_netlist_input_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 73

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 172
class struct_m_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 181
class struct_c_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 84
class union_dev_input_un(Union):
    pass

union_dev_input_un.__slots__ = [
    'p',
    'spice_fet',
    'spice_cap',
    'spice_res',
    'extract_fet',
    'extract_cap',
    'extract_res',
]
union_dev_input_un._fields_ = [
    ('p', POINTER(None)),
    ('spice_fet', POINTER(struct_m_st)),
    ('spice_cap', POINTER(struct_c_st)),
    ('spice_res', POINTER(None)),
    ('extract_fet', POINTER(None)),
    ('extract_cap', POINTER(None)),
    ('extract_res', POINTER(None)),
]

dev_input_t = union_dev_input_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 84

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 111
class struct_termptr_st(Structure):
    pass

struct_termptr_st.__slots__ = [
    'devi',
    'nonnull',
    'termi',
    'devt',
]
struct_termptr_st._fields_ = [
    ('devi', c_uint, 24),
    ('nonnull', c_uint, 1),
    ('termi', c_uint, 3),
    ('devt', c_uint, 4),
]

termptr_t = struct_termptr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 111

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 142
class struct_entity_st(Structure):
    pass

struct_entity_st.__slots__ = [
    'l',
    'qterms',
    'qvals',
    'qcount',
    'id',
    'qother',
    'sym',
]
struct_entity_st._fields_ = [
    ('l', list_t),
    ('qterms', c_int),
    ('qvals', c_int),
    ('qcount', c_int),
    ('id', c_int),
    ('qother', c_int),
    ('sym', c_char * 8),
]

entity_t = struct_entity_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 142

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 185
class struct_devnode_st(Structure):
    pass

struct_devnode_st.__slots__ = [
    'parent',
    'n',
]
struct_devnode_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
]

devnode_t = struct_devnode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 185

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 197
class struct_netlist_st(Structure):
    pass

struct_netlist_st.__slots__ = [
    'input',
    'eqn_mem',
    'iscopy',
    'names',
    'eqnl',
    'qe',
    'e',
]
struct_netlist_st._fields_ = [
    ('input', netlist_input_t),
    ('eqn_mem', POINTER(None)),
    ('iscopy', c_int),
    ('names', POINTER(names_t)),
    ('eqnl', eqnlist_t),
    ('qe', c_int),
    ('e', entity_t * ((1 << 4) - 1)),
]

netlist_t = struct_netlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 197

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 203
class struct_netlistfunc_st(Structure):
    pass

struct_netlistfunc_st.__slots__ = [
    'nl',
    'entity',
    'qcmp',
    'sum',
    'tocompare',
    'qproperties',
    'accumulate',
    'distribute',
    'fixup',
]
struct_netlistfunc_st._fields_ = [
    ('nl', POINTER(netlist_t)),
    ('entity', POINTER(entity_t)),
    ('qcmp', c_int),
    ('sum', CFUNCTYPE(UNCHECKED(c_int), POINTER(struct_netlistfunc_st), c_int, c_int)),
    ('tocompare', CFUNCTYPE(UNCHECKED(None), POINTER(struct_netlistfunc_st), c_int, POINTER(None))),
    ('qproperties', c_int),
    ('accumulate', CFUNCTYPE(UNCHECKED(None), POINTER(struct_netlistfunc_st), c_int, c_int, POINTER(c_float))),
    ('distribute', CFUNCTYPE(UNCHECKED(None), POINTER(struct_netlistfunc_st), c_int, c_int, POINTER(c_float))),
    ('fixup', CFUNCTYPE(UNCHECKED(None), POINTER(struct_netlistfunc_st), termptr_t)),
]

netlistfunc_t = struct_netlistfunc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 221

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 223
class struct_netlist_param_st(Structure):
    pass

struct_netlist_param_st.__slots__ = [
    'next',
    'str',
]
struct_netlist_param_st._fields_ = [
    ('next', POINTER(struct_netlist_param_st)),
    ('str', c_char * 4),
]

netlist_param_t = struct_netlist_param_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 227

enum_netprint_en = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_none = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_name = (netprint_none + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_index = (netprint_name + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_ptr = (netprint_index + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_nname = (netprint_ptr + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_debug = (netprint_nname + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

netprint_t = enum_netprint_en # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 239

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 245
if hasattr(_libs['spiceparser'], 'netlist_init'):
    netlist_init = _libs['spiceparser'].netlist_init
    netlist_init.argtypes = [POINTER(netlist_t)]
    netlist_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 246
if hasattr(_libs['spiceparser'], 'netlist_register_entity'):
    netlist_register_entity = _libs['spiceparser'].netlist_register_entity
    netlist_register_entity.argtypes = [POINTER(netlist_t), c_int, c_int, c_int, c_int, String, c_int]
    netlist_register_entity.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 247
if hasattr(_libs['spiceparser'], 'netlist_print_nodep'):
    netlist_print_nodep = _libs['spiceparser'].netlist_print_nodep
    netlist_print_nodep.argtypes = [POINTER(netlist_t), netprint_t, POINTER(None), POINTER(None), String]
    netlist_print_nodep.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 248
if hasattr(_libs['spiceparser'], 'netlist_parse_input'):
    netlist_parse_input = _libs['spiceparser'].netlist_parse_input
    netlist_parse_input.argtypes = [POINTER(scanner_t), String, POINTER(netlist_param_t)]
    netlist_parse_input.restype = netlist_input_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 249
if hasattr(_libs['spiceparser'], 'netlist_release'):
    netlist_release = _libs['spiceparser'].netlist_release
    netlist_release.argtypes = [POINTER(netlist_t)]
    netlist_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 250
if hasattr(_libs['spiceparser'], 'netlist_free'):
    netlist_free = _libs['spiceparser'].netlist_free
    netlist_free.argtypes = [POINTER(netlist_t)]
    netlist_free.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 251
if hasattr(_libs['spiceparser'], 'netlist_newdev_fromnode'):
    netlist_newdev_fromnode = _libs['spiceparser'].netlist_newdev_fromnode
    netlist_newdev_fromnode.argtypes = [POINTER(netlist_t), c_int, dev_input_t, POINTER(termptr_t)]
    netlist_newdev_fromnode.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 252
if hasattr(_libs['spiceparser'], 'netlist_debug_input'):
    netlist_debug_input = _libs['spiceparser'].netlist_debug_input
    netlist_debug_input.argtypes = [POINTER(None), netlist_input_t]
    netlist_debug_input.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 253
if hasattr(_libs['spiceparser'], 'netlist_debug'):
    netlist_debug = _libs['spiceparser'].netlist_debug
    netlist_debug.argtypes = [POINTER(None), POINTER(netlist_t)]
    netlist_debug.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 254
if hasattr(_libs['spiceparser'], 'netlist_debug_'):
    netlist_debug_ = _libs['spiceparser'].netlist_debug_
    netlist_debug_.argtypes = [POINTER(None), POINTER(netlist_t), c_int]
    netlist_debug_.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 255
if hasattr(_libs['spiceparser'], 'netlist_node'):
    netlist_node = _libs['spiceparser'].netlist_node
    netlist_node.argtypes = [POINTER(netlist_t), String, POINTER(None)]
    netlist_node.restype = termptr_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 256
if hasattr(_libs['spiceparser'], 'netlist_termptr'):
    netlist_termptr = _libs['spiceparser'].netlist_termptr
    netlist_termptr.argtypes = [c_int, c_int, c_int]
    netlist_termptr.restype = termptr_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 257
if hasattr(_libs['spiceparser'], 'netlist_node_termptr'):
    netlist_node_termptr = _libs['spiceparser'].netlist_node_termptr
    netlist_node_termptr.argtypes = [POINTER(netlist_t), termptr_t]
    netlist_node_termptr.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 258
if hasattr(_libs['spiceparser'], 'netlist_findnode'):
    netlist_findnode = _libs['spiceparser'].netlist_findnode
    netlist_findnode.argtypes = [POINTER(netlist_t), String]
    netlist_findnode.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 259
if hasattr(_libs['spiceparser'], 'netlist_merge'):
    netlist_merge = _libs['spiceparser'].netlist_merge
    netlist_merge.argtypes = [POINTER(netlistfunc_t)]
    netlist_merge.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 260
if hasattr(_libs['spiceparser'], 'netlist_distribute'):
    netlist_distribute = _libs['spiceparser'].netlist_distribute
    netlist_distribute.argtypes = [POINTER(netlistfunc_t)]
    netlist_distribute.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 261
if hasattr(_libs['spiceparser'], 'netlist_fixup'):
    netlist_fixup = _libs['spiceparser'].netlist_fixup
    netlist_fixup.argtypes = [POINTER(netlistfunc_t)]
    netlist_fixup.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 262
if hasattr(_libs['spiceparser'], 'netlist_eval'):
    netlist_eval = _libs['spiceparser'].netlist_eval
    netlist_eval.argtypes = [POINTER(netlist_t)]
    netlist_eval.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 263
if hasattr(_libs['spiceparser'], 'netlist_eqn_begin'):
    netlist_eqn_begin = _libs['spiceparser'].netlist_eqn_begin
    netlist_eqn_begin.argtypes = [POINTER(netlist_t)]
    netlist_eqn_begin.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 264
if hasattr(_libs['spiceparser'], 'netlist_eqn_end'):
    netlist_eqn_end = _libs['spiceparser'].netlist_eqn_end
    netlist_eqn_end.argtypes = [POINTER(netlist_t)]
    netlist_eqn_end.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 266
if hasattr(_libs['spiceparser'], 'netlist_copyisher'):
    netlist_copyisher = _libs['spiceparser'].netlist_copyisher
    netlist_copyisher.argtypes = [POINTER(netlist_t), c_int, POINTER(c_int)]
    netlist_copyisher.restype = POINTER(netlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 267
for _lib in _libs.itervalues():
    if not hasattr(_lib, 'netlist_copyfree'):
        continue
    netlist_copyfree = _lib.netlist_copyfree
    netlist_copyfree.argtypes = [POINTER(netlist_t)]
    netlist_copyfree.restype = None
    break

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 272
if hasattr(_libs['spiceparser'], 'spice_new'):
    spice_new = _libs['spiceparser'].spice_new
    spice_new.argtypes = [POINTER(scanner_t)]
    spice_new.restype = POINTER(struct_spice_st)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 273
if hasattr(_libs['spiceparser'], 'spice_release'):
    spice_release = _libs['spiceparser'].spice_release
    spice_release.argtypes = [POINTER(struct_spice_st)]
    spice_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 275
if hasattr(_libs['spiceparser'], 'spice_build'):
    spice_build = _libs['spiceparser'].spice_build
    spice_build.argtypes = [POINTER(netlist_t)]
    spice_build.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 276
if hasattr(_libs['spiceparser'], 'spice_count'):
    spice_count = _libs['spiceparser'].spice_count
    spice_count.argtypes = [POINTER(netlist_t)]
    spice_count.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 277
if hasattr(_libs['spiceparser'], 'spice_debug'):
    spice_debug = _libs['spiceparser'].spice_debug
    spice_debug.argtypes = [POINTER(None), POINTER(struct_spice_st)]
    spice_debug.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 87
class struct_devgen_st(Structure):
    pass

struct_devgen_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devgen_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * ((1 << 3) - 1)),
    ('v', eqn_t * 8),
]

devgen_t = struct_devgen_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 87

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 98
class struct_devfet_st(Structure):
    pass

struct_devfet_st.__slots__ = [
    'parent',
    'n',
    'v',
    'type',
]
struct_devfet_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 4),
    ('v', eqn_t * 6),
    ('type', c_uint),
]

devfet_t = struct_devfet_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 98

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 106
class struct_devcap_st(Structure):
    pass

struct_devcap_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devcap_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

devcap_t = struct_devcap_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 106

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 114
class struct_devres_st(Structure):
    pass

struct_devres_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devres_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

devres_t = struct_devres_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 114

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 122
class struct_devind_st(Structure):
    pass

struct_devind_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devind_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

devind_t = struct_devind_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 122

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 130
class struct_devvsrc_st(Structure):
    pass

struct_devvsrc_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devvsrc_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

devvsrc_t = struct_devvsrc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 130

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 138
class struct_devisrc_st(Structure):
    pass

struct_devisrc_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devisrc_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

devisrc_t = struct_devisrc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 138

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 146
class struct_devdiode_st(Structure):
    pass

struct_devdiode_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devdiode_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 4),
]

devdiode_t = struct_devdiode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 146

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 154
class struct_devbjt_st(Structure):
    pass

struct_devbjt_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_devbjt_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 4),
    ('v', eqn_t * 4),
]

devbjt_t = struct_devbjt_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 154

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 161
class struct_dev2term_st(Structure):
    pass

struct_dev2term_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_dev2term_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 2),
    ('v', eqn_t * 1),
]

dev2term_t = struct_dev2term_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 161

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 168
class struct_dev4term_st(Structure):
    pass

struct_dev4term_st.__slots__ = [
    'parent',
    'n',
    'v',
]
struct_dev4term_st._fields_ = [
    ('parent', dev_input_t),
    ('n', termptr_t * 4),
    ('v', eqn_t * 1),
]

dev4term_t = struct_dev4term_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 168

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 181
class union_devall_un(Union):
    pass

union_devall_un.__slots__ = [
    'p',
    'genp',
    'nodep',
    'fetp',
    'capp',
    'indp',
    'bjtp',
    'vsrcp',
    'isrcp',
]
union_devall_un._fields_ = [
    ('p', POINTER(None)),
    ('genp', POINTER(devgen_t)),
    ('nodep', POINTER(devnode_t)),
    ('fetp', POINTER(devfet_t)),
    ('capp', POINTER(devcap_t)),
    ('indp', POINTER(devind_t)),
    ('bjtp', POINTER(devbjt_t)),
    ('vsrcp', POINTER(devvsrc_t)),
    ('isrcp', POINTER(devisrc_t)),
]

devall_p = union_devall_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 181

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 194
if hasattr(_libs['spiceparser'], 'netlist_copyish'):
    netlist_copyish = _libs['spiceparser'].netlist_copyish
    netlist_copyish.argtypes = [POINTER(netlist_t), c_int, POINTER(c_int)]
    netlist_copyish.restype = POINTER(netlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 195
if hasattr(_libs['spiceparser'], 'netlist_o_spice'):
    netlist_o_spice = _libs['spiceparser'].netlist_o_spice
    netlist_o_spice.argtypes = [POINTER(None), POINTER(netlist_t), c_int]
    netlist_o_spice.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 196
if hasattr(_libs['spiceparser'], 'netlist_devnew_inplace'):
    netlist_devnew_inplace = _libs['spiceparser'].netlist_devnew_inplace
    netlist_devnew_inplace.argtypes = [netlist_input_t, c_int, c_int * 9]
    netlist_devnew_inplace.restype = POINTER(netlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 197
if hasattr(_libs['spiceparser'], 'netlist_devnew'):
    netlist_devnew = _libs['spiceparser'].netlist_devnew
    netlist_devnew.argtypes = [netlist_input_t]
    netlist_devnew.restype = POINTER(netlist_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 199
if hasattr(_libs['spiceparser'], 'netlist_devfet_funcs'):
    netlist_devfet_funcs = _libs['spiceparser'].netlist_devfet_funcs
    netlist_devfet_funcs.argtypes = [POINTER(netlist_t), POINTER(netlistfunc_t)]
    netlist_devfet_funcs.restype = POINTER(netlistfunc_t)

struct_extract_st.__slots__ = [
    'extract_magic',
    'root',
    'fname',
    'did_EF_init_read',
    'merged_list',
    'ext_argc',
    'ext_argv',
]
struct_extract_st._fields_ = [
    ('extract_magic', c_int),
    ('root', String),
    ('fname', String),
    ('did_EF_init_read', c_int),
    ('merged_list', POINTER(None)),
    ('ext_argc', c_int),
    ('ext_argv', POINTER(POINTER(c_char))),
]

extract_t = struct_extract_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_extract.h: 39

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 46
class struct_nlibiodef_st(Structure):
    pass

struct_nlibiodef_st.__slots__ = [
    'encoding',
    'wires',
    'tokens',
    'digitize',
]
struct_nlibiodef_st._fields_ = [
    ('encoding', String),
    ('wires', c_int),
    ('tokens', c_int),
    ('digitize', c_int),
]

nlibiodef_t = struct_nlibiodef_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 46

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 56
class struct_nlibio_st(Structure):
    pass

struct_nlibio_st.__slots__ = [
    'tokens',
    'qnodes',
    'digitize',
    'nodes',
]
struct_nlibio_st._fields_ = [
    ('tokens', c_int),
    ('qnodes', c_int),
    ('digitize', c_int),
    ('nodes', c_int * 4),
]

nlibio_t = struct_nlibio_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 56

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 62
class struct_nlibiol_st(Structure):
    pass

struct_nlibiol_st.__slots__ = [
    'iol',
    'qtokens',
]
struct_nlibiol_st._fields_ = [
    ('iol', list_t),
    ('qtokens', c_int),
]

nlibiol_t = struct_nlibiol_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 62

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 70
class struct_nlibpm_st(Structure):
    pass

struct_nlibpm_st.__slots__ = [
    'index',
    'min',
    'max',
    'qty',
]
struct_nlibpm_st._fields_ = [
    ('index', c_int),
    ('min', c_float),
    ('max', c_float),
    ('qty', c_int),
]

nlibpm_t = struct_nlibpm_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 70

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 80
class struct_nlibfunc_st(Structure):
    pass

struct_nlibfunc_st.__slots__ = [
    'p_delay',
    'p_cycle',
    'p_offset',
    'qin',
    'qout',
    'map',
]
struct_nlibfunc_st._fields_ = [
    ('p_delay', c_int),
    ('p_cycle', c_int),
    ('p_offset', c_int),
    ('qin', c_int),
    ('qout', c_int),
    ('map', c_int * 2),
]

nlibfunc_t = struct_nlibfunc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 80

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 86
class struct_nlibfref_st(Structure):
    pass

struct_nlibfref_st.__slots__ = [
    'index',
]
struct_nlibfref_st._fields_ = [
    ('index', c_int),
]

nlibfref_t = struct_nlibfref_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 86

enum_nlibreftype_en = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

RTrseries = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

RTcshunt = 1 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

RTdelay = 2 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

RTqty = (RTdelay + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

nlibreftype_t = enum_nlibreftype_en # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 97

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 105
class struct_nlibrefnode_st(Structure):
    pass

struct_nlibrefnode_st.__slots__ = [
    'skew',
    'vrefi',
    'devnodei',
]
struct_nlibrefnode_st._fields_ = [
    ('skew', eqn_t * 3),
    ('vrefi', c_int),
    ('devnodei', c_int),
]

nlibrefnode_t = struct_nlibrefnode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 105

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 116
class struct_nlibdb_st(Structure):
    pass

struct_nlibdb_st.__slots__ = [
    'nl',
    '_in',
    'out',
    'map',
    'params',
    'refnodes',
    'pvals',
]
struct_nlibdb_st._fields_ = [
    ('nl', POINTER(netlist_t)),
    ('_in', nlibiol_t),
    ('out', nlibiol_t),
    ('map', nlibfref_t),
    ('params', list_t),
    ('refnodes', list_t),
    ('pvals', POINTER(c_float)),
]

nlibdb_t = struct_nlibdb_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 116

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 126
class struct_nlibflatdb_st(Structure):
    pass

struct_nlibflatdb_st.__slots__ = [
    'lib_index',
    'db_index',
    'qvals',
    'pvals',
    'uservals',
]
struct_nlibflatdb_st._fields_ = [
    ('lib_index', c_int),
    ('db_index', c_int),
    ('qvals', c_int),
    ('pvals', POINTER(c_float)),
    ('uservals', list_t),
]

nlibflatdb_t = struct_nlibflatdb_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 126

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 142
class struct_nlib_st(Structure):
    pass

struct_nlib_st.__slots__ = [
    'iodefs',
    'db',
    'dbref',
    'vref',
    'qvref',
    'funcs',
    'funcnames',
    'eqnl',
    'flags',
    'flatdb',
    'eqn_mem',
]
struct_nlib_st._fields_ = [
    ('iodefs', list_t),
    ('db', list_t),
    ('dbref', POINTER(names_t)),
    ('vref', POINTER(names_t)),
    ('qvref', c_int),
    ('funcs', list_t),
    ('funcnames', POINTER(names_t)),
    ('eqnl', eqnlist_t),
    ('flags', POINTER(bitlist_t)),
    ('flatdb', list_t),
    ('eqn_mem', POINTER(None)),
]

nlib_t = struct_nlib_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 142

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 157
class struct_nlib_icall_st(Structure):
    pass

struct_nlib_icall_st.__slots__ = [
    'dbi',
    'flatdbi',
    '_in',
    'out',
    'itokens',
    'otokens',
    'ctoken',
    'ver',
    'err',
    'idigitize',
    'odigitize',
    'inode',
    'onode',
]
struct_nlib_icall_st._fields_ = [
    ('dbi', c_int),
    ('flatdbi', c_int),
    ('_in', POINTER(c_float) * 4),
    ('out', POINTER(c_float) * 4),
    ('itokens', c_int * 4),
    ('otokens', c_int * 4),
    ('ctoken', c_int),
    ('ver', c_int),
    ('err', c_int),
    ('idigitize', c_int),
    ('odigitize', c_int),
    ('inode', c_int),
    ('onode', c_int),
]

nlib_icall_t = struct_nlib_icall_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 157

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 165
class struct_nlib_ifref_st(Structure):
    pass

struct_nlib_ifref_st.__slots__ = [
    'val',
    'vals',
    'name',
]
struct_nlib_ifref_st._fields_ = [
    ('val', POINTER(c_float)),
    ('vals', c_float * 4),
    ('name', c_char * 64),
]

nlib_ifref_t = struct_nlib_ifref_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 165

enum_nlib_refid_en = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

NLIBref_vss = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

NLIBref_vdd = (NLIBref_vss + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

NLIBref_clk = (NLIBref_vdd + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

NLIBref_firstunused = (NLIBref_clk + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

NLIBref_max = 512 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

nlib_refid_e = enum_nlib_refid_en # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 174

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 185
class struct_nlib_iface_st(Structure):
    pass

struct_nlib_iface_st.__slots__ = [
    'nlib',
    'icalls',
    'frefs',
    'ref_map',
    'phase',
    'lookup_node_f',
    'user',
]
struct_nlib_iface_st._fields_ = [
    ('nlib', POINTER(nlib_t)),
    ('icalls', list_t),
    ('frefs', list_t),
    ('ref_map', c_int * NLIBref_max),
    ('phase', c_int),
    ('lookup_node_f', CFUNCTYPE(UNCHECKED(POINTER(c_float)), POINTER(None), String)),
    ('user', POINTER(None)),
]

nlib_iface_t = struct_nlib_iface_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 185

enum_nlib_tokens_en = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_start = 1024 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_nlib = (Knlib_start + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_input = (Knlib_nlib + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_output = (Knlib_input + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_param = (Knlib_output + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_netlist = (Knlib_param + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_spice = (Knlib_netlist + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_encoding = (Knlib_spice + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_wires = (Knlib_encoding + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_tokens = (Knlib_wires + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_digitize = (Knlib_tokens + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_digital = (Knlib_digitize + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_qtyin = (Knlib_digital + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_qtyout = (Knlib_qtyin + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_end_digital = (Knlib_qtyout + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_min = (Knlib_end_digital + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_max = (Knlib_min + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_qty = (Knlib_max + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_function = (Knlib_qty + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_end_netlist = (Knlib_function + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_define = (Knlib_end_netlist + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_reference = (Knlib_define + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_name = (Knlib_reference + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_rseries = (Knlib_name + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_cshunt = (Knlib_rseries + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_delay = (Knlib_cshunt + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_p_delay = (Knlib_delay + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_p_offset = (Knlib_p_delay + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_p_cycle = (Knlib_p_offset + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

Knlib_end = (Knlib_p_cycle + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

nlib_tokens_t = enum_nlib_tokens_en # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 198

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 232
class struct_nlib_process_st(Structure):
    pass

struct_nlib_process_st.__slots__ = [
    'process',
    'user',
    'nlib',
    'lib_index',
    'db_index',
    'nl',
]
struct_nlib_process_st._fields_ = [
    ('process', CFUNCTYPE(UNCHECKED(None), POINTER(struct_nlib_process_st))),
    ('user', POINTER(None)),
    ('nlib', POINTER(nlib_t)),
    ('lib_index', c_int),
    ('db_index', c_int),
    ('nl', POINTER(netlist_t)),
]

nlib_process_t = struct_nlib_process_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 243

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 246
if hasattr(_libs['spiceparser'], 'nlib_parse'):
    nlib_parse = _libs['spiceparser'].nlib_parse
    nlib_parse.argtypes = [POINTER(nlib_t), POINTER(scanner_t)]
    nlib_parse.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 247
if hasattr(_libs['spiceparser'], 'nlib_add_io'):
    nlib_add_io = _libs['spiceparser'].nlib_add_io
    nlib_add_io.argtypes = [POINTER(nlib_t), c_int, POINTER(nlibiol_t), c_int, c_int, c_int, POINTER(POINTER(c_char))]
    nlib_add_io.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 248
if hasattr(_libs['spiceparser'], 'nlib_init'):
    nlib_init = _libs['spiceparser'].nlib_init
    nlib_init.argtypes = [POINTER(nlib_t)]
    nlib_init.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 249
if hasattr(_libs['spiceparser'], 'nlib_add_pm'):
    nlib_add_pm = _libs['spiceparser'].nlib_add_pm
    nlib_add_pm.argtypes = [POINTER(nlib_t), c_int, String, c_float, c_float, c_int]
    nlib_add_pm.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 250
if hasattr(_libs['spiceparser'], 'nlib_new_db'):
    nlib_new_db = _libs['spiceparser'].nlib_new_db
    nlib_new_db.argtypes = [POINTER(nlib_t), String]
    nlib_new_db.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 251
if hasattr(_libs['spiceparser'], 'nlib_db_netlist'):
    nlib_db_netlist = _libs['spiceparser'].nlib_db_netlist
    nlib_db_netlist.argtypes = [POINTER(nlib_t), c_int, POINTER(netlist_t)]
    nlib_db_netlist.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 252
if hasattr(_libs['spiceparser'], 'nlib_db_func'):
    nlib_db_func = _libs['spiceparser'].nlib_db_func
    nlib_db_func.argtypes = [POINTER(nlib_t), c_int, String]
    nlib_db_func.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 253
if hasattr(_libs['spiceparser'], 'nlib_process'):
    nlib_process = _libs['spiceparser'].nlib_process
    nlib_process.argtypes = [POINTER(nlib_process_t), c_int]
    nlib_process.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 254
if hasattr(_libs['spiceparser'], 'nlib_fixup'):
    nlib_fixup = _libs['spiceparser'].nlib_fixup
    nlib_fixup.argtypes = [POINTER(nlib_t)]
    nlib_fixup.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 255
if hasattr(_libs['spiceparser'], 'nlib_disable'):
    nlib_disable = _libs['spiceparser'].nlib_disable
    nlib_disable.argtypes = [POINTER(nlib_t), c_int]
    nlib_disable.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 256
if hasattr(_libs['spiceparser'], 'nlib_isdisabled'):
    nlib_isdisabled = _libs['spiceparser'].nlib_isdisabled
    nlib_isdisabled.argtypes = [POINTER(nlib_t), c_int]
    nlib_isdisabled.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 258
if hasattr(_libs['spiceparser'], 'nlib_release'):
    nlib_release = _libs['spiceparser'].nlib_release
    nlib_release.argtypes = [POINTER(nlib_t)]
    nlib_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 260
if hasattr(_libs['spiceparser'], 'nlib_flat'):
    nlib_flat = _libs['spiceparser'].nlib_flat
    nlib_flat.argtypes = [POINTER(nlib_process_t), c_int, c_int]
    nlib_flat.restype = POINTER(None)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 261
if hasattr(_libs['spiceparser'], 'nlib_o_spice_subckts'):
    nlib_o_spice_subckts = _libs['spiceparser'].nlib_o_spice_subckts
    nlib_o_spice_subckts.argtypes = [POINTER(nlib_t), POINTER(None)]
    nlib_o_spice_subckts.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 262
if hasattr(_libs['spiceparser'], 'nlib_o_spice_call'):
    nlib_o_spice_call = _libs['spiceparser'].nlib_o_spice_call
    nlib_o_spice_call.argtypes = [POINTER(nlib_t), c_int, c_int, c_int, POINTER(c_int), POINTER(None)]
    nlib_o_spice_call.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 263
if hasattr(_libs['spiceparser'], 'nlib_o_spice_refs'):
    nlib_o_spice_refs = _libs['spiceparser'].nlib_o_spice_refs
    nlib_o_spice_refs.argtypes = [POINTER(nlib_t), POINTER(None)]
    nlib_o_spice_refs.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 264
if hasattr(_libs['spiceparser'], 'nlib_flatdb_write'):
    nlib_flatdb_write = _libs['spiceparser'].nlib_flatdb_write
    nlib_flatdb_write.argtypes = [POINTER(nlib_t), POINTER(None)]
    nlib_flatdb_write.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 265
if hasattr(_libs['spiceparser'], 'nlib_flatdb_read'):
    nlib_flatdb_read = _libs['spiceparser'].nlib_flatdb_read
    nlib_flatdb_read.argtypes = [POINTER(nlib_t), POINTER(None)]
    nlib_flatdb_read.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 269
if hasattr(_libs['spiceparser'], 'nlib_iface_getref'):
    nlib_iface_getref = _libs['spiceparser'].nlib_iface_getref
    nlib_iface_getref.argtypes = [POINTER(nlib_iface_t), c_int]
    nlib_iface_getref.restype = POINTER(nlib_ifref_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 270
if hasattr(_libs['spiceparser'], 'nlib_iface_phase'):
    nlib_iface_phase = _libs['spiceparser'].nlib_iface_phase
    nlib_iface_phase.argtypes = [POINTER(nlib_iface_t)]
    nlib_iface_phase.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 271
if hasattr(_libs['spiceparser'], 'nlib_i_spice_calls'):
    nlib_i_spice_calls = _libs['spiceparser'].nlib_i_spice_calls
    nlib_i_spice_calls.argtypes = [POINTER(nlib_iface_t), POINTER(None)]
    nlib_i_spice_calls.restype = c_int

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 272
if hasattr(_libs['spiceparser'], 'nlib_iface_init'):
    nlib_iface_init = _libs['spiceparser'].nlib_iface_init
    nlib_iface_init.argtypes = [POINTER(nlib_iface_t), POINTER(nlib_t)]
    nlib_iface_init.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 273
if hasattr(_libs['spiceparser'], 'nlib_iface_release'):
    nlib_iface_release = _libs['spiceparser'].nlib_iface_release
    nlib_iface_release.argtypes = [POINTER(nlib_iface_t)]
    nlib_iface_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 223
class struct_subckt_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 71
class union_paydata_u(Union):
    pass

union_paydata_u.__slots__ = [
    'p',
    's',
    'subckt',
    't',
]
union_paydata_u._fields_ = [
    ('p', POINTER(None)),
    ('s', String),
    ('subckt', POINTER(struct_subckt_st)),
    ('t', termptr_t),
]

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 83
class struct_hashload_st(Structure):
    pass

struct_hashload_st.__slots__ = [
    'flag',
    'data',
]
struct_hashload_st._fields_ = [
    ('flag', c_int),
    ('data', union_paydata_u),
]

hashload_t = struct_hashload_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 83

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 89
class struct_nodeclient_st(Structure):
    pass

struct_nodeclient_st.__slots__ = [
    'payload',
    'str',
]
struct_nodeclient_st._fields_ = [
    ('payload', hashload_t),
    ('str', c_ubyte * 4),
]

nodeclient_t = struct_nodeclient_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 89

node_t = POINTER(struct_nodeclient_st) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 91

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 117
class struct_callparam_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 101
class struct_paramload_st(Structure):
    pass

struct_paramload_st.__slots__ = [
    'eqn',
    'patch_call',
    'global_i',
]
struct_paramload_st._fields_ = [
    ('eqn', eqn_t),
    ('patch_call', POINTER(struct_callparam_st)),
    ('global_i', c_int),
]

paramload_t = struct_paramload_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 101

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 108
class struct_paramclient_st(Structure):
    pass

struct_paramclient_st.__slots__ = [
    'payload',
    'str',
]
struct_paramclient_st._fields_ = [
    ('payload', paramload_t),
    ('str', c_char * 4),
]

paramclient_t = struct_paramclient_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 108

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 254
class struct_stack_st(Structure):
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 114
class struct_paramlookup_st(Structure):
    pass

struct_paramlookup_st.__slots__ = [
    'sp',
    'nl',
]
struct_paramlookup_st._fields_ = [
    ('sp', POINTER(struct_stack_st)),
    ('nl', POINTER(struct_netlist_st)),
]

paramlookup_t = struct_paramlookup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 114

struct_callparam_st.__slots__ = [
    'eqn',
    'str',
]
struct_callparam_st._fields_ = [
    ('eqn', eqn_t),
    ('str', c_char * 4),
]

callparam_t = struct_callparam_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 121

enum_keyword_et = c_int # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kother = 0 # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kinclude = (Kother + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Ksubckt = (Kinclude + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kends = (Ksubckt + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kend = (Kends + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kendm = (Kend + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kmodel = (Kendm + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kparam = (Kmodel + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kglobal = (Kparam + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kmult = (Kglobal + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Kscale = (Kmult + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

Knull = (Kscale + 1) # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

keyword_t = enum_keyword_et # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 134

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 149
try:
    spice_tokens = (POINTER(tokenmap_t)).in_dll(_libs['spiceparser'], 'spice_tokens')
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 165
class struct_x_st(Structure):
    pass

struct_x_st.__slots__ = [
    'nn',
    'xp',
    'nodes',
    'locals',
    'nl',
    'deck',
    'rest',
]
struct_x_st._fields_ = [
    ('nn', c_int),
    ('xp', POINTER(struct_subckt_st)),
    ('nodes', POINTER(node_t)),
    ('locals', POINTER(POINTER(callparam_t))),
    ('nl', c_int),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

x_t = struct_x_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 165

struct_m_st.__slots__ = [
    'nodes',
    'l',
    'w',
    '_as',
    'ad',
    'ps',
    'pd',
    'deck',
    'rest',
    'type',
]
struct_m_st._fields_ = [
    ('nodes', node_t * 4),
    ('l', eqn_t),
    ('w', eqn_t),
    ('_as', eqn_t),
    ('ad', eqn_t),
    ('ps', eqn_t),
    ('pd', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
    ('type', uchar),
]

m_t = struct_m_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 179

struct_c_st.__slots__ = [
    'nodes',
    'c',
    'deck',
    'rest',
]
struct_c_st._fields_ = [
    ('nodes', node_t * 2),
    ('c', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

c_t = struct_c_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 187

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 195
class struct_r_st(Structure):
    pass

struct_r_st.__slots__ = [
    'nodes',
    'r',
    'deck',
    'rest',
]
struct_r_st._fields_ = [
    ('nodes', node_t * 2),
    ('r', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

r_t = struct_r_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 195

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 203
class struct_l_st(Structure):
    pass

struct_l_st.__slots__ = [
    'nodes',
    'l',
    'deck',
    'rest',
]
struct_l_st._fields_ = [
    ('nodes', node_t * 2),
    ('l', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

l_t = struct_l_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 203

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 211
class struct_v_st(Structure):
    pass

struct_v_st.__slots__ = [
    'nodes',
    'v',
    'deck',
    'rest',
]
struct_v_st._fields_ = [
    ('nodes', node_t * 2),
    ('v', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

v_t = struct_v_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 211

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 219
class struct_i_st(Structure):
    pass

struct_i_st.__slots__ = [
    'nodes',
    'i',
    'deck',
    'rest',
]
struct_i_st._fields_ = [
    ('nodes', node_t * 2),
    ('i', eqn_t),
    ('deck', POINTER(deck_t)),
    ('rest', POINTER(card_t)),
]

i_t = struct_i_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 219

struct_subckt_st.__slots__ = [
    'subckt_magic',
    'parent',
    'nodes',
    'params',
    'lparams',
    'cktdir',
    '_global',
    'name',
    'ndefn',
    'nm',
    'nc',
    'nr',
    'nl',
    'nx',
    'nv',
    'ni',
    'defn',
    'm',
    'c',
    'r',
    'l',
    'x',
    'v',
    'i',
    'flag',
    'scale',
    'mult',
]
struct_subckt_st._fields_ = [
    ('subckt_magic', c_int),
    ('parent', POINTER(struct_subckt_st)),
    ('nodes', POINTER(hash_t)),
    ('params', POINTER(hash_t)),
    ('lparams', POINTER(hash_t)),
    ('cktdir', POINTER(hash_t)),
    ('_global', POINTER(hash_t)),
    ('name', POINTER(uchar)),
    ('ndefn', c_int),
    ('nm', c_int),
    ('nc', c_int),
    ('nr', c_int),
    ('nl', c_int),
    ('nx', c_int),
    ('nv', c_int),
    ('ni', c_int),
    ('defn', POINTER(node_t)),
    ('m', POINTER(m_t)),
    ('c', POINTER(c_t)),
    ('r', POINTER(r_t)),
    ('l', POINTER(l_t)),
    ('x', POINTER(x_t)),
    ('v', POINTER(v_t)),
    ('i', POINTER(i_t)),
    ('flag', c_int),
    ('scale', c_float),
    ('mult', c_float),
]

subckt_t = struct_subckt_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 251

struct_stack_st.__slots__ = [
    'level',
    'parent',
    'ckt',
    'call',
    'top',
    'nl',
    'scan',
]
struct_stack_st._fields_ = [
    ('level', c_int),
    ('parent', POINTER(struct_stack_st)),
    ('ckt', POINTER(subckt_t)),
    ('call', POINTER(x_t)),
    ('top', POINTER(struct_stack_st)),
    ('nl', POINTER(struct_netlist_st)),
    ('scan', POINTER(scanner_t)),
]

stack_t = struct_stack_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 263

struct_spice_st.__slots__ = [
    'spice_magic',
    'scan',
    'deck',
    'ckt',
    'eqn_mem',
]
struct_spice_st._fields_ = [
    ('spice_magic', c_int),
    ('scan', POINTER(scanner_t)),
    ('deck', POINTER(deck_t)),
    ('ckt', POINTER(subckt_t)),
    ('eqn_mem', POINTER(None)),
]

spice_t = struct_spice_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 272

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 279
if hasattr(_libs['spiceparser'], 'spice_find_subckt'):
    spice_find_subckt = _libs['spiceparser'].spice_find_subckt
    spice_find_subckt.argtypes = [POINTER(subckt_t), String]
    spice_find_subckt.restype = POINTER(subckt_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 280
if hasattr(_libs['spiceparser'], 'spice_new'):
    spice_new = _libs['spiceparser'].spice_new
    spice_new.argtypes = [POINTER(scanner_t)]
    spice_new.restype = POINTER(spice_t)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 281
if hasattr(_libs['spiceparser'], 'spice_release'):
    spice_release = _libs['spiceparser'].spice_release
    spice_release.argtypes = [POINTER(spice_t)]
    spice_release.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 282
if hasattr(_libs['spiceparser'], 'spice_debug'):
    spice_debug = _libs['spiceparser'].spice_debug
    spice_debug.argtypes = [POINTER(None), POINTER(spice_t)]
    spice_debug.restype = None

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 283
if hasattr(_libs['spiceparser'], 'spice_list_subckt'):
    spice_list_subckt = _libs['spiceparser'].spice_list_subckt
    spice_list_subckt.argtypes = [POINTER(subckt_t)]
    spice_list_subckt.restype = list_t

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 37
try:
    SCAN_FORWARD = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 38
try:
    SCAN_REVERSE = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 39
try:
    SCAN_SET = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 40
try:
    SCAN_CLEAR = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\debug.h: 49
def DEBUG_CMDLINE(c, v, s):
    return (cmdline_read_rc (pointer(c), pointer(v), s))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 51
try:
    LIST_MODECHUNK = 4095
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 52
try:
    LIST_DEFMODE = 16
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 53
try:
    LIST_EXPMODE = 8191
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 54
try:
    LIST_FIXEDMODE = 8192
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 55
try:
    LIST_UNITMODE = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 56
try:
    LIST_USERFLAG1 = 65536
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 57
try:
    LIST_USERFLAG2 = 131072
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 58
try:
    LIST_USERMASK = 16711680
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 59
def list_getuser(l):
    return ((((l.contents.mode).value) & LIST_USERMASK) >> 16)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 68
def list_qty(l):
    return (l.contents.q)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 69
def list_sizeof(l):
    return (l.contents.s)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 61
def hash_bin2user(p):
    return (p + sizeof(hashbin_t))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 62
def hash_user2bin(p):
    return (p - sizeof(hashbin_t))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 64
def hash_malloc(h, s):
    return (hash_alloc (h, (malloc (s))))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 99
def OP_ISEV(a):
    return ((a > OPeolist) and (a < OPeol_qty))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 100
def OP_ISV(a):
    return ((a >= OPlit) and (a <= OPvalm))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 101
def OP_ISEND(a):
    return (a <= OPeol_qty)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 102
def OP_ISANYV(a):
    return ((OP_ISV (a)) or (OP_ISEV (a)))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 106
try:
    eqn_litref_INIT = (-1)
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 138
try:
    EQN_DELIM = "\\'"
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 140
try:
    MAXEQNSTACK = 512
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 161
try:
    MAXSTACK = 512
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 93
def OP_ISEV(a):
    return ((a > OPeolist) and (a < OPeol_qty))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 94
def OP_ISV(a):
    return ((a >= OPlit) and (a <= OPvalm))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 95
def OP_ISEND(a):
    return (a <= OPeol_qty)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 96
def OP_ISANYV(a):
    return ((OP_ISV (a)) or (OP_ISEV (a)))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 128
try:
    EQN_DELIM = "\\'"
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 130
try:
    MAXEQNSTACK = 512
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 146
try:
    MAXSTACK = 512
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 55
def list_search(lp):
    return pointer((lp.contents.list))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 60
def list_search_add(a, b):
    return (list_add ((list_search (a)), b))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 61
def list_search_qty(a):
    return (list_qty ((list_search (a))))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 62
def list_search_index(a, b):
    return (list_index ((list_search (a)), b))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 63
def list_search_reset(a):
    return (list_reset ((list_search (a))))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 28
try:
    MEMORY_CHUNKSIZE = (1024 * 16)
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 29
try:
    MEMORY_THRESHOLD = 16
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 39
try:
    MEMORY_MAGIC = 903848725
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 123
try:
    PARSE_CASE_TOLOWER = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 124
try:
    PARSE_CASE_TOUPPER = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 125
try:
    PARSE_NOCASECVT = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 55
try:
    EXTRACT_MAGIC = 1429296738
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 56
try:
    SPICE_MAGIC = 1130024416
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 101
try:
    TERMPTR_BITS_DEVI = 24
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 102
try:
    TERMPTR_BITS_TERMI = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 103
try:
    TERMPTR_BITS_DEVT = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 113
try:
    TERMPTR_MAX_DEVI = ((1 << TERMPTR_BITS_DEVI) - 1)
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 114
try:
    TERMPTR_MAX_TERMI = ((1 << TERMPTR_BITS_TERMI) - 1)
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 115
try:
    TERMPTR_MAX_DEVT = ((1 << TERMPTR_BITS_DEVT) - 1)
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 116
def netlist_termptr_isnull(t):
    return (((t.nonnull).value) == 0)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 151
def NETLIST_OFFSET_PARENT(e):
    return 0

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 155
def NETLIST_OFFSET_TERMS(e):
    return (sizeof(dev_input_t) + ((NETLIST_OFFSET_PARENT (e)).value))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 161
def NETLIST_OFFSET_VALS(e):
    return (((NETLIST_OFFSET_TERMS (e)).value) + (((e.qterms).value) * sizeof(termptr_t)))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 166
def NETLIST_OFFSET_REST(e):
    return (((NETLIST_OFFSET_VALS (e)).value) + (sizeof(eqn_t) * ((e.qvals).value)))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 169
def NETLIST_OFFSET_OTHER(e):
    return (((NETLIST_OFFSET_REST (e)).value) + ((e.qother).value))

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 172
def NETLIST_E_QTERMS(e):
    return (e.contents.qterms)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 173
def NETLIST_QTERMS(nl, t):
    return (((nl.contents.e) [t]).qterms)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 174
def NETLIST_E_QVALS(e):
    return (e.contents.qvals)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 175
def NETLIST_QVALS(nl, t):
    return (((nl.contents.e) [t]).qvals)

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 177
try:
    DEVT_NODE = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 179
try:
    DEVT_NODE_TERMS = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 30
try:
    DEVNODE_HEAD = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 31
try:
    DEVNODE_TAIL = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 33
try:
    DEVFET_S = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 34
try:
    DEVFET_D = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 35
try:
    DEVFET_G = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 36
try:
    DEVFET_B = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 37
try:
    DEVFET_w = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 38
try:
    DEVFET_l = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 39
try:
    DEVFET_as = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 40
try:
    DEVFET_ad = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 41
try:
    DEVFET_ps = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 42
try:
    DEVFET_pd = 5
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 43
try:
    DEVFET_V = 6
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 45
try:
    DEV2TERM_P = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 46
try:
    DEV2TERM_N = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 48
try:
    DEVCAP_c = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 49
try:
    DEVCAP_V = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 51
try:
    DEVRES_r = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 52
try:
    DEVRES_V = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 55
try:
    DEVT_FET = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 56
try:
    DEVT_CAP = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 57
try:
    DEVT_RES = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 58
try:
    DEVT_IND = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 59
try:
    DEVT_DIODE = 5
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 60
try:
    DEVT_VSRC = 6
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 61
try:
    DEVT_ISRC = 7
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 62
try:
    DEVT_BJT = 8
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 63
try:
    DEVT_MAX = 9
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 80
try:
    DEVGEN_V = 8
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 89
try:
    DEVFET_nmos = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 90
try:
    DEVFET_pmos = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 37
try:
    NLIBIO_MAXNODES = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 99
try:
    MAXSKEW_PARAMS = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 144
try:
    NLIB_MAXPHASES = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 159
try:
    NLIB_MAXFREF = 64
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 48
try:
    PAYLOAD_null = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 49
try:
    PAYLOAD_card_val = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 50
try:
    PAYLOAD_parent = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 51
try:
    PAYLOAD_gnptr = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 52
try:
    PAYLOAD_subckt = 4
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 53
try:
    PAYLOAD_node = 5
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 167
try:
    INDEX_GATE = 1
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 168
try:
    INDEX_DRAIN = 0
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 169
try:
    INDEX_SOURCE = 2
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 170
try:
    INDEX_BULK = 3
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 221
try:
    SUBCKT_MAGIC = 1126393107
except:
    pass

# c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 276
def minimum(a, b):
    return (a < b) and a or b

bitlist_st = struct_bitlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\bitlist.h: 35

list_st = struct_list_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 40

listx_st = struct_listx_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 47

sort_func_st = struct_sort_func_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/list.h: 123

names_st = struct_names_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/names.h: 50

hashbin_st = struct_hashbin_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 43

hash_st = struct_hash_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 59

hash_ptrflagstr_st = struct_hash_ptrflagstr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/hash.h: 94

eqntokenlit_st = struct_eqntokenlit_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 113

eqntokenval_st = struct_eqntokenval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 119

eqntokenpval_st = struct_eqntokenpval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 124

lit_val_un = union_lit_val_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 129

eqntoken_st = struct_eqntoken_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 135

eqntop_st = struct_eqntop_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 151

plookup_st = struct_plookup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 155

eqneval_st = struct_eqneval_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 168

eqn_st = struct_eqn_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 178

eqnlist_st = struct_eqnlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eqn.h: 218

eqndef_st = struct_eqndef_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\equations.h: 167

eval_expr_st = struct_eval_expr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\eval.h: 62

list_psearch_st = struct_list_psearch_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 40

list_search_st = struct_list_search_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 46

list_search_iterator_st = struct_list_search_iterator_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\list_search.h: 53

memory_chain_st = struct_memory_chain_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 31

memory_other_st = struct_memory_other_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 41

memory_head_st = struct_memory_head_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\memory.h: 50

sortlist_st = struct_sortlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 29

mergedup_st = struct_mergedup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\mergedup.h: 43

file_line_st = struct_file_line_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 48

tokenmap_st = struct_tokenmap_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 54

card_st = struct_card_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 57

deck_st = struct_deck_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 65

scanner_def_st = struct_scanner_def_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 86

scanner_sect_st = struct_scanner_sect_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 88

scanner_input_st = struct_scanner_input_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 102

scanner_st = struct_scanner_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\/scanner.h: 110

extract_st = struct_extract_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_extract.h: 30

spice_st = struct_spice_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 265

geninput_st = struct_geninput_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 63

netlist_input_un = union_netlist_input_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 73

m_st = struct_m_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 172

c_st = struct_c_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 181

dev_input_un = union_dev_input_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 84

termptr_st = struct_termptr_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 111

entity_st = struct_entity_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 142

devnode_st = struct_devnode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 185

netlist_st = struct_netlist_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 197

netlistfunc_st = struct_netlistfunc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 203

netlist_param_st = struct_netlist_param_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist.h: 223

devgen_st = struct_devgen_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 87

devfet_st = struct_devfet_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 98

devcap_st = struct_devcap_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 106

devres_st = struct_devres_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 114

devind_st = struct_devind_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 122

devvsrc_st = struct_devvsrc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 130

devisrc_st = struct_devisrc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 138

devdiode_st = struct_devdiode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 146

devbjt_st = struct_devbjt_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 154

dev2term_st = struct_dev2term_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 161

dev4term_st = struct_dev4term_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 168

devall_un = union_devall_un # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_dev.h: 181

nlibiodef_st = struct_nlibiodef_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 46

nlibio_st = struct_nlibio_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 56

nlibiol_st = struct_nlibiol_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 62

nlibpm_st = struct_nlibpm_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 70

nlibfunc_st = struct_nlibfunc_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 80

nlibfref_st = struct_nlibfref_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 86

nlibrefnode_st = struct_nlibrefnode_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 105

nlibdb_st = struct_nlibdb_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 116

nlibflatdb_st = struct_nlibflatdb_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 126

nlib_st = struct_nlib_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 142

nlib_icall_st = struct_nlib_icall_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 157

nlib_ifref_st = struct_nlib_ifref_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 165

nlib_iface_st = struct_nlib_iface_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 185

nlib_process_st = struct_nlib_process_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_lib.h: 232

subckt_st = struct_subckt_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 223

paydata_u = union_paydata_u # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 71

hashload_st = struct_hashload_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 83

nodeclient_st = struct_nodeclient_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 89

callparam_st = struct_callparam_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 117

paramload_st = struct_paramload_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 101

paramclient_st = struct_paramclient_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 108

stack_st = struct_stack_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 254

paramlookup_st = struct_paramlookup_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 114

x_st = struct_x_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 165

r_st = struct_r_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 195

l_st = struct_l_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 203

v_st = struct_v_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 211

i_st = struct_i_st # c:\\Users\\satya\\src\\xcircuit-3.8\\spiceparser\\netlist_spice.h: 219

# No inserted files

