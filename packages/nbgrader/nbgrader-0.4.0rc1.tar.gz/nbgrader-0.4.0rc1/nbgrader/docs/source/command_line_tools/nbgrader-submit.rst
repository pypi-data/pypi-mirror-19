
nbgrader submit
===============

::

    Submit an assignment to the nbgrader exchange
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --debug
        set log level to DEBUG (maximize logging output)
    --strict
        Fail if the submission is missing notebooks for the assignment
    --quiet
        set log level to CRITICAL (minimize logging output)
    --notebook=<Unicode> (NbGrader.notebook_id)
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --timezone=<Unicode> (TransferApp.timezone)
        Default: 'UTC'
        Timezone for recording timestamps
    --course=<Unicode> (NbGrader.course_id)
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --assignment=<Unicode> (NbGrader.assignment_id)
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --db=<Unicode> (NbGrader.db_url)
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --student=<Unicode> (NbGrader.student_id)
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
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
    
    SubmitApp options
    -----------------
    --SubmitApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --SubmitApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --SubmitApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --SubmitApp.cache_directory=<Unicode>
        Default: ''
        Local cache directory for nbgrader submit and nbgrader list. Defaults to
        $JUPYTER_DATA_DIR/nbgrader_cache
    --SubmitApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --SubmitApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --SubmitApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --SubmitApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --SubmitApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --SubmitApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --SubmitApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --SubmitApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --SubmitApp.exchange_directory=<Unicode>
        Default: '/srv/nbgrader/exchange'
        The nbgrader exchange directory writable to everyone. MUST be preexisting.
    --SubmitApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --SubmitApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --SubmitApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --SubmitApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --SubmitApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --SubmitApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --SubmitApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --SubmitApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --SubmitApp.path_includes_course=<Bool>
        Default: False
        Whether the path for fetching/submitting  assignments should be prefixed
        with the course name. If this is `False`, then the path will be something
        like `./ps1`. If this is `True`, then the path will be something like
        `./course123/ps1`.
    --SubmitApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --SubmitApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --SubmitApp.strict=<Bool>
        Default: False
        Whether or not to submit the assignment if there are missing notebooks from
        the released assignment notebooks.
    --SubmitApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --SubmitApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --SubmitApp.timestamp_format=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S %Z'
        Format string for timestamps
    --SubmitApp.timezone=<Unicode>
        Default: 'UTC'
        Timezone for recording timestamps
    
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
    
    Examples
    --------
    
        Submit an assignment for grading. For the usage of students.
        
        You must run this command from the directory containing the assignments
        sub-directory. For example, if you want to submit an assignment named
        `assignment1`, that must be a sub-directory of your current working directory.
        If you are inside the `assignment1` directory, it won't work.
        
        To fetch an assignment you must first know the `course_id` for your course.
        If you don't know it, ask your instructor.
        
        To submit `assignment1` to the course `phys101`:
        
            nbgrader submit assignment1 --course phys101
        
        You can submit an assignment multiple times and the instructor will always
        get the most recent version. Your assignment submission are timestamped
        so instructors can tell when you turned it in. No other students will
        be able to see your submissions.
    
    