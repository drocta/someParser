#!/usr/bin/env python

"""unimportant temporary testing file"""

from tokenizer import *

teststring="""
if
bobcat-123-bobcat
1,2,"nidoking"
9999999999999999999999999999999999999999999&bob

"""

instream = InputStream(teststring)

tokstream = TokenStream(instream)

for i in range(10):
    print(tokstream.next())
