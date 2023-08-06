import os
import subprocess
from helpers import _get_json, write_json, logging, \
                    static_path, _update_file, _options_prompt, \
                    _yes_no_prompt, _loop_prompt, _Clean_Stop
from distutils.spawn import find_executable
from shutil import rmtree, copytree, copyfile, make_archive
from datetime import datetime

class Note(object):
    def __init__(self, parent, filename, note_number=1):
        if not isinstance(parent, Course):
            raise TypeError('parent must be Course object')
        else:
            self.parent = parent

        if not isinstance(filename, str):
            raise TypeError('filename must be a string')
        else:
            if note_number == 1:
                self.filename = '%s.tex' % filename
                self.texlink = '\\subfile{%s}' % filename
            else:
                self.filename = '%s-%s.tex' % (filename, note_number)
                self.texlink = '\\subfile{%s-%s}' % (filename, note_number)
            path = os.path.join(self.parent.path, 'Notes', self.filename)
            self.path = path
        if not isinstance(note_number, int):
            raise TypeError('note_number must be integer')
        else:
            self.note_number = note_number

    def create(self, include, override=False):
        if not override and os.path.isfile(self.path):
            logging.warning('Note already exists...')
            if not _yes_no_prompt('Note already exists. Replace?'):
                return False

        temp_path = 'class-template/template.tex'
        template_path = os.path.join(static_path, temp_path)
        
        logging.info('Installing note file for %s' % self.parent.cousre_name)
        copyfile(template_path, self.path)
        if include:
            _update_file(self.parent.main_note, '% NOTE FILES END HERE %',
                         self.texlink, append=True)


    def __repr__(self):
        string = '<Note "%s", Course "%s">' 
        return string % (self.filename, self.parent.course_name)

    def __str__(self):
        return 'Note "%s"' % self.filename


