#!/usr/bin/env python

import sys
import parser
import enviroment
import evaluate

env = enviroment.Enviroment()

def println(aaa):
  print(aaa)
env.defi("println",println)
env.defi("print",println)

if(len(sys.argv) < 2):
  print("REPL.\ntype exit to exit")
  sourcecode = raw_input("==>")
  while(sourcecode != "exit"):
    print(evaluate.evaluate(parser.parse(parser.TokenStream(parser.InputStream(sourcecode))),env))
    sourcecode = raw_input("==>")
else:
  with open(sys.argv[1]) as input_file:
    sourcecode = input_file.read()
  evaluate.evaluate(parser.parse(parser.TokenStream(parser.InputStream(sourcecode))),env)
