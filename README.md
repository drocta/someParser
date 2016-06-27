# someParser
This is based on http://lisperator.net/pltut/ (which is in turn based on https://github.com/marijnh/parse-js ) but it is in python instead of js (instead of lisp), and other things are different.

Whatever licencing that I am obligated to apply to this because of this being partially based on that applies.

However, its in a different programming language, and most of it will be changed, so I don't know how much that is.

This is some parser. Or, rather, now it also includes an interpreter, which works both interactively and with a file . My intent is to use it for another thing later. (it is a sekret to everyone).

My previous tokenizing things have been sloppy, which is why I am trying to do it right, instead of using my old tokenizing stuff.

I'm not 100% sure that I'm able to grant you license to this, because I couldn't find a license on http://lisperator.net/pltut/ , and this is at least so far mainly a translation of that to python.

So, take caution with regards to that.

Assuming I can, I will probably eventually release this under some version of the gpl.

# Use

To use this in its current state, run combined.py. To use it in interactive mode, just run combined.py . To use it to run another program, put the program filename (including path if neccesary) as the command line argument.

If you want to make a file run with this on a unixlike os, that works with the hashbang thing
have the first line of the program be #! followed by something that gives where combined.py is, and then you should be able to run the program by just running it. Like, just typing in ./example1.howl for example. Look at example1.howl to see what I mean.
