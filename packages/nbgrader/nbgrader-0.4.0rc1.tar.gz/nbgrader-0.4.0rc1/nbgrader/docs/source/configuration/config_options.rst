
Configuration options
=====================

These options can be set in ``nbgrader_config.py``, or at the command
line when you start it.

Note: the ``nbgrader_config.py`` file can be either located in the same
directory as where you are running the nbgrader commands (which is most
likely the root of your course directory), or you can place it in one of
a number of locations on your system. These locations correspond to the
configuration directories that Jupyter itself looks in; you can find out
what these are by running ``jupyter --paths``.




Application.log_datefmt : Unicode
    Default: ``'%Y-%m-%d %H:%M:%S'``

    The date format used by logging formatters for %(asctime)s

Application.log_format : Unicode
    Default: ``'[%(name)s]%(highlevel)s %(message)s'``

    The Logging format template

Application.log_level : 0|10|20|30|40|50|'DEBUG'|'INFO'|'WARN'|'ERROR'|'CRITICAL'
    Default: ``30``

    Set the log level by value or name.

JupyterApp.answer_yes : Bool
    Default: ``False``

    Answer yes to any prompts.

JupyterApp.config_file : Unicode
    Default: ``''``

    Full path of a config file.

JupyterApp.config_file_name : Unicode
    Default: ``''``

    Specify a config file to load.

JupyterApp.generate_config : Bool
    Default: ``False``

    Generate default config file.

NbGrader.assignment_id : Unicode
    Default: ``''``

    
    The assignment name. This MUST be specified, either by setting the
    config option, passing an argument on the command line, or using the
    --assignment option on the command line.


NbGrader.autograded_directory : Unicode
    Default: ``'autograded'``

    
    The name of the directory that contains assignment submissions after
    they have been autograded. This corresponds to the `nbgrader_step`
    variable in the `directory_structure` config option.


NbGrader.course_directory : Unicode
    Default: ``''``

    
    The root directory for the course files (that includes the `source`,
    `release`, `submitted`, `autograded`, etc. directories). Defaults to
    the current working directory.


NbGrader.course_id : Unicode
    Default: ``''``

    
    A key that is unique per instructor and course. This MUST be
    specified, either by setting the config option, or using the
    --course option on the command line.


NbGrader.db_assignments : List
    Default: ``[]``

    
    A list of assignments that will be created in the database. Each
    item in the list should be a dictionary with the following keys:
    
        - name
        - duedate (optional)
    
    The values will be stored in the database. Please see the API
    documentation on the `Assignment` database model for details on
    these fields.


NbGrader.db_students : List
    Default: ``[]``

    
    A list of student that will be created in the database. Each
    item in the list should be a dictionary with the following keys:
    
        - id
        - first_name (optional)
        - last_name (optional)
        - email (optional)
    
    The values will be stored in the database. Please see the API
    documentation on the `Student` database model for details on
    these fields.


NbGrader.db_url : Unicode
    Default: ``''``

    
    URL to the database. Defaults to sqlite:///<course_directory>/gradebook.db,
    where <course_directory> is another configurable variable.


NbGrader.directory_structure : Unicode
    Default: ``'{nbgrader_step}/{student_id}/{assignment_id}'``

    
    Format string for the directory structure that nbgrader works
    over during the grading process. This MUST contain named keys for
    'nbgrader_step', 'student_id', and 'assignment_id'. It SHOULD NOT
    contain a key for 'notebook_id', as this will be automatically joined
    with the rest of the path.


NbGrader.feedback_directory : Unicode
    Default: ``'feedback'``

    
    The name of the directory that contains assignment feedback after
    grading has been completed. This corresponds to the `nbgrader_step`
    variable in the `directory_structure` config option.


NbGrader.ignore : List
    Default: ``['.ipynb_checkpoints', '*.pyc', '__pycache__']``

    
    List of file names or file globs to be ignored when copying directories.


NbGrader.logfile : Unicode
    Default: ``'.nbgrader.log'``

    
    Name of the logfile to log to.


NbGrader.notebook_id : Unicode
    Default: ``'*'``

    
    File glob to match notebook names, excluding the '.ipynb' extension.
    This can be changed to filter by notebook.


