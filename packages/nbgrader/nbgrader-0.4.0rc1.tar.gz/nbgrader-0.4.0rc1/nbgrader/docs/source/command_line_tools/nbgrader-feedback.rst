
nbgrader feedback
=================

::

    Generate feedback from a graded notebook
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --debug
        set log level to DEBUG (maximize logging output)
    --force
        Overwrite an assignment/submission if it already exists.
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
    
    GetGrades options
    -----------------
    --GetGrades.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    CSSHTMLHeaderPreprocessor options
    ---------------------------------
    --CSSHTMLHeaderPreprocessor.default_language=<Unicode>
        Default: 'ipython'
        Deprecated default highlight language as of 5.0, please use language_info
        metadata instead
    --CSSHTMLHeaderPreprocessor.display_data_priority=<List>
        Default: ['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...
        An ordered list of preferred output type, the first encountered will usually
        be used when converting discarding the others.
    --CSSHTMLHeaderPreprocessor.enabled=<Bool>
        Default: False
    --CSSHTMLHeaderPreprocessor.highlight_class=<Unicode>
        Default: '.highlight'
        CSS highlight class identifier
    
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
    
        Create HTML feedback for students after all the grading is finished.
        This takes a single parameter, which is the assignment ID, and then (by
        default) looks at the following directory structure:
        
            autograded/*/{assignment_id}/*.ipynb
        
        from which it generates feedback the the corresponding directories
        according to:
        
            feedback/{student_id}/{assignment_id}/{notebook_id}.html
        
        Running `nbgrader feedback` requires that `nbgrader autograde` (and most
        likely `nbgrader formgrade`) have been run and that all grading is
        complete.
        
        To generate feedback for all submissions for "Problem Set 1":
            nbgrader feedback "Problem Set 1"
        
        To generate feedback only for the student with ID 'Hacker':
            nbgrader feedback "Problem Set 1" --student Hacker
        
        To feedback for only the notebooks that start with '1':
            nbgrader feedback "Problem Set 1" --notebook "1*"
    
    