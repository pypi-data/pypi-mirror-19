==============
 indexedlines
==============

Copyright (c) 2016 Luís Gomes


``indexedlines`` implements a list-like immutable view over lines of text files.
In other words, it allows access to any line given it's zero-based index.
Thus, if you have a big text file and you want to get line number 100001, you
don't have to read the first 100000 sentences before getting that one.

Of course there are no free lunches, and this module needs to compute a list
of sentence offsets beforehand (which is saved to disk when a indexedlines
object is created for the first time).