NbGrader.release_directory : Unicode
    Default: ``'release'``

    
    The name of the directory that contains the version of the
    assignment that will be released to students. This corresponds to
    the `nbgrader_step` variable in the `directory_structure` config
    option.


NbGrader.source_directory : Unicode
    Default: ``'source'``

    
    The name of the directory that contains the master/instructor
    version of assignments. This corresponds to the `nbgrader_step`
    variable in the `directory_structure` config option.


NbGrader.student_id : Unicode
    Default: ``'*'``

    
    File glob to match student IDs. This can be changed to filter by
    student. Note: this is always changed to '.' when running `nbgrader
    assign`, as the assign step doesn't have any student ID associated
    with it.


NbGrader.submitted_directory : Unicode
    Default: ``'submitted'``

    
    The name of the directory that contains assignments that have been
    submitted by students for grading. This corresponds to the
    `nbgrader_step` variable in the `directory_structure` config option.



ExportApp.plugin_class : Type
    Default: ``'nbgrader.plugins.export.CsvExportPlugin'``

    The plugin class for exporting the grades.

NbConvertApp.export_format : Unicode
    Default: ``'html'``

    The export format to be used, either one of the built-in formats,
    or a dotted object name that represents the import path for an
    `Exporter` class

NbConvertApp.from_stdin : Bool
    Default: ``False``

    read a single notebook from stdin.

NbConvertApp.notebooks : List
    Default: ``[]``

    List of notebooks to convert.
    Wildcards are supported.
    Filenames passed positionally will be added to the list.


NbConvertApp.output_base : Unicode
    Default: ``''``

    overwrite base name use for output files.
    can only be used when converting one notebook at a time.


NbConvertApp.output_files_dir : Unicode
    Default: ``'{notebook_name}_files'``

    Directory to copy extra files (figures) to.
    '{notebook_name}' in the string will be converted to notebook
    basename

NbConvertApp.postprocessor_class : DottedOrNone
    Default: ``''``

    PostProcessor class used to write the
    results of the conversion

NbConvertApp.use_output_suffix : Bool
    Default: ``True``

    Whether to apply a suffix prior to the extension (only relevant
    when converting to notebook format). The suffix is determined by
    the exporter, and is usually '.nbconvert'.

NbConvertApp.writer_class : DottedObjectName
    Default: ``'FilesWriter'``

    Writer class used to write the 
    results of the conversion

BaseNbConvertApp.force : Bool
    Default: ``False``

    Whether to overwrite existing assignments/submissions

BaseNbConvertApp.permissions : Int
    Default: ``0``

    
    Permissions to set on files output by nbgrader. The default is generally
    read-only (444), with the exception of nbgrader assign, in which case the
    user also has write permission.


AssignApp.create_assignment : Bool
    Default: ``False``

    
    Whether to create the assignment at runtime if it does not
    already exist.


AssignApp.no_database : Bool
    Default: ``False``

    
    Do not save information about the assignment into the database.



TransferApp.cache_directory : Unicode
    Default: ``''``

    Local cache directory for nbgrader submit and nbgrader list. Defaults to $JUPYTER_DATA_DIR/nbgrader_cache

TransferApp.exchange_directory : Unicode
    Default: ``'/srv/nbgrader/exchange'``

    The nbgrader exchange directory writable to everyone. MUST be preexisting.

TransferApp.path_includes_course : Bool
    Default: ``False``

    
    Whether the path for fetching/submitting  assignments should be
    prefixed with the course name. If this is `False`, then the path
    will be something like `./ps1`. If this is `True`, then the path
    will be something like `./course123/ps1`.


TransferApp.timestamp_format : Unicode
    Default: ``'%Y-%m-%d %H:%M:%S %Z'``

    Format string for timestamps

TransferApp.timezone : Unicode
    Default: ``'UTC'``

    Timezone for recording timestamps

ReleaseApp.force : Bool
    Default: ``False``

    Force overwrite existing files in the exchange.


QuickStartApp.force : Bool
    Default: ``False``

    Whether to overwrite existing files

