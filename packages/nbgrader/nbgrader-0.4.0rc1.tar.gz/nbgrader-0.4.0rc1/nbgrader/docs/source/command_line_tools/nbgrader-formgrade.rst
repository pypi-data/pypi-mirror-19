
nbgrader formgrade
==================

::

    Grade a notebook using an HTML form
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --debug
        set log level to DEBUG (maximize logging output)
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
    --port=<Int> (FormgradeApp.port)
        Default: 5000
        Port for the server
    --ip=<Unicode> (FormgradeApp.ip)
        Default: 'localhost'
        IP address for the server
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
    
    HTMLExporter options
    --------------------
    --HTMLExporter.default_preprocessors=<List>
        Default: ['nbconvert.preprocessors.ClearOutputPreprocessor', 'nbconver...
        List of preprocessors available by default, by name, namespace,  instance,
        or type.
    --HTMLExporter.file_extension=<FilenameExtension>
        Default: '.txt'
        Extension of the file that should be written to disk
    --HTMLExporter.filters=<Dict>
        Default: {}
        Dictionary of filters, by name and namespace, to add to the Jinja
        environment.
    --HTMLExporter.preprocessors=<List>
        Default: []
        List of preprocessors, by name or namespace, to enable.
    --HTMLExporter.raw_mimetypes=<List>
        Default: []
        formats of raw cells to be included in this Exporter's output.
    --HTMLExporter.template_extension=<Unicode>
        Default: '.tpl'
    --HTMLExporter.template_file=<Unicode>
        Default: ''
        Name of the template file to use
    --HTMLExporter.template_path=<List>
        Default: ['.']
    
    Examples
    --------
    
        Run the formgrader server application in order to manually grade
        submissions that have already been autograded. Running the formgrader
        allows *any* submission (from any assignment, for any student) to be
        graded, as long as it has already been run through the autograder.
        
        By default, the formgrader runs at http://localhost:5000. It also starts
        a Jupyter notebook server, to allow students' notebooks to be open up
        and run manually if so desired. The notebook server also runs on
        localhost on a random port, though this port can be specified by setting
        `FormgradeApp.nbserver_port`. The notebook server can be disabled entirely
        by setting `FormgradeApp.start_nbserver=False`.
        
        The formgrader must be run from the root of a nbgrader-compatible directory
        structure, which by default looks like:
        
            autograded/{student_id}/{assignment_id}/{notebook_id}.ipynb
        
        To run the formgrader on the default IP and port:
            nbgrader formgrade
        
        To run the formgrader on a public-facing IP address:
            nbgrader formgrade --ip 0.0.0.0
        
        To run the formgrader a different port:
            nbgrader formgrade --port 5001
    
    