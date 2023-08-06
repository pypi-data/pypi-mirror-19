#! /usr/bin/python2.7

import argparse
import fileinput
import logging
import os
import re
import shutil

# create logger
logger = logging.getLogger('php2python')

debug = True

# console handler
ch = logging.StreamHandler()
if debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

ch.setLevel(logging.DEBUG)

formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter2 = logging.Formatter('%(levelname)s - %(message)s')

ch.setFormatter(formatter2)

logger.addHandler(ch)

declarations = []
in_foreach = False
in_if = False
last_indent = None


def python_script_name(php_script):
    return php_script.split('.php')[0] + '.py'


def replace(f, o, n):
    php_file = fileinput.FileInput(f, inplace=True)
    for line in php_file:
        # sys.stdout.write('new text')
        print(line.replace(o, n)),

    php_file.close()


def remove_lines_bound(f, start, end=None, ignore_leading_spaces=True):
    php_file = fileinput.FileInput(f, inplace=True)
    end = '[' + end + ']$' if end else ''
    if ignore_leading_spaces:
        reg = '^(( )*' + start + ').*' + end
    else:
        reg = '^' + start + '.*' + end
    for line in php_file:
        if re.match(reg, line):
            continue

        print(line),

    php_file.close()


def add_self_to_functions(f):
    process_class_declarations(f)

    php_file = fileinput.FileInput(f, inplace=True)
    for line in php_file:
        reg = r'(.*)(public|protected) function (.*)\((.*)\)'
        match = re.match(reg, line)
        if match:

            groups = match.groups()
            function_indent = groups[0]
            function_name = '__init__' if groups[2] == '__construct' else groups[2]
            function_params = '(self,' + groups[3] + '):' if groups[3] else '(self):'

            function = function_indent + 'def ' + function_name + function_params
            print function

            if groups[2] == '__construct':
                for declaration in declarations:
                    print declaration
                print
                # todo case of no constructor
        else:
            print(line),

    php_file.close()


def process_class_declarations(f):
    php_file = fileinput.FileInput(f, inplace=True)
    for line in php_file:
        reg = r'(.*)(public|protected) \$(.*);$'
        match = re.match(reg, line)
        if match:

            groups = match.groups()
            declaration_indent = groups[0]
            declaration = (declaration_indent * 2) + 'self.' + groups[2] + ' = None'

            declarations.append(declaration)
            continue
        else:
            print(line),

    php_file.close()


def class_definition(f):
    php_file = fileinput.FileInput(f, inplace=True)
    for line in php_file:
        reg = r'class (\w+)( extends (\w+)|)'
        match = re.match(reg, line)
        if match:
            groups = match.groups()
            class_name = groups[0]
            class_parent = groups[2] or 'object'
            if groups[2]:
                logger.warning("You need to import " + groups[2])

            class_def = 'class ' + class_name + '(' + class_parent + '):'
            print class_def

        else:
            print(line),

    php_file.close()


def process_if(py_script):
    php_file = fileinput.FileInput(py_script, inplace=True)
    for line in php_file:
        reg = r'(.*)if(.*)\((.*)\)(.*)\{$'
        match = re.match(reg, line)
        if match:
            groups = match.groups()
            if_indent = groups[0]
            if_line = if_indent + 'if ' + groups[2] + ':'
            print(if_line)
        else:
            print(line),

    php_file.close()


def process_else(py_script):
    php_file = fileinput.FileInput(py_script, inplace=True)
    for line in php_file:
        reg = r'(.*)\}(.*)else(.*)(.*)\{$'
        match = re.match(reg, line)
        if match:
            groups = match.groups()
            else_indent = groups[0]
            else_line = else_indent + 'else :'
            print(else_line)
        else:
            print(line),

    php_file.close()


def process_foreach(py_script):
    php_file = fileinput.FileInput(py_script, inplace=True)
    for line in php_file:
        reg = r'(.*)foreach(.*)\((.*) as (.*)\)(.*)\{$'
        match = re.match(reg, line)
        if match:

            groups = match.groups()
            foreach_indent = groups[0]
            needle = groups[3]
            haystack = groups[2]
            foreach_line = foreach_indent+'for '+needle + ' in '+haystack+' :'

            print(foreach_line)
        else:
            print(line),

    php_file.close()


def convert2python(php_script, py_script, overwrite):
    if not os.path.exists(php_script):
        logger.error("Could not locate PHP script: %s" % php_script)
        return

    if os.path.exists(py_script):
        if not overwrite:
            logger.error("Sorry, A python Script %s already exist, use -o to overwrite." % py_script)
            return

    logger.info("Converting: %s. Output file will be: %s" % (php_script, py_script))
    shutil.copyfile(php_script, py_script)

    logger.info('# Remove opening and closing <?php')
    replace(py_script, '<?php', '')

    logger.info('# convert $this-> to self.')
    replace(py_script, '$this->', 'self.')

    logger.info('# convert :: to .')
    replace(py_script, '::', '.')

    logger.info('# Process if statements')
    process_if(py_script)

    logger.info('# Process else statements')
    process_else(py_script)

    logger.info('# delete all }')
    logger.info('# delete namespace|require_once|include_once')
    remove_lines_bound(py_script, "namespace", ";")
    remove_lines_bound(py_script, "require_once", ";")
    remove_lines_bound(py_script, "include_once", ";")
    remove_lines_bound(py_script, "\{", "")
    remove_lines_bound(py_script, "\}", "")

    logger.info('# convert protected $var to self.var = None then move into __init__')
    logger.info('# convert public|protected function to def')
    logger.info('# add `self` to function signatures')
    add_self_to_functions(py_script)

    logger.info('# classes not children to extend `object`')
    logger.info('# process child classes')
    class_definition(py_script)

    logger.info('# convert $ to \'\'')
    replace(py_script, '$', '')

    logger.info('# convert ; to \'\'')
    replace(py_script, ';', '')

    logger.info('# convert new to \'\'')
    replace(py_script, 'new ', '')

    logger.info('# process foreach')
    process_foreach(py_script)

    logger.info(("Converted: %s. to: %s. { Go on, Proof Check :) }" % (php_script, py_script)))


def main():
    parser = argparse.ArgumentParser(description='PHP to PYTHON syntax converter.')
    parser.add_argument('-s', '--script', help='Path to PHP script', required=True)
    parser.add_argument('-o', '--overwrite', help='Overwrite Python script if exists', action='store_true')

    args = parser.parse_args()
    php_script = args.script
    py_script = python_script_name(php_script)

    convert2python(php_script, py_script, args.overwrite)


if __name__ == '__main__':
    main()