AutogradeApp.create_student : Bool
    Default: ``False``

    
    Whether to create the student at runtime if it does not
    already exist.


CollectApp.update : Bool
    Default: ``False``

    Update existing submissions with ones that have newer timestamps.

FetchApp.replace_missing_files : Bool
    Default: ``False``

    Whether to replace missing files on fetch

SubmitApp.strict : Bool
    Default: ``False``

    Whether or not to submit the assignment if there are missing notebooks from the released assignment notebooks.


FormgradeApp.authenticator_class : Type
    Default: ``'nbgrader.auth.noauth.NoAuth'``

    Authenticator used in all formgrade requests.

FormgradeApp.ip : Unicode
    Default: ``'localhost'``

    IP address for the server

FormgradeApp.mathjax_url : Unicode
    Default: ``''``

    
    URL or local path to mathjax installation. Defaults to the version
    of MathJax included with the Jupyter Notebook.


FormgradeApp.port : Int
    Default: ``5000``

    Port for the server

ListApp.as_json : Bool
    Default: ``False``

    Print out assignments as json

ListApp.cached : Bool
    Default: ``False``

    List assignments in submission cache.

ListApp.inbound : Bool
    Default: ``False``

    List inbound files rather than outbound.

ListApp.remove : Bool
    Default: ``False``

    Remove, rather than list files.

UpdateApp.validate : Bool
    Default: ``True``

    whether to validate metadata after updating it



LateSubmissionPlugin.penalty_method : 'none'|'zero'
    Default: ``'none'``

    
    The method for assigning late submission penalties:
        'none': do nothing (no penalty assigned)
        'zero': assign an overall score of zero (penalty = score)


ExportPlugin.to : Unicode
    Default: ``''``

    destination to export to


NbConvertBase.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

NbConvertBase.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``

    
    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


Preprocessor.enabled : Bool
    Default: ``False``

    No description

NbGraderPreprocessor.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running nbgrader

AssignLatePenalties.plugin_class : Type
    Default: ``'nbgrader.plugins.latesubmission.LateSubmissionPlugin'``

    The plugin class for assigning the late penalty for each notebook.

IncludeHeaderFooter.footer : Unicode
    Default: ``''``

    Path to footer notebook

IncludeHeaderFooter.header : Unicode
    Default: ``''``

    Path to header notebook

LockCells.lock_all_cells : Bool
    Default: ``False``

    Whether all assignment cells are locked (non-deletable and non-editable)

LockCells.lock_grade_cells : Bool
    Default: ``True``

    Whether grade cells are locked (non-deletable)

LockCells.lock_readonly_cells : Bool
    Default: ``True``

    Whether readonly cells are locked (non-deletable and non-editable)

LockCells.lock_solution_cells : Bool
    Default: ``True``

    Whether solution cells are locked (non-deletable and non-editable)

ClearSolutions.begin_solution_delimeter : Unicode
    Default: ``'BEGIN SOLUTION'``

    The delimiter marking the beginning of a solution

ClearSolutions.code_stub : Dict
    Default: ``{'python': '# YOUR CODE HERE\\nraise NotImplementedError()'}``

    The code snippet that will replace code solutions

ClearSolutions.end_solution_delimeter : Unicode
    Default: ``'END SOLUTION'``

    The delimiter marking the end of a solution

ClearSolutions.enforce_metadata : Bool
    Default: ``True``

    
    Whether or not to complain if cells containing solutions regions are
    not marked as solution cells. WARNING: this will potentially cause
    things to break if you are using the full nbgrader pipeline. ONLY
    disable this option if you are only ever planning to use nbgrader
    assign.


ClearSolutions.text_stub : Unicode
    Default: ``'YOUR ANSWER HERE'``

    The text snippet that will replace written solutions


DisplayAutoGrades.as_json : Bool
    Default: ``False``

    Print out validation results as json

DisplayAutoGrades.changed_warning : Unicode
    Default: ``"THE CONTENTS OF {num_changed} TEST CELL(S) HAVE CHANGED!\\nTh...``

    Warning to display when a cell has changed.

