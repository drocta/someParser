#!/usr/bin/env python

class InputStreamError(Exception):
    """Class for errors for InputStream"""
    pass

class InputStream:
    def __init__(self,instring):
        self.instring = instring
        self.pos, self.line, self.col = 0,1,0
        self.leng = len(instring)

    def next(self):
        if(self.eof()):
          return ""
        ch = self.instring[self.pos]
        self.pos += 1
        if(ch == "\n"):
            self.line += 1
            self.col = 0
        else:
            self.col += 1
        return ch

    def peek(self):
        if(self.eof()):
            return ""
        return self.instring[self.pos]

    def eof(self):
        return self.pos >= self.leng

    def croak(self, msg):
        raise InputStreamError(msg + " (" + str(self.line) + ":" + str(self.col) + ")")
