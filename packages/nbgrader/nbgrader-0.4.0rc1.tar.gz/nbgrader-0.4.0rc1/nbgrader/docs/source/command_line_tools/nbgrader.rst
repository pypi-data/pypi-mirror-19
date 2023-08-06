
nbgrader
========

::

    A system for assigning and grading notebooks
    
    Subcommands
    -----------
    
    Subcommands are launched as `nbgrader cmd [args]`. For information on using
    subcommand 'cmd', do: `nbgrader cmd -h`.
    
    export
        Export grades from the database to another format.
    assign
        Create the student version of an assignment. Intended for use by
        instructors only.
    extension
        Install and activate the "Create Assignment" notebook extension.
    release
        Release an assignment to students through the nbgrader exchange.
        Intended for use by instructors only.
    validate
        Validate a notebook in an assignment. Intended for use by
        instructors and students.
    quickstart
        Create an example class files directory with an example
        config file and assignment.
    autograde
        Autograde submitted assignments. Intended for use by instructors
        only.
    collect
        Collect an assignment from students through the nbgrader exchange.
        Intended for use by instructors only.
    fetch
        Fetch an assignment from an instructor through the nbgrader exchange.
        Intended for use by students only.
    submit
        Submit an assignment to an instructor through the nbgrader exchange.
        Intended for use by students only.
    feedback
        Generate feedback (after autograding and manual grading).
        Intended for use by instructors only.
    formgrade
        Manually grade assignments (after autograding). Intended for use
        by instructors only.
    list
        List inbound or outbound assignments in the nbgrader exchange.
        Intended for use by instructors and students.
    update
        Update nbgrader cell metadata to the most recent version.
    db
        Perform operations on the nbgrader database, such as adding,
        removing, importing, and listing assignments or students.
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --debug
        set log level to DEBUG (maximize logging output)
    --generate-config
        Generate a config file.
    --quiet
        set log level to CRITICAL (minimize logging output)
    --notebook=<Unicode> (NbGrader.notebook_id)
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --student=<Unicode> (NbGrader.student_id)
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --assignment=<Unicode> (NbGrader.assignment_id)
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
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
    --course=<Unicode> (NbGrader.course_id)
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    
    Class parameters
    ----------------
    
    Parameters are set from command-line arguments of the form:
    `--Class.trait=value`. This line is evaluated in Python, so simple expressions
    are allowed, e.g.:: `--C.a='range(3)'` For setting C.a=[0,1,2].
    
    NbGraderApp options
    -------------------
    --NbGraderApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --NbGraderApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --NbGraderApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --NbGraderApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --NbGraderApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --NbGraderApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --NbGraderApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --NbGraderApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --NbGraderApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --NbGraderApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --NbGraderApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --NbGraderApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --NbGraderApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --NbGraderApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --NbGraderApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --NbGraderApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --NbGraderApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --NbGraderApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --NbGraderApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --NbGraderApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --NbGraderApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --NbGraderApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --NbGraderApp.submitted_directory=<Unicode>
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
    
    ExportApp options
    -----------------
    --ExportApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --ExportApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --ExportApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ExportApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --ExportApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --ExportApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --ExportApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --ExportApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --ExportApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --ExportApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --ExportApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --ExportApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ExportApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --ExportApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --ExportApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --ExportApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --ExportApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --ExportApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --ExportApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --ExportApp.plugin_class=<Type>
        Default: 'nbgrader.plugins.export.CsvExportPlugin'
        The plugin class for exporting the grades.
    --ExportApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --ExportApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ExportApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --ExportApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    AssignApp options
    -----------------
    --AssignApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --AssignApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --AssignApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --AssignApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --AssignApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --AssignApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --AssignApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --AssignApp.create_assignment=<Bool>
        Default: False
        Whether to create the assignment at runtime if it does not already exist.
    --AssignApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --AssignApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --AssignApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --AssignApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --AssignApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --AssignApp.force=<Bool>
        Default: False
        Whether to overwrite existing assignments/submissions
    --AssignApp.from_stdin=<Bool>
        Default: False
        read a single notebook from stdin.
    --AssignApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --AssignApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --AssignApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --AssignApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --AssignApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --AssignApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --AssignApp.no_database=<Bool>
        Default: False
        Do not save information about the assignment into the database.
    --AssignApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --AssignApp.output_files_dir=<Unicode>
        Default: '{notebook_name}_files'
        Directory to copy extra files (figures) to. '{notebook_name}' in the string
        will be converted to notebook basename
    --AssignApp.permissions=<Int>
        Default: 0
        Permissions to set on files output by nbgrader. The default is generally
        read-only (444), with the exception of nbgrader assign, in which case the
        user also has write permission.
    --AssignApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --AssignApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --AssignApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --AssignApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    ExtensionApp options
    --------------------
    --ExtensionApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --ExtensionApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --ExtensionApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ExtensionApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --ExtensionApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --ExtensionApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --ExtensionApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --ExtensionApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --ExtensionApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --ExtensionApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --ExtensionApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --ExtensionApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ExtensionApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --ExtensionApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --ExtensionApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --ExtensionApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --ExtensionApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --ExtensionApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --ExtensionApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --ExtensionApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --ExtensionApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ExtensionApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --ExtensionApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    ReleaseApp options
    ------------------
    --ReleaseApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --ReleaseApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --ReleaseApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ReleaseApp.cache_directory=<Unicode>
        Default: ''
        Local cache directory for nbgrader submit and nbgrader list. Defaults to
        $JUPYTER_DATA_DIR/nbgrader_cache
    --ReleaseApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --ReleaseApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --ReleaseApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --ReleaseApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --ReleaseApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --ReleaseApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --ReleaseApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --ReleaseApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --ReleaseApp.exchange_directory=<Unicode>
        Default: '/srv/nbgrader/exchange'
        The nbgrader exchange directory writable to everyone. MUST be preexisting.
    --ReleaseApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ReleaseApp.force=<Bool>
        Default: False
        Force overwrite existing files in the exchange.
    --ReleaseApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --ReleaseApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --ReleaseApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --ReleaseApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --ReleaseApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --ReleaseApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --ReleaseApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --ReleaseApp.path_includes_course=<Bool>
        Default: False
        Whether the path for fetching/submitting  assignments should be prefixed
        with the course name. If this is `False`, then the path will be something
        like `./ps1`. If this is `True`, then the path will be something like
        `./course123/ps1`.
    --ReleaseApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --ReleaseApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ReleaseApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --ReleaseApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ReleaseApp.timestamp_format=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S %Z'
        Format string for timestamps
    --ReleaseApp.timezone=<Unicode>
        Default: 'UTC'
        Timezone for recording timestamps
    
    ValidateApp options
    -------------------
    --ValidateApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --ValidateApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --ValidateApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ValidateApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --ValidateApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --ValidateApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --ValidateApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --ValidateApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --ValidateApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --ValidateApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --ValidateApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --ValidateApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ValidateApp.from_stdin=<Bool>
        Default: False
        read a single notebook from stdin.
    --ValidateApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --ValidateApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --ValidateApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --ValidateApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --ValidateApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --ValidateApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --ValidateApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --ValidateApp.output_files_dir=<Unicode>
        Default: '{notebook_name}_files'
        Directory to copy extra files (figures) to. '{notebook_name}' in the string
        will be converted to notebook basename
    --ValidateApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --ValidateApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ValidateApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --ValidateApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    QuickStartApp options
    ---------------------
    --QuickStartApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --QuickStartApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --QuickStartApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --QuickStartApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --QuickStartApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --QuickStartApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --QuickStartApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --QuickStartApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --QuickStartApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --QuickStartApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --QuickStartApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --QuickStartApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --QuickStartApp.force=<Bool>
        Default: False
        Whether to overwrite existing files
    --QuickStartApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --QuickStartApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --QuickStartApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --QuickStartApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --QuickStartApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --QuickStartApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --QuickStartApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --QuickStartApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --QuickStartApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --QuickStartApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --QuickStartApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    AutogradeApp options
    --------------------
    --AutogradeApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --AutogradeApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --AutogradeApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --AutogradeApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --AutogradeApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --AutogradeApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --AutogradeApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --AutogradeApp.create_student=<Bool>
        Default: False
        Whether to create the student at runtime if it does not already exist.
    --AutogradeApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --AutogradeApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --AutogradeApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --AutogradeApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --AutogradeApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --AutogradeApp.force=<Bool>
        Default: False
        Whether to overwrite existing assignments/submissions
    --AutogradeApp.from_stdin=<Bool>
        Default: False
        read a single notebook from stdin.
    --AutogradeApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --AutogradeApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --AutogradeApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --AutogradeApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --AutogradeApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --AutogradeApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --AutogradeApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --AutogradeApp.output_files_dir=<Unicode>
        Default: '{notebook_name}_files'
        Directory to copy extra files (figures) to. '{notebook_name}' in the string
        will be converted to notebook basename
    --AutogradeApp.permissions=<Int>
        Default: 0
        Permissions to set on files output by nbgrader. The default is generally
        read-only (444), with the exception of nbgrader assign, in which case the
        user also has write permission.
    --AutogradeApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --AutogradeApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --AutogradeApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --AutogradeApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    CollectApp options
    ------------------
    --CollectApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --CollectApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --CollectApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --CollectApp.cache_directory=<Unicode>
        Default: ''
        Local cache directory for nbgrader submit and nbgrader list. Defaults to
        $JUPYTER_DATA_DIR/nbgrader_cache
    --CollectApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --CollectApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --CollectApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --CollectApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --CollectApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --CollectApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --CollectApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --CollectApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --CollectApp.exchange_directory=<Unicode>
        Default: '/srv/nbgrader/exchange'
        The nbgrader exchange directory writable to everyone. MUST be preexisting.
    --CollectApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --CollectApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --CollectApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --CollectApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --CollectApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --CollectApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --CollectApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --CollectApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --CollectApp.path_includes_course=<Bool>
        Default: False
        Whether the path for fetching/submitting  assignments should be prefixed
        with the course name. If this is `False`, then the path will be something
        like `./ps1`. If this is `True`, then the path will be something like
        `./course123/ps1`.
    --CollectApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --CollectApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --CollectApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --CollectApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --CollectApp.timestamp_format=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S %Z'
        Format string for timestamps
    --CollectApp.timezone=<Unicode>
        Default: 'UTC'
        Timezone for recording timestamps
    --CollectApp.update=<Bool>
        Default: False
        Update existing submissions with ones that have newer timestamps.
    
    FetchApp options
    ----------------
    --FetchApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --FetchApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --FetchApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --FetchApp.cache_directory=<Unicode>
        Default: ''
        Local cache directory for nbgrader submit and nbgrader list. Defaults to
        $JUPYTER_DATA_DIR/nbgrader_cache
    --FetchApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --FetchApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --FetchApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --FetchApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --FetchApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --FetchApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --FetchApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --FetchApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --FetchApp.exchange_directory=<Unicode>
        Default: '/srv/nbgrader/exchange'
        The nbgrader exchange directory writable to everyone. MUST be preexisting.
    --FetchApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FetchApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --FetchApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --FetchApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --FetchApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --FetchApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --FetchApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --FetchApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --FetchApp.path_includes_course=<Bool>
        Default: False
        Whether the path for fetching/submitting  assignments should be prefixed
        with the course name. If this is `False`, then the path will be something
        like `./ps1`. If this is `True`, then the path will be something like
        `./course123/ps1`.
    --FetchApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --FetchApp.replace_missing_files=<Bool>
        Default: False
        Whether to replace missing files on fetch
    --FetchApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FetchApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --FetchApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --FetchApp.timestamp_format=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S %Z'
        Format string for timestamps
    --FetchApp.timezone=<Unicode>
        Default: 'UTC'
        Timezone for recording timestamps
    
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
    
    FeedbackApp options
    -------------------
    --FeedbackApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --FeedbackApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --FeedbackApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --FeedbackApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --FeedbackApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --FeedbackApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --FeedbackApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --FeedbackApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --FeedbackApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --FeedbackApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --FeedbackApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --FeedbackApp.export_format=<Unicode>
        Default: 'html'
        The export format to be used, either one of the built-in formats, or a
        dotted object name that represents the import path for an `Exporter` class
    --FeedbackApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FeedbackApp.force=<Bool>
        Default: False
        Whether to overwrite existing assignments/submissions
    --FeedbackApp.from_stdin=<Bool>
        Default: False
        read a single notebook from stdin.
    --FeedbackApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --FeedbackApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --FeedbackApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --FeedbackApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --FeedbackApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --FeedbackApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --FeedbackApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --FeedbackApp.output_files_dir=<Unicode>
        Default: '{notebook_name}_files'
        Directory to copy extra files (figures) to. '{notebook_name}' in the string
        will be converted to notebook basename
    --FeedbackApp.permissions=<Int>
        Default: 0
        Permissions to set on files output by nbgrader. The default is generally
        read-only (444), with the exception of nbgrader assign, in which case the
        user also has write permission.
    --FeedbackApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --FeedbackApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FeedbackApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --FeedbackApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    FormgradeApp options
    --------------------
    --FormgradeApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --FormgradeApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --FormgradeApp.authenticator_class=<Type>
        Default: 'nbgrader.auth.noauth.NoAuth'
        Authenticator used in all formgrade requests.
    --FormgradeApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --FormgradeApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --FormgradeApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --FormgradeApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --FormgradeApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --FormgradeApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --FormgradeApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --FormgradeApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --FormgradeApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --FormgradeApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FormgradeApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --FormgradeApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --FormgradeApp.ip=<Unicode>
        Default: 'localhost'
        IP address for the server
    --FormgradeApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --FormgradeApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --FormgradeApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --FormgradeApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --FormgradeApp.mathjax_url=<Unicode>
        Default: ''
        URL or local path to mathjax installation. Defaults to the version of
        MathJax included with the Jupyter Notebook.
    --FormgradeApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --FormgradeApp.port=<Int>
        Default: 5000
        Port for the server
    --FormgradeApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --FormgradeApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --FormgradeApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --FormgradeApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    ListApp options
    ---------------
    --ListApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --ListApp.as_json=<Bool>
        Default: False
        Print out assignments as json
    --ListApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --ListApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ListApp.cache_directory=<Unicode>
        Default: ''
        Local cache directory for nbgrader submit and nbgrader list. Defaults to
        $JUPYTER_DATA_DIR/nbgrader_cache
    --ListApp.cached=<Bool>
        Default: False
        List assignments in submission cache.
    --ListApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --ListApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --ListApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --ListApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --ListApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --ListApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --ListApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --ListApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --ListApp.exchange_directory=<Unicode>
        Default: '/srv/nbgrader/exchange'
        The nbgrader exchange directory writable to everyone. MUST be preexisting.
    --ListApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ListApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --ListApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --ListApp.inbound=<Bool>
        Default: False
        List inbound files rather than outbound.
    --ListApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --ListApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --ListApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --ListApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --ListApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --ListApp.path_includes_course=<Bool>
        Default: False
        Whether the path for fetching/submitting  assignments should be prefixed
        with the course name. If this is `False`, then the path will be something
        like `./ps1`. If this is `True`, then the path will be something like
        `./course123/ps1`.
    --ListApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --ListApp.remove=<Bool>
        Default: False
        Remove, rather than list files.
    --ListApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --ListApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --ListApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --ListApp.timestamp_format=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S %Z'
        Format string for timestamps
    --ListApp.timezone=<Unicode>
        Default: 'UTC'
        Timezone for recording timestamps
    
    UpdateApp options
    -----------------
    --UpdateApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --UpdateApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --UpdateApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --UpdateApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --UpdateApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --UpdateApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --UpdateApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --UpdateApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --UpdateApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --UpdateApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --UpdateApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --UpdateApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --UpdateApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --UpdateApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --UpdateApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --UpdateApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --UpdateApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --UpdateApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --UpdateApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --UpdateApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --UpdateApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --UpdateApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --UpdateApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --UpdateApp.validate=<Bool>
        Default: True
        whether to validate metadata after updating it
    
    DbApp options
    -------------
    --DbApp.answer_yes=<Bool>
        Default: False
        Answer yes to any prompts.
    --DbApp.assignment_id=<Unicode>
        Default: ''
        The assignment name. This MUST be specified, either by setting the config
        option, passing an argument on the command line, or using the --assignment
        option on the command line.
    --DbApp.autograded_directory=<Unicode>
        Default: 'autograded'
        The name of the directory that contains assignment submissions after they
        have been autograded. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    --DbApp.config_file=<Unicode>
        Default: ''
        Full path of a config file.
    --DbApp.config_file_name=<Unicode>
        Default: ''
        Specify a config file to load.
    --DbApp.course_directory=<Unicode>
        Default: ''
        The root directory for the course files (that includes the `source`,
        `release`, `submitted`, `autograded`, etc. directories). Defaults to the
        current working directory.
    --DbApp.course_id=<Unicode>
        Default: ''
        A key that is unique per instructor and course. This MUST be specified,
        either by setting the config option, or using the --course option on the
        command line.
    --DbApp.db_assignments=<List>
        Default: []
        A list of assignments that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - name
            - duedate (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Assignment` database model for details on these fields.
    --DbApp.db_students=<List>
        Default: []
        A list of student that will be created in the database. Each item in the
        list should be a dictionary with the following keys:
            - id
            - first_name (optional)
            - last_name (optional)
            - email (optional)
        The values will be stored in the database. Please see the API documentation
        on the `Student` database model for details on these fields.
    --DbApp.db_url=<Unicode>
        Default: ''
        URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
        where <course_directory> is another configurable variable.
    --DbApp.directory_structure=<Unicode>
        Default: '{nbgrader_step}/{student_id}/{assignment_id}'
        Format string for the directory structure that nbgrader works over during
        the grading process. This MUST contain named keys for 'nbgrader_step',
        'student_id', and 'assignment_id'. It SHOULD NOT contain a key for
        'notebook_id', as this will be automatically joined with the rest of the
        path.
    --DbApp.feedback_directory=<Unicode>
        Default: 'feedback'
        The name of the directory that contains assignment feedback after grading
        has been completed. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --DbApp.generate_config=<Bool>
        Default: False
        Generate default config file.
    --DbApp.ignore=<List>
        Default: ['.ipynb_checkpoints', '*.pyc', '__pycache__']
        List of file names or file globs to be ignored when copying directories.
    --DbApp.log_datefmt=<Unicode>
        Default: '%Y-%m-%d %H:%M:%S'
        The date format used by logging formatters for %(asctime)s
    --DbApp.log_format=<Unicode>
        Default: '[%(name)s]%(highlevel)s %(message)s'
        The Logging format template
    --DbApp.log_level=<Enum>
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --DbApp.logfile=<Unicode>
        Default: '.nbgrader.log'
        Name of the logfile to log to.
    --DbApp.notebook_id=<Unicode>
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
    --DbApp.release_directory=<Unicode>
        Default: 'release'
        The name of the directory that contains the version of the assignment that
        will be released to students. This corresponds to the `nbgrader_step`
        variable in the `directory_structure` config option.
    --DbApp.source_directory=<Unicode>
        Default: 'source'
        The name of the directory that contains the master/instructor version of
        assignments. This corresponds to the `nbgrader_step` variable in the
        `directory_structure` config option.
    --DbApp.student_id=<Unicode>
        Default: '*'
        File glob to match student IDs. This can be changed to filter by student.
        Note: this is always changed to '.' when running `nbgrader assign`, as the
        assign step doesn't have any student ID associated with it.
    --DbApp.submitted_directory=<Unicode>
        Default: 'submitted'
        The name of the directory that contains assignments that have been submitted
        by students for grading. This corresponds to the `nbgrader_step` variable in
        the `directory_structure` config option.
    
    LateSubmissionPlugin options
    ----------------------------
    --LateSubmissionPlugin.penalty_method=<Enum>
        Default: 'none'
        Choices: ('none', 'zero')
        The method for assigning late submission penalties:
            'none': do nothing (no penalty assigned)
            'zero': assign an overall score of zero (penalty = score)
    
    ExportPlugin options
    --------------------
    --ExportPlugin.to=<Unicode>
        Default: ''
        destination to export to
    
    CsvExportPlugin options
    -----------------------
    --CsvExportPlugin.to=<Unicode>
        Default: ''
        destination to export to
    
    AssignLatePenalties options
    ---------------------------
    --AssignLatePenalties.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --AssignLatePenalties.plugin_class=<Type>
        Default: 'nbgrader.plugins.latesubmission.LateSubmissionPlugin'
        The plugin class for assigning the late penalty for each notebook.
    
    IncludeHeaderFooter options
    ---------------------------
    --IncludeHeaderFooter.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --IncludeHeaderFooter.footer=<Unicode>
        Default: ''
        Path to footer notebook
    --IncludeHeaderFooter.header=<Unicode>
        Default: ''
        Path to header notebook
    
    LockCells options
    -----------------
    --LockCells.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --LockCells.lock_all_cells=<Bool>
        Default: False
        Whether all assignment cells are locked (non-deletable and non-editable)
    --LockCells.lock_grade_cells=<Bool>
        Default: True
        Whether grade cells are locked (non-deletable)
    --LockCells.lock_readonly_cells=<Bool>
        Default: True
        Whether readonly cells are locked (non-deletable and non-editable)
    --LockCells.lock_solution_cells=<Bool>
        Default: True
        Whether solution cells are locked (non-deletable and non-editable)
    
    ClearSolutions options
    ----------------------
    --ClearSolutions.begin_solution_delimeter=<Unicode>
        Default: 'BEGIN SOLUTION'
        The delimiter marking the beginning of a solution
    --ClearSolutions.code_stub=<Dict>
        Default: {'python': '# YOUR CODE HERE\nraise NotImplementedError()'}
        The code snippet that will replace code solutions
    --ClearSolutions.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --ClearSolutions.end_solution_delimeter=<Unicode>
        Default: 'END SOLUTION'
        The delimiter marking the end of a solution
    --ClearSolutions.enforce_metadata=<Bool>
        Default: True
        Whether or not to complain if cells containing solutions regions are not
        marked as solution cells. WARNING: this will potentially cause things to
        break if you are using the full nbgrader pipeline. ONLY disable this option
        if you are only ever planning to use nbgrader assign.
    --ClearSolutions.text_stub=<Unicode>
        Default: 'YOUR ANSWER HERE'
        The text snippet that will replace written solutions
    
    SaveAutoGrades options
    ----------------------
    --SaveAutoGrades.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    DisplayAutoGrades options
    -------------------------
    --DisplayAutoGrades.as_json=<Bool>
        Default: False
        Print out validation results as json
    --DisplayAutoGrades.changed_warning=<Unicode>
        Default: "THE CONTENTS OF {num_changed} TEST CELL(S) HAVE CHANGED!\nTh...
        Warning to display when a cell has changed.
    --DisplayAutoGrades.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --DisplayAutoGrades.failed_warning=<Unicode>
        Default: 'VALIDATION FAILED ON {num_failed} CELL(S)! If you submit\nyo...
        Warning to display when a cell fails.
    --DisplayAutoGrades.ignore_checksums=<Bool>
        Default: False
        Don't complain if cell checksums have changed (if they are locked cells) or
        haven't changed (if they are solution cells)
    --DisplayAutoGrades.indent=<Unicode>
        Default: '    '
        A string containing whitespace that will be used to indent code and errors
    --DisplayAutoGrades.invert=<Bool>
        Default: False
        Complain when cells pass, rather than fail.
    --DisplayAutoGrades.passed_warning=<Unicode>
        Default: 'NOTEBOOK PASSED ON {num_passed} CELL(S)!\n'
        Warning to display when a cell passes (when invert=True)
    --DisplayAutoGrades.width=<Int>
        Default: 90
        Maximum line width for displaying code/errors
    
    ComputeChecksums options
    ------------------------
    --ComputeChecksums.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    SaveCells options
    -----------------
    --SaveCells.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    OverwriteCells options
    ----------------------
    --OverwriteCells.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    CheckCellMetadata options
    -------------------------
    --CheckCellMetadata.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    Execute options
    ---------------
    --Execute.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --Execute.execute_retries=<Int>
        Default: 0
        The number of times to try re-executing the notebook before throwing an
        error. Generally, this shouldn't need to be set, but might be useful for CI
        environments when tests are flaky.
    --Execute.extra_arguments=<List>
        Default: []
        A list of extra arguments to pass to the kernel. For python kernels, this
        defaults to ``--HistoryManager.hist_file=:memory:``. For other kernels this
        is just an empty list.
    --Execute.kernel_manager_class=<Type>
        Default: 'jupyter_client.manager.KernelManager'
        The kernel manager class to use.
    --Execute.kernel_name=<Unicode>
        Default: ''
        Name of kernel to use to execute the cells. If not set, use the kernel_spec
        embedded in the notebook.
    --Execute.shutdown_kernel=<Enum>
        Default: 'graceful'
        Choices: ['graceful', 'immediate']
        If `graceful` (default), then the kernel is given time to clean up after
        executing all cells, e.g., to execute its `atexit` hooks. If `immediate`,
        then the kernel is signaled to immediately terminate.
    --Execute.timeout=<Int>
        Default: 30
        The time to wait (in seconds) for output from executions. If a cell
        execution takes longer, an exception (TimeoutError on python 3+,
        RuntimeError on python 2) is raised.
        `None` or `-1` will disable the timeout. If `timeout_func` is set, it
        overrides `timeout`.
    --Execute.timeout_func=<Any>
        Default: None
        A callable which, when given the cell source as input, returns the time to
        wait (in seconds) for output from cell executions. If a cell execution takes
        longer, an exception (TimeoutError on python 3+, RuntimeError on python 2)
        is raised.
        Returning `None` or `-1` will disable the timeout for the cell. Not setting
        `timeout_func` will cause the preprocessor to default to using the `timeout`
        trait for all cells. The `timeout_func` trait overrides `timeout` if it is
        not `None`.
    
    GetGrades options
    -----------------
    --GetGrades.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    ClearOutput options
    -------------------
    --ClearOutput.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    LimitOutput options
    -------------------
    --LimitOutput.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    --LimitOutput.max_lines=<Int>
        Default: 1000
        maximum number of lines of output (-1 means no limit)
    --LimitOutput.max_traceback=<Int>
        Default: 100
        maximum number of traceback lines (-1 means no limit)
    
    DeduplicateIds options
    ----------------------
    --DeduplicateIds.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    Examples
    --------
    
        The nbgrader application is a system for assigning and grading notebooks.
        Each subcommand of this program corresponds to a different step in the
        grading process. In order to facilitate the grading pipeline, nbgrader
        places some constraints on how the assignments must be structured. By
        default, the directory structure for the assignments must look like this:
        
            {nbgrader_step}/{student_id}/{assignment_id}/{notebook_id}.ipynb
        
        where 'nbgrader_step' is the step in the nbgrader pipeline, 'student_id'
        is the ID of the student, 'assignment_id' is the name of the assignment,
        and 'notebook_id' is the name of the notebook (excluding the extension).
        For example, when running `nbgrader autograde "Problem Set 1"`, the
        autograder will first look for all notebooks for all students in the
        following directories:
        
            submitted/*/Problem Set 1/*.ipynb
        
        and it will write the autograded notebooks to the corresponding directory
        and filename for each notebook and each student:
        
            autograded/{student_id}/Problem Set 1/{notebook_id}.ipynb
        
        These variables, as well as the overall directory structure, can be
        configured through the `NbGrader` class (run `nbgrader --help-all`
        to see these options).
        
        For more details on how each of the subcommands work, please see the help
        for that command (e.g. `nbgrader assign --help-all`).
    
    