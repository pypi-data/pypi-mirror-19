
nbgrader validate
=================

::

    Validate a notebook by running it
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --invert
        Complain when cells pass, rather than vice versa.
    --json
        Print out validation results as json.
    
    Class parameters
    ----------------
    
    Parameters are set from command-line arguments of the form:
    `--Class.trait=value`. This line is evaluated in Python, so simple expressions
    are allowed, e.g.:: `--C.a='range(3)'` For setting C.a=[0,1,2].
    
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
    
    CheckCellMetadata options
    -------------------------
    --CheckCellMetadata.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    ClearOutput options
    -------------------
    --ClearOutput.enabled=<Bool>
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
    
    Examples
    --------
    
        You can run `nbgrader validate` on just a single file, e.g.:
            nbgrader validate "Problem 1.ipynb"
        
        Or, you can run it on multiple files using shell globs:
            nbgrader validate "Problem Set 1/*.ipynb"
        
        If you want to test instead that none of the tests pass (rather than that
        all of the tests pass, which is the default), you can use --invert:
            nbgrader validate --invert "Problem 1.ipynb"
    
    