import os
import json
import logging
import readline
import sys
from colors import red, yellow, green, blue, magenta

class _Clean_Stop(Exception):
    pass

if not sys.argv:
    pass

elif sys.argv[0]:
    __orig_hook = sys.excepthook
    
    def __my_except_hook(exception_type, exception_message, exception_traceback):
        global sys
        if exception_type.__name__ == 'KeyboardInterrupt':
            print red('User interrupt...')
            sys.excepthook = __orig_hook
        elif exception_type.__name__ == '_Clean_Stop':
            if exception_message.message:
                logging.error(exception_message)
            sys.excepthook = __orig_hook
        else:
            __orig_hook(exception_type, exception_message, exception_traceback)
    
    sys.excepthook = __my_except_hook

class MyFormatter(logging.Formatter):
    err_fmt  = red("ERROR: %(msg)s")
    dbg_fmt  = yellow("DBG: %(module)s: %(lineno)d: %(msg)s")
    info_fmt = "%(msg)s"
    wrng_fmt = yellow("WARNING: %(msg)s")
    crit_fmt = red("CRITICAL: %(msg)s")

    def __init__(self, fmt="%(levelno)s: %(msg)s"):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = MyFormatter.dbg_fmt

        elif record.levelno == logging.INFO:
            self._fmt = MyFormatter.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = MyFormatter.err_fmt

        elif record.levelno == logging.CRITICAL:
            self._fmt = MyFormatter.crit_fmt

        elif record.levelno == logging.WARNING:
            self._fmt = MyFormatter.wrng_fmt

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._fmt = format_orig

        return result

fmt = MyFormatter()
hdlr = logging.StreamHandler(sys.stdout)

hdlr.setFormatter(fmt)
logging.root.addHandler(hdlr)

readline.parse_and_bind('tab: complete')
logging.root.setLevel(logging.DEBUG)
logging.basicConfig(format=yellow('%(levelname)-10s%(message)s'))

def _get_data(path):
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, path)

config_path = _get_data('static/config.json')
static_path = _get_data('static')

def _path_errs(var_name, json_opts):
    base_err = 'Invalid JSON file: '
    def _check_path(path):
        if path == False:
            return False
        elif not isinstance(path, (str, unicode)):
            raise TypeError
        elif not os.path.exists(path):
            raise IOError
        elif os.path.abspath(os.path.expanduser(path)) != path:
            raise AttributeError
        else:
            return path
    try:
        _check_path(json_opts[var_name])
    except TypeError:
        e = base_err + 'Invalid %s variable' % var_name
        raise ValueError(e)
    except AttributeError:
        e = base_err + 'Please do not use relative paths '
        e += 'in the JSON file (%s)' % var_name
        raise AttributeError(e)
    except IOError:
        e = base_err + '"%s" variable is not a directory' % var_name
        raise ValueError(e)

def _run_checks(json_opts):
    base_err = 'Invalid JSON file: '
    required_keys = [u'defaultSemester',
                     u'collegeDirectory',
                     u'semesterList',
                     u'gradingScheme',
                     u'courseList',
                     u'semesterNumber',
                     u'setDefaultSemesterOn-newsemester',
                     u'gradesPath',
                     u'noteFormat']
    # check that all necessary keys are present
    for key in json_opts.keys():
        if key not in required_keys:
            e = base_err + 'Could not find key "%s"' % key
            raise KeyError(e)
    
    # check collegeDirectory variable
    _path_errs('collegeDirectory', json_opts)

    # check defaultSemester variable
    _path_errs('defaultSemester', json_opts)

    # check gradesPath variable
    _path_errs('gradesPath', json_opts)
    if json_opts['gradesPath']:
        if os.path.splitext(json_opts['gradesPath'])[1] != '.tsv':
            raise IOError('gradesPath must be a .tsv file')

    if not isinstance(json_opts['noteFormat'], (str, unicode)):
        e = base_err + 'noteFormat must be a string'
        raise TypeError(e)

    if not isinstance(json_opts['gradingScheme'], dict):
        e = base_err + 'Grading Scheme must be a dictionary'
        raise TypeError(e)
    required_grade_vals = [('gpa', float), ('include_in_gpa', bool)]
    for key in json_opts['gradingScheme'].keys():
        value = json_opts['gradingScheme'][key]
        if not isinstance(value, dict):
            raise TypeError('Grading Scheme components must be dicts')

        for req_key, req_type in required_grade_vals:
            if req_key not in value.keys():
                e = 'Grading Scheme components must have components:'
                e +=  '\'gpa\', \'include_in_gpa\''
                raise KeyError(e)
            if not isinstance(value[req_key], req_type):
                raise TypeError('%s must be %s' % (req_key, req_type))

    return json_opts

