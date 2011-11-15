#!/usr/bin/env python
import spiceparser
from ctypes import byref

class Scanner:
    def __init__(self):
        self.scanner = spiceparser.scan_t()
        spiceparser.scanner_init(byref(self.scanner))

class Spice:
    def __init__(self, scanner):
        self.spice = spiceparser.spice_new(byref(scanner.scanner))
    def generate_asg(self):
        spiceparser.generate_asg(self.spice)
    def __del__(self):
        spiceparser.spice_release(self.spice)