class Course(object):
    def __init__(self, parent, course_name):
        if isinstance(course_name, (str, unicode)):
            self.course_name = course_name
        else:
            raise ValueError('course_name must be string')
        if isinstance(parent, Semester):
            self.parent = parent
        else:
            raise ValueError('parent must be Semester object')

        self.path = os.path.join(self.parent.path, self.course_name)
        self.note_path = os.path.join(self.path, 'Notes')
        self.main_note = os.path.join(self.note_path, 'main.tex')
        self.dt_fmt = _get_json()['noteFormat']
        try:
            self.notes = self.get_notes()
        except IOError:
            self.notes = []

        self.graded = self.is_graded()
        if self.graded:
            self.letter_grade, \
            self.gpa_grade, \
            self.credits, \
            self.weight = self.get_grade()
        else:
            self.letter_grade = None
            self.gpa_grade = None
            self.credits = None
            self.weight = None

    def create(self):
        logging.info('Creating course "%s"' % self.course_name)
        current_courses = map(lambda course: course.course_name,
                              self.parent.courses)
        if self.course_name in current_courses:
            if not _yes_no_prompt('Course "%s" already exists. Overwrite?'):
                return
            else:
                reprompt = False
        else:
            reprompt = True

        reprompt_q = 'Directory "%s" already exists. Overwrite?' % self.path
        if reprompt and not _yes_no_prompt(reprompt_q):
            return

        if os.path.isdir(self.path):
            rmtree(self.path)

        os.mkdir(self.path)
        copytree(os.path.join(static_path, 'course-template'),
                 self.note_path)

    def get_notes(self, day=None):
        def valid_line(line, day):
            e = 'Unrecognized note name format "%s"' % line
            if not line or '\\subfile{' not in line or 'formula' in line:
                return None

            fname = line.replace('\\subfile{', '').replace('}', '')
            f_split = fname.split('-')
            if len(f_split) < 3 or len(f_split) > 4:
                logging.warning(e)
                return None
            elif len(f_split) == 4:
                filedate = '-'.join(f_split[0:3])
                try:
                    fileversion = int(f_split[3])
                except ValueError:
                    logging.warning(e)
                    return None
            else:
                filedate ='-'.join(f_split)
                fileversion = 1

            try:
                dt = datetime.strptime(filedate, self.dt_fmt)
            except ValueError:
                logging.warning(e)
                return None
            else:
                if day != None:
                    look_for = day.strftime(self.dt_fmt)
                    compare_to = dt.strftime(self.dt_fmt)
                    if compare_to == look_for:
                        return fname, fileversion
                else:
                    return fname, fileversion


        if day != None and not isinstance(day, datetime):
            raise TypeError('day must be a datetime object')

        try:
            f = open(self.main_note)
        except IOError:
            raise IOError('main.tex file not found')

        lines = f.read().split('\n')
        f.close()
        strip_lines = map(lambda l: l.strip(), lines)
        try:
            start_str = '% NOTE FILES BEGIN HERE %'
            notes_begin = strip_lines.index(start_str)
        except ValueError:
            start_err = 'Did not find line "%s" in main.tex' % start_str
            raise ValueError(start_err)
        try:
            end_str = '% NOTE FILES END HERE %'
            notes_end = strip_lines.index(end_str)
        except ValueError:
            end_err = 'Did not find line "%s" in main.tex' % end_str
            raise ValueError(end_err)

        if notes_begin > notes_end:
            e = '"%s" line found before "%s" line' % (end_str, start_str)
            raise ValueError(e)

        f_lines = [lines[i].strip() for i in range(notes_begin+1, notes_end)]
        filtered_notes = map(lambda f: valid_line(f, day), f_lines)
        filtered_notes = filter(None, filtered_notes)
        note_list = []
        for fname, version in filtered_notes:
            fname_ext = '%s.tex' % fname
            note_list.append(Note(self, filename=fname_ext,
                                  note_number=version))

        return note_list

    def new_notes(self, day=datetime.today()):
        if not isinstance(day, datetime):
            raise TypeError('day keyword argument must be a datetime')

        versions = map(lambda note: note.note_number,
                       self.get_notes(day=day))
        if not versions:
            note = Note(self, day.strftime(self.dt_fmt))
            include = True
        else:
            day_string = day.strftime(self.dt_fmt)
            logging.warning('Notes already exist for %s' % day_string)
            todo = _options_prompt(['Overwrite',
                                    'Add new notes for the same day',
                                    'Cancel'])
            if todo == 1:
                overwrite = True
            elif todo == 2:
                overwrite = False
            elif todo == 3:
                return
            else:
                print 'uh oh'
                raise Exception

            if overwrite:
                version = max(versions)
                include = False
            else:
                version = max(versions) + 1
                include = True

            note = Note(self, day.strftime(self.dt_fmt), note_number=version)

        created = note.create(include, override=True)
        if created == None:
            return None

        self.notes.append(note)

    def is_graded(self):
        # TODO : Abstract this to College object
        json_opts = _get_json()
        f = open(json_opts['gradesPath'])
        lines = [line for line in f.read().split('\n') if line != '']
        courses_graded = map(lambda line: line.split('\t')[1],
                             lines[1:])
        f.close()
        return self.course_name in courses_graded

    def get_grade(self):
        '''returns a 4-tuple: letter_grade, gpa, credits, course_weight'''
        if self.is_graded():
            json_opts = _get_json()
            f = open(json_opts['gradesPath'])
            lines = map(lambda line: line.split('\t'),
                        f.read().split('\n'))
            f.close()
            for line in lines:
                if line[1] == self.course_name:
                    return (line[3], line[4], line[2], line[5])

    def grade_course(self, *args, **kwargs):
        json_opts = _get_json()
        is_graded = self.is_graded()
        if is_graded and not ('override' in kwargs and kwargs['override']):
            overwrite = _yes_no_prompt('Course already graded... overwrite?')
        else:
            overwrite = False

        grades_path = json_opts['gradesPath']
        grading_scheme = json_opts['gradingScheme']

        print 'Input grade for "%s"' % self.course_name
        grade = _loop_prompt('Letter grade: ')
        if grade == None:
            return
        if grade not in grading_scheme.keys():
            logging.critical('Grade type not found in grading scheme...')
            kwargs['override'] = True
            return self.grade_course(**kwargs)

        scheme = grading_scheme[grade]
        gpa = scheme['gpa']
        include_in_gpa = scheme['include_in_gpa']
        credits = _loop_prompt('Credits: ')
        if credits == None:
            return
        if include_in_gpa:
            weight = credits
        else:
            weight = 0
        line_to_write = [self.parent.semester_numb, self.course_name,
                         credits, grade, gpa, weight]
        line_to_write = map(str, line_to_write)
        if overwrite:
            with open(grades_path, 'r+') as f:
                lines = map(lambda line: line.split('\t'),
                        f.read().split('\n'))
                for i, line in enumerate(lines):
                    if line[1] == self.course_name:
                        lines[i] = line_to_write
                        break
                to_write = '\n'.join(map(lambda line: '\t'.join(line), lines))
                f.seek(0)
                f.write(to_write)
                f.truncate()
        else:
            with open(grades_path, 'a') as f:
                f.write('\t'.join(line_to_write) + '\n')

        self.graded = True

    def compile(self):
        os.chdir(self.note_path)
        pdflatex_path = find_executable('pdflatex')
        if not pdflatex_path:
            raise OSError('pdflatex not installed')

        perl_path = find_executable('perl')
        if perl_path:
            texfot_path = os.path.join(static_path, 'texfot.pl')
            process = [perl_path, texfot_path, pdflatex_path, '-shell-escape',
                       '-interaction=nonstopmode', self.main_note, '>>',
                       '/dev/null']
        else:
            logging.warning('Could not find perl executable')
            process = [pdflatex_path, '-interaction=nonstopmode',
                       '-shell-escape', self.main_note, '>>', '/dev/null']

        a = subprocess.call(process)
        if a:
            raise SyntaxError('Error in compiling LaTeX (run 1)')
        else:
            b = subprocess.call(process)
            if b:
                raise SyntaxError('Error in compiling LaTeX (run 2)')
            else:
                return os.path.join(self.note_path, 'main.pdf')
    
    def _archive_prompt(self, grade):
        if grade:
            options = ['Grade, archive & delete course folder',
                       'Grade, archive & keep course folder',
                       'Grade & delete course',
                       'Grade course',
                       'Cancel (remove-course to delete without grading)']
            todo = _options_prompt(options)
            if todo == 1:
                return True, True
            elif todo == 2:
                return True, False
            elif todo == 3:
                return False, True
            elif todo == 4:
                return False, False
            elif todo == 5:
                return None, None
            else:
                print 'uh oh'
                raise Exception
        else:
            options = ['Archive & delete course folder',
                       'Delete course folder',
                       'Cancel']
            todo = _options_prompt(options)
            if todo == 1:
                return True, True
            elif todo == 2:
                return False, True
            elif todo == 3:
                return None, None
            else:
                print 'uh oh'
                raise Exception

    def course_complete(self, grade=True):
        archive_course, delete_course = self._archive_prompt(grade)
        if archive_course == None:
            return

        if grade:
            self.grade_course()
        if archive_course:
            self.archive()
        if delete_course:
            self.delete(override=archive_course)

    def remove_course(self):
        self.course_complete(grade=False)

    def archive(self):
        college = self.parent.parent
        archive_path = college.archive_path
        path = os.path.join(college.archive_path, self.course_name)

        string = 'Archiving %s to "%s"'
        logging.info(string % (self.course_name, archive_path))

        make_archive(path, 'zip', root_dir=self.path)

    def delete(self, override=False):
        if not override:
            if not _yes_no_prompt('Confirm deletion'):
                return

        logging.info('Removing "%s"' % self.course_name)
        rmtree(self.path)
        self.parent.courses = self.parent.get_courses()

    def __repr__(self):
        string = '<course "%s" at Semester <%s>>'
        return string % (self.course_name, self.parent.semester_numb)

    def __str__(self):
        return '<%s>' % self.course_name


