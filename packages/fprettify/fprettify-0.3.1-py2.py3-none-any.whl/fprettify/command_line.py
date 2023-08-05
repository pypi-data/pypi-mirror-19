"""
  fprettify Command line interface
"""
import re
import sys
import os
import logging
import fprettify


def main(argv=None):
    """
    Command line interface
    """
    if argv is None:
        argv = sys.argv
    defaults_dict = {'indent': 3, 'whitespace': 2,
                     'stdout': 0, 'report-errors': 1,
                     'debug': 0}

    usage_desc = ("usage:\n" + argv[0] + """
    [--indent=3] [--whitespace=2]
    [--[no-]stdout] [--[no-]report-errors] file1 [file2 ...]
    [--help]
    [--[no-]debug]

    Auto-format F90 source file1, file2, ...:
    If no files are given, stdin is used.
             Auto-indentation, auto-alignment and whitespace formatting.
             Amount of whitespace controlled by --whitespace=0,1,2.
             For indenting with a relative width of n columns
             specify --indent=n.

             For manual formatting of specific lines:

             * disable auto-alignment by starting line continuation
               with an ampersand '&'.
             * completely disable reformatting by adding a comment '!&'.

             For manual formatting of a code block, use:

             * start a manually formatted block with a '!&<' comment
               and close it with a '!&>' comment.

    --stdout
             write output to stdout
    --[no-]report-errors
             report warnings and errors

    Defaults:
    """ + str(defaults_dict))

    if "--help" in argv:
        sys.stderr.write(usage_desc + '\n')
        return 0
    args = []
    for arg in argv[1:]:
        match = re.match(
            r"--(no-)?(stdout|report-errors|debug)", arg)
        if match:
            defaults_dict[match.groups()[1]] = not match.groups()[0]
        else:
            match = re.match(
                r"--(indent|whitespace)=(.*)", arg)
            if match:
                defaults_dict[match.groups()[0]] = int(match.groups()[1])
            else:
                if arg.startswith('--'):
                    sys.stderr.write('unknown option ' + arg + '\n')
                else:
                    args.append(arg)
    failure = 0
    if not args:
        args = ['stdin']

    for filename in args:
        if not os.path.isfile(filename) and filename != 'stdin':
            sys.stderr.write("file " + filename + " does not exists!\n")
        else:
            stdout = defaults_dict['stdout'] or filename == 'stdin'

            if defaults_dict['report-errors']:
                if defaults_dict['debug']:
                    level = logging.DEBUG
                else:
                    level = logging.INFO

            else:
                level = logging.CRITICAL

            logger = logging.getLogger('prettify-logger')
            logger.setLevel(level)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            try:
                fprettify.reformat_inplace(filename,
                                           stdout=stdout,
                                           indent_size=defaults_dict['indent'],
                                           whitespace=defaults_dict['whitespace'])
            except:
                failure += 1
                import traceback
                sys.stderr.write('-' * 60 + "\n")
                traceback.print_exc(file=sys.stderr)
                sys.stderr.write('-' * 60 + "\n")
                sys.stderr.write("Processing file '" + filename + "'\n")
    return failure > 0
