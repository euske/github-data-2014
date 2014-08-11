GitHub Data Challenge 2014 Entry
================================

https://github.com/blog/1864-third-annual-github-data-challenge

Data We Used
------------

 * Pick the top 100 repositories (in terms of Stars) that are labelled as: C, Java and Python.
   (via GitHub Search API, cf. https://developer.github.com/v3/search/)
   [Obtained at Aug. 8, 2014]
 * List all the files: (Caveats: We excluded non-ASCII filenames.)
   * C: 94637 files
   * Java: 33756 files
   * Python: 57807 files
 * Randomly pick 10000 files for each language that has reasonable file size. (1KB-100KB)
   * C: 153MB in total
   * Java: 57MB in total
   * Python: 95MB in total

Data Skewness
-------------

 * Many files in C are from the Linux kernel.
   (3611 files from torvalds/linux, 3336 files from raspberrypi/linux)
 * Many files in Java are from JetBrains IntelliJ.
   (3599 files from JetBrains/intellij-community)
 * Many files in Python are from Appscale.
   (2417 files from AppScale/appscale)

Language Parsing
----------------

 * We used ANTLR4 for C and Java (cf. http://antlr.org), 
   and ast module for Python (cf. https://docs.python.org/2/library/ast.html).
 * C Caveats: ANTLR4 cannot handle preprocessor directives,
   so we stripped out #defines and #includes from the code.
   After all, we're interested in a source code for human readers, not for compilers.
 * Python Caveats: Mixture of Python 2 and 3 code.
