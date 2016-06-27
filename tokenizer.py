#!/usr/bin/env python

from inputstream import *

class Token:
    """class for tokens"""
    def __init__(self,ttype,value):
        self.ttype = ttype
        self.value = value
    def __str__(self):
        return "{type: " + self.ttype + " , value: " + str(self.value) + "}"

class TokenStream():
    def __init__(self,inputStream):#inputStream should be an InputStream
        self.inputStream = inputStream
        self.current = False
        self.keywords = ['if','then','else', 'lambda', 'true', 'false', 'while']
    
    def read_next(self):
        while(True):
            self.read_while(self.is_whitespace)
            if(self.inputStream.eof()):
                return False
            ch = self.inputStream.peek()
            if(ch == '#'):
                self.skip_comment()
                continue
            break
        if(ch in "\"'"):
            return self.read_string()
        if(ch in "0123456789"):
            return self.read_number()
        if(self.is_id_start(ch)):
            return self.read_ident()
        if(self.is_punc(ch)):
            return Token("punc",self.inputStream.next())
        if(self.is_op_char(ch)):
            return Token("op",self.read_while(self.is_op_char))
        self.inputStream.croak("Can't handle character: " + ch)
 
    def is_keyword(self,x):
        return x in self.keywords
    def is_id_start(self,ch):
        return (ch.isalpha() or (ch =='_'))
    def is_id(self,ch):
        return (ch.isalnum() or (ch in "?!-<>=~"))
    def is_op_char(self,ch):
        return ch in "+-*/%=&|<>!"
    def is_punc(self,ch):
        return ch in ",;(){}[]"
    def is_whitespace(self,ch):
        return (ch in " \t\n\r")
    

    def read_while(self,predicate):
        outstr = ""
        while((not self.inputStream.eof()) and predicate(self.inputStream.peek())):
            outstr += self.inputStream.next()
        return outstr

    def read_number(self):
        numberStr = ""
        numberStr += self.read_while(lambda ch: ch.isdigit())
        if(self.inputStream.peek() == '.'):
            numberStr += self.inputStream.next()
            numberStr += self.read_while(lambda ch: ch.isdigit())
            return Token("numf",float(numberStr))
        else:
            return Token("num",int(numberStr))
    
    def read_ident(self):
        strId = self.read_while(self.is_id)
        if(self.is_keyword(strId)):
            return Token("kw",strId)
        else:
            return Token("var",strId)
    
    def read_escaped(self,end):
        escaped = False
        outstr = ""
        self.inputStream.next()
        while(not self.inputStream.eof()):
            ch = self.inputStream.next()
            if(escaped):
                outstr += ch
                escaped = False
            elif(ch == "\\"):
                escaped = True
            elif(ch == end):
                break
            else:
                outstr += ch
        return outstr

    def read_string(self):
        return Token("str",self.read_escaped('"'))

    def skip_comment(self):
        self.read_while(lambda ch: (ch != "\n"))
        self.inputStream.next()

    def peek(self):
        if(self.current == False):
            self.current = self.read_next()
        return self.current

    def croak(self,msg):
      return self.inputStream.croak(msg)    

    def next(self):
        token = self.current
        self.current = False
        if(token == False):
            token = self.read_next()
        return token
 
    def eof(self):
        return (False == self.peek())

#end of class definition