class Semester(object):
    def __init__(self, parent, path=None, to_create=False):
        if not isinstance(parent, College):
            raise TypeError('`parent` must be a College object')
        else:
            self.parent = parent

        if to_create:
            return
        
        self.path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(self.path):
            raise IOError('Invalid semester path "%s"' % self.path)

        self.folder_name = os.path.split(self.path)[1]
        
        folder_components = self.folder_name.split(' ')
        e = 'Invalid semester folder: '
        e += 'name must be formatted as `Semester <#>`'
        try:
            self.semester_numb = int(folder_components[1])
            if folder_components[0] != 'Semester':
                raise ValueError
        except ValueError:
            raise ValueError(e)
        except IndexError:
            raise ValueError(e)

        self.courses = self.get_courses()
        self.graded_cs = lambda: [c for c in self.courses if c.graded]
        self.ungraded_cs = lambda: [c for c in self.courses if not c.graded]

    def create(self, semester_number):
        '''Start a new semester'''
        try:
            sem_numb = int(semester_number)
        except TypeError:
            raise TypeError('semester_number must be an integer')

        parent_path = self.parent.path 
        new_path = os.path.join(parent_path, 'Semester %s' % semester_number)
        if os.path.isdir(new_path):
            logging.warning('Semester already exists...')
            todo = _options_prompt(['Add courses to semester',
                                   'Overwrite semester', 'Cancel'])
            if todo == 1:
                add_courses = True
                overwrite = False
            elif todo == 2:
                if _yes_no_prompt('Confirm overwrite'):
                    add_courses = True
                    overwrite = True
            elif todo == 3:
                raise _Clean_Stop
            else:
                print 'uh oh'
                raise Exception

        else:
            overwrite = True
            add_courses = False

        if overwrite and not add_courses:
            os.mkdir(new_path)
        elif overwrite and add_courses:
            rmtree(new_path)
            os.mkdir(new_path)
        elif add_courses and not overwrite:
            pass
        else:
            return

        courses_to_add = []
        print 'Input courses names'
        print 's <enter> to finish'
        print '<ctrl-c> to cancel'
        while True:
            class_name = _loop_prompt('Course name: ', exit_str='s')
            if class_name == False:
                break
            courses_to_add.append(class_name)

        self = Semester(self.parent, path=new_path)

        map(lambda course: Course(self, course).create(), courses_to_add)

    def get_courses(self):
        # subdirs is the list of directories in the semester folder
        try:
            subdirs = next(os.walk(self.path))[1]
        except StopIteration:
            raise IOError('Invalid semester directory')
        subpaths = map(lambda f: os.path.join(self.path, f), subdirs)
        courses = []
        for subdir, subpath in zip(subdirs, subpaths):
            # sub subdirs is the list of directories within each
            # directory within the semester folder
            try:
                sub_subdirs = next(os.walk(subpath))[1]
            except StopIteration:
                raise IOError('Invalid semester directory')
            if 'Notes' in sub_subdirs:
                courses.append(Course(self, subdir))

        return courses

    def select_course(self, courses=None):
        if courses == None:
            courses = self.get_courses()
        if not isinstance(courses, list):
            raise TypeError('courses must be a list')
        for course in courses:
            if not isinstance(course, Course):
                raise TypeError('courses items must be Course objects')

        options = map(lambda course: course.course_name, courses)
        if not options:
            raise _Clean_Stop('No courses found')
        return courses[_options_prompt(options) - 1]

    def new_course(self, course_name):
        Course(self, course_name).create()

    def archive(self):
        college = self.parent
        archive_path = college.archive_path
        path = os.path.join(college.archive_path, self.folder_name)

        string = 'Archiving "%s" to "%s"'
        logging.info(string % (self.folder_name, archive_path))

        make_archive(path, 'zip', root_dir=self.path)

    def delete(self, override=False):
        if not override:
            if not _yes_no_prompt('Confirm deletion'):
                raise _Clean_Stop

        json_opts = _get_json()
        new_opts = json_opts.copy()
        if new_opts['defaultSemester'] == self.path:
            for i, semester in enumerate(self.parent.semesters):
                if semester.semester_numb == self.semester_numb:
                    self.parent.semesters.pop(i)
                    break
            
            self.default_semester = self.parent.get_latest_semester()
            new_opts['defaultSemester'] = self.default_semester.path
            write_json(new_opts)

        logging.info('Deleting %s' % self.path)
        rmtree(self.path)

    def _semester_prompt(self):
        print 'Finishing Semester %s' % self.semester_numb
        options = ['Archive semester',
                   'Archive semester & delete folder',
                   'Cancel.']
        todo = _options_prompt(options)
        if todo == 1:
            return True, False
        elif todo == 2:
            return True, True
        elif todo == 3:
            return False, False
        else:
            print 'uh oh'
            raise Exception

    def semester_complete(self):
        if self.ungraded_cs():
            logging.warning('Not all courses are graded')
            options = ['Grade first', 'Continue without grading', 'Cancel']
            todo = _options_prompt(options)
            if todo == 1:
                u_courses = self.ungraded_cs()
                while u_courses:
                    course = self.select_course(courses=u_courses)
                    course.grade_course()
                    u_courses = self.ungraded_cs()

            elif todo == 2:
                pass
            elif todo == 3:
                raise _Clean_Stop
            else:
                print 'uh oh'
                raise Exception

        archive_semester, delete_semester = self._semester_prompt()
        if archive_semester:
            self.archive()
        if delete_semester:
            self.delete(override=True)

    def __repr__(self):
        string = '<semester <%s> with %s courses at college "%s">'
        return string % (self.semester_numb,
                         len(self.courses),
                         self.parent.path)


