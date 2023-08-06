PyCAPO is an implementation of SSA CAPO (CASA, Archive, and Pipeline Options)
in Python. It is shipped as a library with a simple API and a command line
utility that calls the library and produces results suitable for use in a shell
script, enabling us to make quick CAPO enabled scripts.

CAPO is a configuration system that reads values from multiple property files,
these files are delimited by the combination of two options to it, CAPO_PATH
and CAPO_PROFILE:

CAPO_PATH is a colon delimited list of directories to search for property files,
like '/home/casa/capo:/home/ssa/capo:/etc/capo'. The same property can be read
from multiple files, and in this case the later property replaces the earlier
property. CAPO_PATH can be given as an argument to the library or CLI app, or
PyCAPO will look for a CAPO_PATH environment variable. If those two are missing
PyCAPO defaults to '/home/casa/capo:/home/ssa/capo:$HOME/.capo'. PyCAPO skips
over missing or unreadable property files (this is intentional).

CAPO_PROFILE describes the profile PyCAPO looks for, e.g. 'test', 'staging',
'production', and PyCAPO expects the property files on the CAPO_PATH it looks
for to be named $profile.properties, e.g., /home/casa/capo/test.properties.
CAPO_PROFILE can be an argument to the library or CLI app, or PyCAPO will look
for a CAPO_PROFILE environment variable. If both of those are missing PyCAPO
will complain and die (this is also intentional).

CAPO isn't yet robust against things like profiles with spaces in their name,
and it has only been tested under Linux and MacOS.
