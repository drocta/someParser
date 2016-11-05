#!/usr/bin/env python

from tokenizer import *

class astNode:
  def __init__(self, ntype, **kwargs):
    self.ntype = ntype
    self.kwargs = kwargs
    if 'value' in kwargs:
      self.value = kwargs['value']
    else:
      self.value = None
    if 'vars' in kwargs:
      self.vars = kwargs['vars']
    else:
      self.vars = None
    if('body' in kwargs):
      self.body = kwargs['body']
    else:
      self.body = None
    if('func' in kwargs):
      self.func = kwargs['func']
    else:
      self.func = None
    if('args' in kwargs):
      self.args = kwargs['args']
    else:
      self.args = None
    if('cond' in kwargs):
      self.cond = kwargs['cond']
    else:
      self.cond = None
    if('then' in kwargs):
      self.then = kwargs['then']
    else:
      self.then = None
    if('else' in kwargs):
      self.els = kwargs['else']
    else:
      self.els = None
    if('op' in kwargs):
      self.op = kwargs['op']
    else:
      self.op = None
    if('left' in kwargs):
      self.left = kwargs['left']
    else:
      self.left = None
    if('right' in kwargs):
      self.right = kwargs['right']
    else:
      self.right = None
    if('prog' in kwargs):
      self.prog = kwargs['prog']
    else:
      self.prog = None
  
  def __str__(self):
    return "{type: " + self.ntype + ", " + (','.join([key+":"+str(self.kwargs[key]) for key in self.kwargs])) + "}"
  
  def __repr__(self):
    return self.__str__()


def parse(tokenStream):
  precedence={
    '=':1,
    '||':2,
    '&&':3, '->':3,
    '<':7,  ">": 7, "<=": 7, ">=": 7, "==": 7, "!=": 7,
    "+": 10, "-": 10,
    "*": 20, "/": 20, "%": 20 }
  def is_z(ttype, val = False):
    tok = tokenStream.peek()
    if(tok and (tok.ttype == ttype) and ((not val) or (tok.value == val))):
      return tok
    else:
      return False

  def is_punc(ch = False):
    return is_z("punc",ch)
  def is_kw(kw = False):
    return is_z("kw",kw)
  def is_op(op = False):
    return is_z("op",op)

  def skip_z(ttype,val = False):
    ttypeLongname = {"op":"Operation", "kw":"Keyword", "punc":"Punctuation"}
    if(is_z(ttype,val)):
      tokenStream.next()
    else:
      tokenStream.croak("Expecting " + ttypeLongname[ttype] + '"' + val + '"')
  
  def skip_punc(ch = False):
    skip_z("punc", ch)
  def skip_kw(kw = False):
    skip_z("kw", kw)
  def skip_op(op = False):
    skip_z("op", op)

  def unexpected():
    tokenStream.croak("Unexpected token: " + str(tokenStream.peek()))
  
  def maybe_binary(mleft, my_prec): #prec stands for precedence
    tok = is_op() # is any sort of operator thingy
    if(tok): #if it is
      if(tok.value in precedence):
        its_prec = precedence[tok.value]
      else:
        its_prec = -20 #non built in operators have precedence -20 so that they are lower than everything built in
      if(its_prec > my_prec):
        tokenStream.next()
        ntype = "binary"
        if(tok.value == "="):
          ntype = "assign"
        mright = maybe_binary(parse_atom(), its_prec)
        node = astNode(ntype, op = tok.value, left = mleft, right = mright)
        return maybe_binary(node, my_prec)
    return mleft
  
  def delimited(start,stop,separator, parser):
    a = []
    first = True
    skip_punc(start) # ensures that the start punctuation is there, and then eats it.
    while(not tokenStream.eof()):
      if(is_punc(stop)):
        break
      if(first):
        first = False
      else:
        skip_punc(separator)
      if(is_punc(stop)): 
        break
      a.append(parser()) #parse the next thing in whatever is the appropriate way, and add it to the list
    skip_punc(stop) # ensures that the stop punc is there, and then eats it.
    return a # the list of things that were parsed.
  
  def parse_call(mfunc):
    return astNode("call",func = mfunc, args = delimited("(",")",",", parse_expression))

  def parse_varname():
    name = tokenStream.next()
    if(name.ttype != "var"):
      tokenStream.croak("Expecting variable name")
    return name.value
  
  def parse_if():
    skip_kw("if")
    mcond = parse_expression()
    if(not is_punc("{")):
      skip_kw("then")
    mthen = parse_expression()
    ret = astNode("if",cond = mcond, then = mthen)
    if(is_kw("else")):
      tokenStream.next()
      ret.els = parse_expression()
      ret.kwargs['else'] = ret.els
    return ret
  
  def parse_lambda():
    return astNode("lambda", vars = delimited("(",")",",", parse_varname), body = parse_expression())
  
  def parse_bool():
    return astNode("bool", value = ( tokenStream.next().value == "true"))

  def maybe_call(exprFunction): # evaluates argument, and then, if applicable, calls it as a function.
    exprResult = exprFunction() #this might not work right. Might need to adjust this for python
    if(is_punc("(")):
      return parse_call(exprResult)
    else:
      return exprResult
  
  def parse_atom():
    def f(): # this is too long for a lambda
      if(is_punc("(")):#for parens for grouping (I think.)
        tokenStream.next()
        exp = parse_expression()
        skip_punc(")")
        return exp
      if(is_punc("{")):
        return parse_prog()
      if(is_kw("if")):
        return parse_if()
      if(is_kw("true") or is_kw("false")):
        return parse_bool()
      if(is_kw("lambda")):
        tokenStream.next()
        return parse_lambda()
      tok = tokenStream.next()
      if(tok.ttype in ("var","num", "str")):
        return astNode(tok.ttype, value = tok.value)
      unexpected()
    return maybe_call(f)

  def parse_toplevel():
    prog = []
    while(not tokenStream.eof()):
      prog.append(parse_expression())
      if(not tokenStream.eof()):
        skip_z("punc",";")
    return astNode("prog", prog = prog)

  def parse_prog():
    mprog = delimited("{","}",";", parse_expression);
    if(len(mprog) == 0):
      return False
    if(len(mprog) == 1):
      return mprog[0]
    return astNode("prog", prog = mprog)

  def parse_expression():
    return maybe_call(lambda: maybe_binary(parse_atom(),0))

  return parse_toplevel()
