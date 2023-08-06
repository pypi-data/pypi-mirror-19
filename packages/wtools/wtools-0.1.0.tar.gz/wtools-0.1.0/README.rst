Summary
-------
This package contains a collection of tools for the waf_ build environment
intended for both native- as well cross compilation of C/C++ based projects.

Following provides a non-exhausting list of functions provided:

- C/C++ setup cross-compile toolchains (**wtools.wcc**)
- C/C++ export to makefiles (**wtools.wmake**)
- C/C++ export to Eclipse (**wtools.weclipse**)
- C/C++ code formatting (**wtools.indent**)


Installation
------------
The *wtools* package can be installed using pip::

    pip install -I wtools [--user]

As alternative you can also clone the repository and install the latest
revision::

    cd ~
    git clone https://bitbucket.org/Moo7/wtools.git wtools
    pip install -e ~/wtools [--user]


Support
-------
If you have any suggestions for improvements and/or enhancements, please feel 
free to drop me a note by creating an issue_ at the wtools_ projects 
page.


.. _waf: https://waf.io
.. _wafbook: https://waf.io/book/
.. _issue: https://bitbucket.org/Moo7/wtools/issues
.. _wtools: https://bitbucket.org/Moo7/wtools

