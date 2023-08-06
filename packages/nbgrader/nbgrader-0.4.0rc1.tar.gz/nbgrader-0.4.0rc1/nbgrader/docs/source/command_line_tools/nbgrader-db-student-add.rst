
nbgrader db student add
=======================

::

    Add a student to the nbgrader database
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --email=<Unicode> (DbStudentAddApp.email)
        Default: None
        The email of the student
    --first-name=<Unicode> (DbStudentAddApp.first_name)
        Default: None
        The first name of the student
    --last-name=<Unicode> (DbStudentAddApp.last_name)
        Default: None
        The last name of the student
    --db=<Unicode> (NbGrader.db_url)
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --log-level=<Enum> (Application.log_level)
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --course-dir=<Unicode> (NbGrader.course_directory)
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    
    Class parameters
    ----------------
    
    Parameters are set from command-line arguments of the form:
    `--Class.trait=value`. This line is evaluated in Python, so simple expressions
    are allowed, e.g.:: `--C.a='range(3)'` For setting C.a=[0,1,2].
    
    DbStudentAddApp options
    -----------------------
    --DbStudentAddApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --DbStudentAddApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --DbStudentAddApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --DbStudentAddApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --DbStudentAddApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --DbStudentAddApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --DbStudentAddApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --DbStudentAddApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --DbStudentAddApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --DbStudentAddApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --DbStudentAddApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --DbStudentAddApp.email=<Unicode>
        Default: None
        The email of the student
    --DbStudentAddApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --DbStudentAddApp.first_name=<Unicode>
        Default: None
        The first name of the student
    --DbStudentAddApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --DbStudentAddApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --DbStudentAddApp.last_name=<Unicode>
        Default: None
        The last name of the student
    --DbStudentAddApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --DbStudentAddApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --DbStudentAddApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --DbStudentAddApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --DbStudentAddApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --DbStudentAddApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --DbStudentAddApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --DbStudentAddApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --DbStudentAddApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    NbGrader options
    ----------------
    --NbGrader.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --NbGrader.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --NbGrader.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --NbGrader.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --NbGrader.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --NbGrader.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --NbGrader.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --NbGrader.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --NbGrader.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --NbGrader.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --NbGrader.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --NbGrader.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --NbGrader.generate_config=<Bool>
        Default: False
        Generate default config file.
    --NbGrader.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --NbGrader.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --NbGrader.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --NbGrader.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --NbGrader.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --NbGrader.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --NbGrader.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --NbGrader.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --NbGrader.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --NbGrader.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    