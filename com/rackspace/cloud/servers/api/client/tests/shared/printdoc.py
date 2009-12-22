# Copyright (c) 2009, Rackspace.
# See COPYING for details.

"""
printdoc decorator, prints module's docstring (used for tests)
"""
from sys import stdout

def printdoc(f):
    """
    printdoc decorator, prints out func's docstring, returns unmodified func
    """
    if f.__doc__:
        stdout.write('\n')

        testname = "[ %s ]" % f.__name__
        testname = testname.center(74) + '\n'
        stdout.write(testname)

        stdout.write('  ' + (74 * "~") + '\n')

        words = list()
        for l in f.__doc__.splitlines(): words += l.split()

        lines = list()
        buff = ' '

        for word in words:
            if (len(buff) + len(word)) >= 78:
                lines.append(buff)
                buff = ' '
            buff += ' %s' % word
        lines.append(buff)

        stdout.write('\n'.join(lines))
        stdout.write('\n')
        stdout.write('  ' + (74 * "~") + '\n')
    else:
        print "%s: No docstring found!" % f.__name__
    return f

# vim:set ai sw=4 ts=4 tw=0 expandtab:
