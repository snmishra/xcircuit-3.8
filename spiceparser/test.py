from spiceparser import scanner_t, scanner_init, scanner_input_newfp
from spiceparser import spice_new, spice_list_subckt, spice_release
import ctypes
from ctypes import byref
libc = ctypes.cdll.msvcrt
scan = scanner_t()
scanner_init(byref(scan))
fp = libc.fopen('../../test.sp', 'r')
scanner_input_newfp(byref(scan), fp)
spice = spice_new(byref(scan))
subckts = spice_list_subckt(spice.contents.ckt)
spice_release(spice);