class College(object):
    def __init__(self, path=_get_json()['collegeDirectory']):
        if path == False:
            path = self.create()
        elif not isinstance(path, (str, unicode)):
            raise TypeError('College: path must be a string')

        json_opts = _get_json()
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.isdir(path):
            e = 'Invalid path. College directory may have been removed.'
            logging.error(e)
            todo = _options_prompt(['Remake college directory',
                                    'Choose new directory',
                                    'Cancel'])
            if todo == 1:
                pass
            elif todo == 2:
                self = College(path=False)
                return
            elif todo == 3:
                raise _Clean_Stop
            else:
                print 'uh oh'
                raise Exception
        
        self.path = path
        self.archive_path = os.path.join(self.path, 'Archive-path')
        if not os.path.isdir(self.archive_path):
            os.makedirs(self.archive_path)

        self.semesters = self.get_semesters()
        if not self.semesters:
            # no semesters in college dir but path is in config
            if json_opts['defaultSemester']:
                e = 'Default Semester path not recognized'
                e += '(requires format Semester <#>)'
                raise IOError(e)
            # no semesters in college dir and no path in config
            else:
                e = 'No semesters found... run `new-semester <semester-number>'
                logging.warning(e)
                self.default_semester = None
        elif not json_opts['defaultSemester']:
            new_opts = json_opts.copy()
            latest_semester = self.get_latest_semester()
            new_opts['defaultSemester'] = latest_semester.path
            write_json(new_opts)
            self.default_semester = self.get_default_semester()
        else:
            def_sem_path = json_opts['defaultSemester']
            self.default_semester = Semester(self, path=def_sem_path)

    def create(self):
        logging.info('First run detected')
        prompt = 'Input a parent college directory '
        prompt += '(relative paths supported)\n> '
        inp = _loop_prompt(prompt)

        path = os.path.abspath(os.path.expanduser(inp))

        if not os.path.isdir(path):
            logging.info('Installing directory...')
            os.makedirs(path)
        
        json_opts = _get_json()
        json_opts['gradesPath'] = False
        json_opts['defaultSemester'] = False
        json_opts['collegeDirectory'] = path
        header = '%s\t' * 6 + '\n'
        header = header % ('Semester', 'Course', 'Grade',
                           'Credits', 'Weight', 'GPA')
        if json_opts['gradesPath']:
            with open(json_opts['gradesPath'], 'w') as f:
                f.write(header)
        else:
            grades_path = os.path.join(path, 'grades.tsv')
            json_opts['gradesPath'] = grades_path
            with open(grades_path, 'w') as f:
                f.write(header)

        logging.info('Saving configuration..')
        write_json(json_opts)
        raise _Clean_Stop

    def get_semesters(self):
        subdirs = next(os.walk(self.path))[1]
        semesters = []
        for subdir in subdirs:
            try:
                sem = Semester(self, path=os.path.join(self.path, subdir))
            except ValueError:
                pass
            else:
                semesters.append(sem)

        return semesters

    def new_semester(self, semester_number):
        Semester(self, to_create=True).create(semester_number)

    def get_default_semester(self, *args, **kwargs):
        json_opts = _get_json()
        try:
            return Semester(self, path=json_opts['defaultSemester'])
        except AttributeError:
            return self.get_latest_semester()          

    def get_latest_semester(self):
        latest = -1
        latest_sem = False
        for semester in self.semesters:
            sem_numb = semester.semester_numb
            if sem_numb > latest:
                latest = sem_numb
                latest_sem = semester

        return latest_sem

    def print_grades(self):
        print 'Not implemented yet...'

    def __repr__(self):
        string = '<college dir at "%s" with %s semesters>'
        return string % (self.path, len(self.semesters))


if __name__ == '__main__':
    c = College()

