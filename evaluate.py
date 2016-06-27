#!/usr/bin/env python

def evaluate(exp, env):
  if(exp.ntype in ("num", "str", "bool")):
    return exp.value
  if(exp.ntype == "var"):
    return env.get(exp.value)
  if(exp.ntype == "assign"):
    if(exp.left.ntype != "var"):
      raise ValueError("Cannot assign to " + str(exp.left))
    return env.set(exp.left.value, evaluate(exp.right,env))
  if(exp.ntype == "binary"):
    return apply_op(exp.op, evaluate(exp.left,env),evaluate(exp.right,env))
  if(exp.ntype == "lambda"):
    return make_lambda(env,exp)
  if(exp.ntype == "if"):
    cond = evaluate(exp.cond,env)
    if(cond != False):
      return evaluate(exp.then,env)
    if(exp.els):
      return evaluate(exp.els,env)
    return False
  if(exp.ntype == "prog"):
    val = False
    for subexp in exp.prog:
      val = evaluate(subexp,env)
    return val
  if(exp.ntype =="call"):
    func = evaluate(exp.func,env)
    evaledArgs = [evaluate(arg,env) for arg in exp.args]
    return func(*evaledArgs)
  
  raise ValueError("I don't know how to evaluate " + exp.ntype)

operationsFunctions = {
'+':(lambda a,b:a+b),
'-':(lambda a,b:a-b),
'*':(lambda a,b:a*b),
'/':(lambda a,b:a/b),
'%':(lambda a,b:a%b),
'&&':(lambda a,b:a and b),
'||':(lambda a,b:a or b),
'<':(lambda a,b:a < b),
'<=':(lambda a,b:a <= b),
'>':(lambda a,b:a > b),
'>=':(lambda a,b:a >= b),
'==':(lambda a,b:a == b),
'!=':(lambda a,b:a != b),
}

def apply_op(op,a,b):
  if(op in operationsFunctions):
    return (operationsFunctions[op])(a,b)
  else:
    raise ValueError("Undefined operator: " + str(op) )

def make_lambda(env,exp):
  def l(*args):
    names = exp.vars
    scope = env.extend()
    for i in range(len(names)):
      if(i < len(args)):
        scope.defi(names[i],args[i])
      else:
        print("Warning: not enough arguments!")
        scope.defi(names[i],False)
    return evaluate(exp.body, scope)
  return l