DisplayAutoGrades.failed_warning : Unicode
    Default: ``'VALIDATION FAILED ON {num_failed} CELL(S)! If you submit\\nyo...``

    Warning to display when a cell fails.

DisplayAutoGrades.ignore_checksums : Bool
    Default: ``False``

    
    Don't complain if cell checksums have changed (if they are locked
    cells) or haven't changed (if they are solution cells)


DisplayAutoGrades.indent : Unicode
    Default: ``'    '``

    A string containing whitespace that will be used to indent code and errors

DisplayAutoGrades.invert : Bool
    Default: ``False``

    Complain when cells pass, rather than fail.

DisplayAutoGrades.passed_warning : Unicode
    Default: ``'NOTEBOOK PASSED ON {num_passed} CELL(S)!\\n'``

    Warning to display when a cell passes (when invert=True)

DisplayAutoGrades.width : Int
    Default: ``90``

    Maximum line width for displaying code/errors





ExecutePreprocessor.allow_errors : Bool
    Default: ``False``

    
    If `False` (default), when a cell raises an error the
    execution is stopped and a `CellExecutionError`
    is raised.
    If `True`, execution errors are ignored and the execution
    is continued until the end of the notebook. Output from
    exceptions is included in the cell output in both cases.


ExecutePreprocessor.interrupt_on_timeout : Bool
    Default: ``False``

    
    If execution of a cell times out, interrupt the kernel and
    continue executing other cells rather than throwing an error and
    stopping.


ExecutePreprocessor.kernel_manager_class : Type
    Default: ``'jupyter_client.manager.KernelManager'``

    The kernel manager class to use.

ExecutePreprocessor.kernel_name : Unicode
    Default: ``''``

    
    Name of kernel to use to execute the cells.
    If not set, use the kernel_spec embedded in the notebook.


ExecutePreprocessor.raise_on_iopub_timeout : Bool
    Default: ``False``

    
    If `False` (default), then the kernel will continue waiting for
    iopub messages until it receives a kernel idle message, or until a
    timeout occurs, at which point the currently executing cell will be
    skipped. If `True`, then an error will be raised after the first
    timeout. This option generally does not need to be used, but may be
    useful in contexts where there is the possibility of executing
    notebooks with memory-consuming infinite loops.


ExecutePreprocessor.shutdown_kernel : 'graceful'|'immediate'
    Default: ``'graceful'``

    
    If `graceful` (default), then the kernel is given time to clean
    up after executing all cells, e.g., to execute its `atexit` hooks.
    If `immediate`, then the kernel is signaled to immediately
    terminate.


ExecutePreprocessor.timeout : Int
    Default: ``30``

    
    The time to wait (in seconds) for output from executions.
    If a cell execution takes longer, an exception (TimeoutError
    on python 3+, RuntimeError on python 2) is raised.
    
    `None` or `-1` will disable the timeout. If `timeout_func` is set,
    it overrides `timeout`.


ExecutePreprocessor.timeout_func : Any
    Default: ``None``

    
    A callable which, when given the cell source as input,
    returns the time to wait (in seconds) for output from cell
    executions. If a cell execution takes longer, an exception
    (TimeoutError on python 3+, RuntimeError on python 2) is
    raised.
    
    Returning `None` or `-1` will disable the timeout for the cell.
    Not setting `timeout_func` will cause the preprocessor to
    default to using the `timeout` trait for all cells. The
    `timeout_func` trait overrides `timeout` if it is not `None`.


Execute.execute_retries : Int
    Default: ``0``

    
    The number of times to try re-executing the notebook before throwing
    an error. Generally, this shouldn't need to be set, but might be useful
    for CI environments when tests are flaky.


Execute.extra_arguments : List
    Default: ``[]``

    
    A list of extra arguments to pass to the kernel. For python kernels,
    this defaults to ``--HistoryManager.hist_file=:memory:``. For other
    kernels this is just an empty list.





LimitOutput.max_lines : Int
    Default: ``1000``

    maximum number of lines of output (-1 means no limit)

LimitOutput.max_traceback : Int
    Default: ``100``

    maximum number of traceback lines (-1 means no limit)

