#! /usr/bin/env python

import os
import re
import shutil
import fileinput
import imp

from private.runprogramdirective import RunProgramDirective, RunCommandDirective
import private.metadata 

def run_stata(**kwargs):
    """Run Stata program [with log file].
    inputs: program, [executable, option, changedir]
    
    program = .do file
    executable = Stata version to use (defualt = 'stata-mp')
    option = Stata command line options (default = '-e')
    changedir = boolean for requirement to execute do file from its own directory
    """

    run = RunProgramDirective(kwargs)
   
    run.error_check('stata')

    # get program
    if run.changedir:
        program = '"' + run.program + '"'
    else:
        program = '"' + run.program_full + '"'
    
    # get executable
    executable = run.executable
    if not executable:
        if run.osname == 'posix':
            executable = metadata.default_executables['stataunix']
        else:
            executable = metadata.default_executables['statawin']
 
    # get option    
    option = run.option
    if not option:
        if run.osname == 'posix':
            option = metadata.default_options['stataunix']
        else:
            option = metadata.default_options['statawin']
            
    command = metadata.commands['stata'] % (executable, option, program) 
    run.execute_run(command)

def run_python(**kwargs):
    """Run Python program.
    inputs: program, [executable, option, args, changedir]
    
    program = .py file
    executable = (defualt = 'python')
    option = Python execution options (default = '')
    args = arguments for 'program'
    changedir = boolean for requirement to execute do file from its own directory
    """

    run = RunProgramDirective(kwargs)

    run.error_check('python')

    # get program
    if run.changedir:
        program = '"' + run.program + '"'
    else:
        program = '"' + run.program_full + '"'

    # get executable
    executable = run.executable
    if not run.executable:
        executable = metadata.default_executables['python']

    command = metadata.commands['python'] % (executable, run.option, program, run.args)

    run.execute_run(command)

def run_lyx(**kwargs):
    """Run Lyx export to PDF; handouts and comments options.
    inputs: program, [executable, option, changedir, handout, comments, pdfout]

    program = .lyx file
    executable = (default = 'lyx')
    option = (default = '-e pdf2' for pdflatex export)
    changedir = boolean for requirement to execute do file from its own directory
    handout = boolean to generate Beamer handouts (default = False)
    comments = boolean to print LyX notes and comments in grey (default = False)
    pdfout = directory for PDF output with default file name -or- file 
                 path (with '.pdf' suffix)
    """

    run = RunProgramDirective(kwargs)
    
    run.error_check('lyx')

    # get program
    program_name = run.program_name
    if run.changedir:
        program = '"' + run.program + '"'
    else:
        program = '"' + run.program_full + '"'
    
    # get option
    option = run.option
    if not run.option:
        option = metadata.default_options['lyx']
        
    # get executable
    executable = run.executable
    if not run.executable:
        executable = metadata.default_executables['lyx']

    # make handout/commented LyX file
    handout = run.handout
    comments = run.comments

    if handout or comments:
        program_name_suffix = '_handout' if handout else '_comments'
        temp_program_name = program_name + program_name_suffix
        temp_program_full = os.path.join(run.program_path, temp_program_name + '.lyx') 
        
        program = program.replace(program_name, temp_program_name)
        program_name = temp_program_name
        
        beamer = False
        shutil.copy2(run.program_full, temp_program_full)
        for line in fileinput.input(temp_program_full, inplace = True):
            if r'\textclass beamer' in line:
                beamer = True
            elif handout and r'\options' in line and beamer:
                line = line.rstrip('\n') + ', handout\n'
            elif comments and ((r'\begin_inset Note Note' in line) or (r'\begin_inset Note Comment')):
                line = line.replace('Note Note', 'Note Greyedout')
            
    command = metadata.commands['lyx'] % (executable, option, program)

    run.execute_run(command)

    # move (and rename) PDF output
    pdfname = os.path.join(run.program_path, program_name + '.pdf')
    pdfout = run.pdfout
    if not re.search('.pdf$', pdfout):
        # assume only provided path, not name
        pdfout = os.path.join(pdfout, program_name + '.pdf')
        
    if os.path.abspath(pdfname) != os.path.abspath(pdfout):
        shutil.copy2(pdfname, pdfout)
        os.remove(pdfname)
        
    # remove handout/commented LyX file
    if handout or comments:
        os.remove(temp_program_full)
          
def run_command(**kwargs):
    """Run a Shell command.
    input: command
    
    command = Shell command
    """

    run = RunCommandDirective(kwargs)
    
    run.error_check('other')

    run.execute_run(run.command)
       
