List of built-in binaries:

::

    1. `newsemester <semester-number>`
    2. `newcourse "[<course-name>]"`
    3. `removecourse`
    4. `newnotes`
    5. `classcompile`
    6. `coursecomplete`
    7. `semestercomplete`
    8. `printgrades`

The first time you run a command after ``coursemanager`` installation,
you will be prompted to setup your college directory (where all notes,
course directories, and grade files will be stored).

1. ``newsemester <semester-number>``

-  Creates the directory 'Semester ' within your college directory.
-  Prompts for courses being taken in the new semester. Creates a course
   directory for each course with a 'Notes' subdirectory in each course
   directory.

2. ``newcourse "[<course-name>]"``

-  Creates a new course with name []. Defaults to the latest semester
   (highest semester number).
-  To change the default semester directory, run the following code in
   python: from course\_manager import config\_path print config\_path

Navigate to the JSON file printed out and change the defalt\_directory
variable to match what you want the current semester to be.

3. ``removecourse``

-  Removes a given course without recording a grade. Gives the option to
   completely remove the course directory or to archive it to a ZIP
   file.
-  Options for courses to remove are based on the default semester (see
   (2.) for more).

4. ``newnotes``

-  Adds new notes to a given course. If cwd is within a given course
   directory, the notes will be created for that course. Otherwise,
   options for courses are based on the default semester (see (2.) for
   more).

-  By default, ``newnotes`` will create a new .tex file named the
   current date. The .tex file will contain the necessary components to
   be recognized as a
   ```subfile`` <https://www.sharelatex.com/learn/Multi-file_LaTeX_projects>`__
   of the main.tex file that is initially created within the course
   directory.

-  A line linking to the new notes file is added to the ``main.tex``
   file.

5. ``classcompile`` [config]

-  Compiles the ``main.tex`` file for a given course. If cwd is within a
   given course directory, the notes will be created for that course.
   Otherwise, options for courses are based on the default semester (see
   (2.) for more).

-  If ``config`` is used within the command, all LaTeX extra files
   (``main.log``, ``main.toc``, ``main.out``, and ``main.aux`` are NOT
   deleted after compilation.)

-  This command compiles the LaTeX twice (LaTeX compilation is a
   two-pass process, originally to preserve memory. Running only once
   will not always catch figure and citation references).

6. ``coursecomplete``

-  Archives a given course. Options for courses to remove are based on
   the default semester (see (2.) for more).

-  Prompts for the grade in that course and how many credits the course
   was worth. Updates the ``grades.tsv`` file with the new grade.

-  Currently, GPA calculations are based on Brown University grading
   standards. These settings can be edited in the ``config.json`` file
   (instructions on how to edit this file are under (2.).

7. ``semestercomplete``

-  Archives the default semester (see (2.) for more about the default
   semester). Gives the option to keep or remove the default semester
   directory in addition to archiving it.

-  Runs ``coursecomplete`` on all courses for which grades have not yet
   been inputted.

-  Updates ``grades.tsv``.

8. ``printgrades``

-  Prints a formatted versions of ``grades.tsv`` to the terminal. (Uses
   the python
   ```tabulate`` <https://bitbucket.org/astanin/python-tabulate#rst-header-table-format>`__
   package. You can edit the format of the output by running
   ``which printgrades`` and editing the type of table printed. The
   options can be found with the
   ```tabulate`` <https://bitbucket.org/astanin/python-tabulate#rst-header-table-format>`__
   documentation.).
