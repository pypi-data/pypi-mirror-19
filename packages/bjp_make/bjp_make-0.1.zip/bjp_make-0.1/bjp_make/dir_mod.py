#! /usr/bin/env python

import os

def clear_dirs(*args):
    """Delete all files in existing directories while keeping the 
    directory structure (i.e. sub-directories). Create a directory 
    for each argument if they do not already exist."""
    for dir in args:
        if os.path.isdir(dir):
            subdirs = [x[1] for x in os.walk(dir)][0]
            files = [x[2] for x in os.walk(dir)][0]
            for f in files:
                os.remove(dir+'/'+f)
            for subdir in subdirs:
                clear_dirs(dir+"/"+subdir)
        else:
            os.makedirs(dir)
        print 'Cleared:', dir		