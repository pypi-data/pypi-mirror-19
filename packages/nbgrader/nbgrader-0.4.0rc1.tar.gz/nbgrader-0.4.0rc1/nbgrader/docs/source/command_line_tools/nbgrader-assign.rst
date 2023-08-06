
nbgrader assign
===============

::

    Produce the version of an assignment to be released to students.
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --force
        Overwrite an assignment/submission if it already exists.
    --create
        Create an entry for the assignment in the database, if one does not already exist.
    --no-metadata
        Do not validate or modify cell metatadata.
    --quiet
        set log level to CRITICAL (minimize logging output)
    --debug
        set log level to DEBUG (maximize logging output)
    --no-db
        Do not save information into the database.
    --notebook=<Unicode> (NbGrader.notebook_id)
        Default: '*'
        File glob to match notebook names, excluding the '.ipynb' extension. This
        can be changed to filter by notebook.
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
    
    ClearOutput options
    -------------------
    --ClearOutput.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    CheckCellMetadata options
    -------------------------
    --CheckCellMetadata.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
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
    
    CheckCellMetadata options
    -------------------------
    --CheckCellMetadata.enabled=<Bool>
        Default: True
        Whether to use this preprocessor when running nbgrader
    
    Examples
    --------
    
        Produce the version of the assignment that is intended to be released to
        students. This performs several modifications to the original assignment:
        
            1. It inserts a header and/or footer to each notebook in the
               assignment, if the header/footer are specified.
        
            2. It locks certain cells so that they cannot be deleted by students
               accidentally (or on purpose!)
        
            3. It removes solutions from the notebooks and replaces them with
               code or text stubs saying (for example) "YOUR ANSWER HERE".
        
            4. It clears all outputs from the cells of the notebooks.
        
            5. It saves information about the cell contents so that we can warn
               students if they have changed the tests, or if they have failed
               to provide a response to a written answer. Specifically, this is
               done by computing a checksum of the cell contents and saving it
               into the cell metadata.
        
            6. It saves the tests used to grade students' code into a database,
               so that those tests can be replaced during autograding if they
               were modified by the student (you can prevent this by passing the
               --no-db flag).
        
               Additionally, the assignment must already be present in the
               database. To create it while running `nbgrader assign` if it
               doesn't already exist, pass the --create flag.
        
        `nbgrader assign` takes one argument (the name of the assignment), and
        looks for notebooks in the 'source' directory by default, according to
        the directory structure specified in `NbGrader.directory_structure`.
        The student version is then saved into the 'release' directory.
        
        Note that the directory structure requires the `student_id` to be given;
        however, there is no student ID at this point in the process. Instead,
        `nbgrader assign` sets the student ID to be '.' so by default, files are
        read in according to:
        
            source/./{assignment_id}/{notebook_id}.ipynb
        
        and saved according to:
        
            release/./{assignment_id}/{notebook_id}.ipynb
    
    