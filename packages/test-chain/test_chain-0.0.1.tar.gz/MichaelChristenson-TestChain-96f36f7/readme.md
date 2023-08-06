#### Test Chaining
------------------

Unit testing is a key part of software development that allows for
automatic discernment of bugs and glitches in code. The central function
of this project, named skip_if_already_done, allows a streamlined
approach to testing by only throwing an exception for that test if it
were that test which  generated the exception, rather than a test that
the test itself runs.


Usage
-----
- First, one must install test_chain
- Have the testing class extend TestChain

The testChainMeta metaclass houses a function to asssist in unit testing
and a metaclass to apply that function automatically to all relevant
functions within any class that extends it. The @skip_if_already_done
function checks if a downstream function has failed and reports its
failing, rather than claiming that it itself has failed.