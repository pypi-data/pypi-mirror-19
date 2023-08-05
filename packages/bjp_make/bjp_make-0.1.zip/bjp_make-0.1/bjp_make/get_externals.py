#! /usr/bin/env python

import imp
import re

from private.getexternaldirectives import CopyDirective

######################################################
# Main Program
######################################################

def get_externals(externals_file, external_dir = '@DEFAULTVALUE@'):

    externals = input_to_array(externals_file)

    for line in externals:
        directive = CopyDirective(line)
        #directive.error_check()
        directive.clean(external_dir)
        directive.issue_sys_command()


######################################################
# Supporting functions
######################################################
        
def input_to_array(filename):
    """ Import a file and send lines to array"""
    filearray = []
    FILENAME = open(filename, 'rU')
    for line in FILENAME:
        # remove header rows
        if ( not re.match('rev', line) 
             and not re.match('linkpath', line)
             and not re.match('\s*\#',line) 
             and not re.match('\s*$',line) 
             and not re.match('url', line)):
            filearray.append(line.rstrip('\n'))
    FILENAME.close()
    
    return filearray

