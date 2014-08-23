GitHub Data Challenge 2014 Entry
================================

**Theme: Quest for True Names**

Challenge page:
https://github.com/blog/1864-third-annual-github-data-challenge

Key Findings
------------

 * What are typical words used for variable names and function names? **Answer: we got a list.**
 * Are they different in different languages? **Answer: Yes, they are!**
 * We can assume nouns are commonly used for variables, and verbs for functions.
   Is there an interesting connection between them? **Answer: Yes, there is!**

Method
------

 * Examine source code in three major languages: C, Java and Python.
 * List the names for variables, functions (methods) and types (classes).
 * Count common words from each list, and see if an interesting statistics emerges.

Data We Used
------------

 * Pick the top 100 repositories (in terms of Stars) that are labelled as each language.
   (via GitHub Search API, cf. https://developer.github.com/v3/search/)
   [Obtained at Aug. 8, 2014]
 * List all the files: (Caveats: We excluded non-ASCII filenames.)
   * C: 110,705 files (including header files)
   * Java: 94,635 files
   * Python: 33,710 files
 * Randomly pick files for each language that has reasonable file size. (1KB-100KB)
   * C: 7,381 files (80MB in total)
   * Java: 7,764 files (53MB in total)
   * Python: 5,872 files (56MB in total)
 * In order to mitigate the data skewness, 
   we limited the maximum number of files for each repository to 100.

Language Parsing
----------------

 * We used ANTLR4 for C and Java (cf. http://antlr.org), 
   and ast module for Python (cf. https://docs.python.org/2/library/ast.html).
 * C Caveats: ANTLR4 cannot handle preprocessor directives,
   so we stripped out #defines and #includes from the code.
   After all, we're interested in a source code for human readers, not for compilers.
   But this left a certain number of non-syntactic C codes.
   (e.g. `int func(void *p, EXTRA_ARGS);` )
 * Python Caveats: Mixture of Python 2 and 3 code. 
   The compiler.ast module handles both pretty well.
 * The following names were excluded: one-letter names, "assert" as a function name, and
   "self" as a variable name (in Python).
