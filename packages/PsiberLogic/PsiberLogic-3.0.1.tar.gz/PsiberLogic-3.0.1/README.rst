PsiberLogic is a fuzzy control package for Python 3.  Version 3.x removes the pre-compiled
cython files, due to the need for the user to utilize the same version of dependencies.  As such,
this version is much simpler to utilize, but does require compilation upon installation.
MSVS 2015 is recommended for compilation, but others can be utilized with minor edits to
"compile.py".

After installation, simply import PsiberLogic as PL and call PL.compile().

This software is a simplified, Cythonized, and compacted package that is a derivative work of Jose
Alexandre Nalon's excellent Peach package.  This was done for increases in computational efficiency
as well as to maintain the work by updating to Python 3.  This package is for anyone seeking a
high-performance, python3-callable package for creating fuzzy logic controllers.  PsiberLogic has
almost no checks for errors; if the format provided in the demo file is not followed correctly
errors could be present that will not be reported.

Note that additional types of membership functions and defuzzification methods may be added
later, and additional speed optimizations are in development.  This has currently only been
tested for windows machines, but could work fine on OS X / Linux. Please feel free to
suggest improvements, send feedback, or inform the author of any bugs. (contact@psibernetix.com)

This package is licensed under the LGPL (see LICENSE.txt), and all distributions or derivative
works of PsiberLogic must be as well.

Created by:  Dr. Nick Ernest, Psibernetix Inc. CEO

Current Version: 3.0.1