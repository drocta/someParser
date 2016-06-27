#!/usr/bin/env python

class Environment:
  def __init__(self, parent = None):
    self.parent = parent
    if(parent != None):
      self.vars = parent.vars.copy()
    else:
      self.vars = {}
  
  def extend(self):
    return Environment(self)
  
  def lookup(self, name): #get scope for name
    #this will need to be drastically changed for [redacted], but
    #doing it like [lambda]anguage for now
    if(name not in self.vars):
      return False
    if(self.parent != None):
      a = self.parent.lookup(name)
    else:
      a = False
    if(a == False):
      a = self
    return a
  
  def get(self,name):
    if(name in self.vars):
      return self.vars[name]
    raise ValueError("Undefined variable: " + name)
  
  def set(self, name, value):
    scope = self.lookup(name)
    if((not scope) and (self.parent != None)):
      raise ValueError("Undefined variable: " + name)
    if(not scope):
      scope = self
    scope.vars[name] = value
    return scope.vars[name]
  
  def defi(self, name, value):
    self.vars[name] = value
    return self.vars[name]