def _get_json():
    json_opts = json.load(open(config_path))
    college_dir = json_opts['collegeDirectory']
    rewrite = False
    if college_dir:
        new_dir = os.path.abspath(os.path.expanduser(college_dir))
        json_opts['collegeDirectory'] = new_dir
        if new_dir != college_dir:
            rewrite = True

    sem_dir = json_opts['defaultSemester']
    if sem_dir:
        new_dir = os.path.abspath(os.path.expanduser(sem_dir))
        json_opts['defaultSemester'] = new_dir
        if sem_dir != new_dir:
            rewrite = True
    write_json(json_opts) if rewrite else None
    return json_opts

write_json = lambda opts: json.dump(opts, open(config_path, 'w'),
                                    indent=4, sort_keys=True)

def _update_file(path, startswith_str, to_replace, append=False):
    f = open(path, 'r')
    lines = f.read().split('\n')
    f.close()
    for i, line in enumerate(lines):
        if line.startswith(startswith_str):
            if append:
                lines.insert(i, to_replace)
            else:
                lines[i] = to_replace
            break

    f = open(path, 'w')
    f.write('\n'.join(lines))
    f.close()

def _loop_prompt(q, require_response=True, exit_str=None,
                 exit_on_interrupt=True):
    if (isinstance(exit_str, (str, unicode)) and
        not exit_str and require_response):
        e = '_loop_prompt: can\'t use empty string exit_str'
        e += ' and require a response'
        raise ValueError(e)
    try:
        inp = raw_input(q)
    except KeyboardInterrupt:
        if exit_on_interrupt:
            raise KeyboardInterrupt('User interrupt...')
        else:
            return None
    else:
        if not inp and require_response:
            print 'Please enter a response'
            return loop_prompt(q, require_response=require_response)
        elif inp.lower() == exit_str:
            return False
        else:
            return inp

def _options_prompt(options, exit_on_interrupt=True):
    if not isinstance(options, list):
        raise TypeError('_options_prompt options must be a list of strings')
    if not options:
        raise TypeError('_options_prompt options must have at least one item')

    options_str = ''
    for i, option in enumerate(options):
        option_numb = i + 1
        options_str += '%s %s' % (magenta(str(option_numb) + '.'), option)

        if option_numb != len(options):
            options_str += '\n'

    print options_str
    while True:
        try:
            inp = raw_input('> ').strip('.')
            numb = int(inp)
            if numb < 1 or numb > len(options):
                raise ValueError

        except KeyboardInterrupt:
            if exit_on_interrupt:
                raise KeyboardInterrupt('User interrupt...')
            else:
                return None
        except ValueError:
            print 'Invalid input...'
            continue
        else:
            return numb


def _yes_no_prompt(pre_print, exit_on_interrupt=True):
    pre_print += ' [%s/%s]' % (green('y'), red('n'))
    print pre_print
    while True:
        try:
            inp = raw_input('> ')
            inp = inp.lower()
        except KeyboardInterrupt:
            if exit_on_interrupt:
                raise KeyboardInterrupt('User interrupt...')
            else:
                return None
        else:
            if inp == 'y':
                return True
            elif inp == 'n':
                return False
            else:
                print 'Please enter [%s] or [%s]' % (green('y'), red('n'))
                continue

