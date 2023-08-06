
Creating and grading assignments
================================

.. contents:: Table of Contents
   :depth: 2

Developing assignments with the assignment toolbar
--------------------------------------------------

**Note**: As you are developing your assignments, you should save them
into the ``source/{assignment_id}/`` folder of the nbgrader hierarchy,
where ``assignment_id`` is the name of the assignment you are creating
(e.g. "ps1").

.. seealso::

    :doc:`philosophy`
        More details on how the nbgrader hierarchy is structured.
        
    :doc:`/configuration/student_version`
        Instructions for customizing how the student version of the assignment looks.

Before you can begin developing assignments, you will need to actually
install the nbgrader toolbar. If you do not have it installed, please
first follow the :doc:`installation instructions <installation>`.

Once the toolbar has been installed, you should see it in the drop down
"Cell toolbar" menu:

.. figure:: images/assignment_toolbar.png
   :alt: 

Selecting the "Create Assignment" toolbar will create a separate toolbar
for each cell which by default will be a dropdown menu with the "-" item
selected. For markdown cells, there are two additional options to choose
from, either "Manually graded answer" or "Read-only":

.. figure:: images/markdown_cell.png
   :alt: 

For code cells, there are four options to choose from, including
"Manually graded answer", "Autograded answer", "Autograder tests", and
"Read-only":

.. figure:: images/code_cell.png
   :alt: 

The following sections go into detail about the different cell types,
and show cells that are taken from a complete example of an assignment
generated with the nbgrader toolbar extension:

-  `source/ps1/problem1.ipynb <source/ps1/problem1.html>`__
-  `source/ps1/problem2.ipynb <source/ps1/problem2.html>`__

.. _manually-graded-cells:

"Manually graded answer" cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you select the "Manually graded answer" option (available for both
markdown and code cells), the nbgrader extension will mark that cell as
a cell that contains an answer that must be manually graded by a human
grader. Here is an example of a manually graded answer cell:

.. figure:: images/manually_graded_answer.png
   :alt: 

The most common use case for this type of cell is for written
free-response answers (for example, which interpret the results of code
that may have been written and/or executed above).

When you specify a manually graded answer, you must additionally tell nbgrader how many points the answer is worth, and an id for the cell. Additionally, when creating the release version of the assignment (see :ref:`assign-and-release-an-assignment`), the bodies of answer cells will be replaced with a code or text stub indicating to the students that they should put their answer or solution there. Please see :doc:`/configuration/student_version` for details on how to customize this behavior.

*Note: the blue border only shows up when the nbgrader extension toolbar
is active; it will not be visible to students.*

.. _autograded-answer-cells:

"Autograded answer" cells
~~~~~~~~~~~~~~~~~~~~~~~~~

If you select the "Autograded answer" option (available only for code
cells), the nbgrader extension will mark that cell as a cell that
contains an answer which will be autograded. Here is an example of an
autograded graded answer cell:

.. figure:: images/autograded_answer.png
   :alt: 

As shown in the image above, solutions can be specified inline, through the use of a special syntax such as ``### BEGIN SOLUTION`` and ``### END SOLUTION``. When creating the release version (see :ref:`assign-and-release-an-assignment`), the region between the special syntax lines will be replaced with a code stub. If this special syntax is not used, then the entire contents of the cell will be replaced with the code stub. Please see :doc:`/configuration/student_version` for details on how to customize this behavior.

Unlike manually graded answers, autograded answers aren't worth any
points: instead, the points for autograded answers are specified for the
particular tests that grade those answers. See the next section for
further details.

*Note: the blue border only shows up when the nbgrader extension toolbar
is active; it will not be visible to students.*

"Autograder tests" cells
~~~~~~~~~~~~~~~~~~~~~~~~

If you select the "Autograder tests" option (available only for code
cells), the nbgrader extension will mark that cell as a cell that
contains tests to be run during autograding. Here is an example of two
test cells:

.. figure:: images/autograder_tests.png
   :alt: 

Test cells should contain ``assert`` statements (or similar). When run through ``nbgrader autograde`` (see :ref:`autograde-assignments`), the cell will pass if no errors are raised, and fail otherwise. You must specify the number of points that each test cell is worth; then, if the tests pass during autograding, students will receive the specified number of points, and otherwise will receive zero points.

The lock icon on the left side of the cell toolbar indicates that the
tests are "read-only". See the next section for further details on what
this means.

For tips on writing autograder tests, see :ref:`autograding-resources`.

*Note: the blue border only shows up when the nbgrader extension toolbar
is active; it will not be visible to students.*

.. _read-only-cells:

"Read-only" cells
~~~~~~~~~~~~~~~~~

If you select the "Read-only" option (available for both code and
markdown cells), the nbgrader extension will mark that cell as one that
cannot be modified. This is indicated by a lock icon on the left side of
the cell toolbar:

.. figure:: images/read_only.png
   :alt: 

However, this doesn't actually mean that it is truly read-only when opened in the notebook. Instead, what is means is that during the ``nbgrader assign`` step (see :ref:`assign-and-release-an-assignment`), the source of these cells will be recorded into the database. Then, during the ``nbgrader autograde`` step (see :ref:`autograde-assignments`), nbgrader will check whether the source of the student's version of the cell has changed. If it has, it will replace the cell's source with the version in the database, thus effectively overwriting any changes the student made.

.. versionadded:: 0.4.0
    Read-only cells (and test cells) are now truly read-only! However, at the moment this functionality will only work on the master version of the notebook (5.0.0.dev).

This functionality is particularly important for test cells, which are
always marked as read-only. Because the mechanism for autograding is
that students receive full credit if the tests pass, an easy way to get
around this would be to simply delete or comment out the tests. This
read-only functionality will reverse any such changes made by the
student.

.. _assign-and-release-an-assignment:

Assign and release an assignment
--------------------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-assign`
        Command line options for ``nbgrader assign``
        
    :doc:`philosophy`
        Details about how the directory hierarchy is structured

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

After an assignment has been created with the assignment toolbar, you will want to create a release version of the assignment for the students.

As described in :doc:`philosophy`, you need to organize your files in a particular way. For releasing assignments, you should have the master copy of your files saved (by default) in the following source directory structure:

::

    {course_directory}/source/{assignment_id}/{notebook_id}.ipynb

Note: The ``student_id`` is not included here because the source and
release versions of the assignment are the same for all students.

After running ``nbgrader assign``, the release version of the notebooks
will be:

::

    {course_directory}/release/{assignment_id}/{notebook_id}.ipynb

As a reminder, the instructor is responsible for distributing this
release version to their students using their institution's existing
student communication and document distribution infrastructure.

Workflow example: Instructor generating an assignment release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example walks an instructor through the workflow for generating an
assignment and preparing it for release to students:

1. Add problem set to the source folder
2. Verify that the tests pass in the instructor version
3. Configure assignments and students in the config file
4. Assign a problem set using nbgrader
5. Inspect the release folder
6. Verify that the tests fail in the student version
7. Release files to students

1. Add problem set to the source folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To simplify this example, two notebooks of the assignment have already
been stored in the ``source/ps1`` folder:

-  `source/ps1/problem1.ipynb <source/ps1/problem1.html>`__
-  `source/ps1/problem2.ipynb <source/ps2/problem2.html>`__

2. Verify that the tests pass in the instructor version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ideally, the solutions in the instructor version should be correct and
pass all the test cases to ensure that you are giving your students
tests that they can actually pass. To verify this is the case, run:

.. code:: 

    %%bash
    
    nbgrader validate source/ps1/*.ipynb


.. parsed-literal::

    Success! Your notebook passes all the tests.
    Success! Your notebook passes all the tests.


If the notebook passes all the test cases, you should see the message
"Success! Your notebook passes all the tests."

3. Configure assignments and students in the config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Creating a ``nbgrader_config.py`` file and configuring the list of your
assignments is the first workflow step to create a release version of an
assignment. These assignments will be automatically added to the sqlite
database ``gradebook.db``. If this database does not already exist,
nbgrader will automatically create it. By default, the nbgrader commands
(like ``nbgrader assign``) will assume that this database is called
``gradebook.db`` and that it lives in the root of your course directory,
though its name and path can be configured in ``nbgrader_config.py``.

.. code:: 

    %%file nbgrader_config.py
    
    c = get_config()
    c.NbGrader.db_assignments = [dict(name="ps1", duedate="2015-02-02 17:00:00 UTC")]
    c.NbGrader.db_students = [
        dict(id="bitdiddle", first_name="Ben", last_name="Bitdiddle"),
        dict(id="hacker", first_name="Alyssa", last_name="Hacker")
    ]


.. parsed-literal::

    Writing nbgrader_config.py


You can also add students and assignments to the database using the
``nbgrader db`` command line tool:

.. code:: 

    %%bash
    
    nbgrader db student add reasoner --last-name=Reasoner --first-name=Louis
    nbgrader db assignment add ps2


.. parsed-literal::

    [DbStudentAddApp | INFO] Creating/updating student with ID 'reasoner': {'last_name': 'Reasoner', 'email': None, 'first_name': 'Louis'}
    [DbAssignmentAddApp | INFO] Creating/updating assignment with ID 'ps2': {'duedate': None}


See the documentation on :doc:`managing_the_database` for more details.

4. Assign a problem set using nbgrader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that the gradebook is set up, run ``nbgrader assign``. When running
``nbgrader assign``, the assignment name (which is "ps1") is passed. We
also specify a *header* notebook (``source/header.ipynb``) to prepend at
the beginning of each notebook in the assignment. By default, this
command should be run from the root of the course directory:

.. code:: 

    %%bash
    
    nbgrader assign "ps1" --IncludeHeaderFooter.header=source/header.ipynb


.. parsed-literal::

    [AssignApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/source/./ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/release/./ps1/jupyter.png
    [AssignApp | INFO] Updating/creating assignment 'ps1': {'duedate': '2015-02-02 17:00:00 UTC'}
    [AssignApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/source/./ps1/problem1.ipynb to notebook
    [AssignApp | INFO] Writing 8034 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/release/./ps1/problem1.ipynb
    [AssignApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/source/./ps1/problem2.ipynb to notebook
    [AssignApp | INFO] Writing 2187 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/release/./ps1/problem2.ipynb
    [AssignApp | INFO] Setting destination file permissions to 644


5. Inspect the release folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Upon completion of ``nbgrader assign`` in the previous step, there will
be a new folder called ``release`` with the same structure as
``source``. The ``release`` folder contains the actual release version
of the assignment files:

-  `release/ps1/problem1.ipynb <release/ps1/problem1.html>`__
-  `release/ps1/problem2.ipynb <release/ps1/problem2.html>`__

6. Verify that the tests fail in the student version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ideally, all the tests should fail in the student version if the student
hasn't implemented anything. To verify that this is in fact the case, we
can use the ``nbgrader validate --invert`` command:

.. code:: 

    %%bash
    
    nbgrader validate --invert release/ps1/*.ipynb


.. parsed-literal::

    Success! The notebook does not pass any tests.
    Success! The notebook does not pass any tests.


If the notebook fails all the test cases, you should see the message
"Success! The notebook does not pass any tests."

7. Release files to students
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At this point you will be able to take the files in the ``release`` folder and distribute them to students. If you are using nbgrader in a shared server environment, you can do this with the ``nbgrader release`` command (see :doc:`managing_assignment_files`). Otherwise, you will need to do this manually:

**Please note**: Students must use version 3 or greater of the
IPython/Jupyter notebook for nbgrader to work properly. If they are not
using version 3 or greater, it is possible for them to delete cells that
contain important metadata for nbgrader. With version 3 or greater,
there is a feature in the notebook that prevents cells from being
deleted. See `this
issue <https://github.com/jupyter/nbgrader/issues/424>`__ for more
details.

To ensure that students have a recent enough version of the notebook,
you can include a cell such as the following in each notebook of the
assignment:

.. code:: python

    import IPython
    assert IPython.version_info[0] >= 3, "Your version of IPython is too old, please update it."

.. _autograde-assignments:

Autograde assignments
---------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-autograde`
        Command line options for ``nbgrader autograde``
        
    :doc:`philosophy`
        Details about how the directory hierarchy is structured

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

After assignments have been submitted by students, you will want to save them into a ``submitted`` directory. As described in :doc:`philosophy`, you need to organize your files in a particular way. For autograding assignments, you should have the submitted versions of students' assignments organized as follows:

::

    submitted/{student_id}/{assignment_id}/{notebook_id}.ipynb

After running ``nbgrader autograde``, the autograded version of the
notebooks will be:

::

    autograded/{student_id}/{assignment_id}/{notebook_id}.ipynb

Workflow example: Instructor autograding assignments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following example, we have an assignment with two notebooks.
There are two submissions of the assignment:

Submission 1:

-  `submitted/bitdiddle/ps1/problem1.ipynb <submitted/bitdiddle/ps1/problem1.html>`__
-  `submitted/bitdiddle/ps1/problem2.ipynb <submitted/bitdiddle/ps1/problem2.html>`__

Submission 2:

-  `submitted/hacker/ps1/problem1.ipynb <submitted/hacker/ps1/problem1.html>`__
-  `submitted/hacker/ps1/problem2.ipynb <submitted/hacker/ps1/problem2.html>`__

Before we can actually start grading, we need to actually specify who
the students are. We did this earlier in the ``nbgrader_config.py``
file, where we also specified the list of assignments:

.. code:: 

    !cat nbgrader_config.py


.. parsed-literal::

    
    c = get_config()
    c.NbGrader.db_assignments = [dict(name="ps1", duedate="2015-02-02 17:00:00 UTC")]
    c.NbGrader.db_students = [
        dict(id="bitdiddle", first_name="Ben", last_name="Bitdiddle"),
        dict(id="hacker", first_name="Alyssa", last_name="Hacker")
    ]

Once the config file has been set up with the students, we can run the
autograder (and as with the other nbgrader commands for instructors,
this must be run from the root of the course directory):

.. code:: 

    %%bash
    
    nbgrader autograde "ps1"


.. parsed-literal::

    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/jupyter.png
    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/timestamp.txt -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/timestamp.txt
    [AutogradeApp | INFO] Creating/updating student with ID 'bitdiddle': {'first_name': 'Ben', 'last_name': 'Bitdiddle'}
    [AutogradeApp | INFO] SubmittedAssignment<ps1 for bitdiddle> submitted at 2015-02-02 22:58:23.948203
    [AutogradeApp | WARNING] SubmittedAssignment<ps1 for bitdiddle> is 21503.948203 seconds late
    [AutogradeApp | INFO] Overwriting files with master versions from the source directory
    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/source/./ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/jupyter.png
    [AutogradeApp | INFO] Sanitizing /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/problem1.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/problem1.ipynb to notebook
    [AutogradeApp | WARNING] Attribute 'checksum' for cell correct_squares has changed! (should be: 8f41dd0f9c8fd2da8e8708d73e506b3a, got: 845d4666cabb30b6c75fc534f7375bf5)
    [AutogradeApp | WARNING] Attribute 'checksum' for cell squares_invalid_input has changed! (should be: 23c2b667d3b60eff3be46eb3290a6b4a, got: 123394e73f33a622ec057e2eae51a54a)
    [AutogradeApp | INFO] Writing 8093 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem1.ipynb
    [AutogradeApp | INFO] Autograding /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem1.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem1.ipynb to notebook
    [AutogradeApp | INFO] Executing notebook with kernel: python
    [AutogradeApp | WARNING] SubmittedAssignment<ps1 for bitdiddle> is 21503.948203 seconds late
    [AutogradeApp | INFO] Using late submission penalty method: none
    [AutogradeApp | WARNING] Late submission penalty: None
    [AutogradeApp | INFO] Writing 13509 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem1.ipynb
    [AutogradeApp | INFO] Sanitizing /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/problem2.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/bitdiddle/ps1/problem2.ipynb to notebook
    [AutogradeApp | INFO] Writing 2228 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem2.ipynb
    [AutogradeApp | INFO] Autograding /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem2.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem2.ipynb to notebook
    [AutogradeApp | INFO] Executing notebook with kernel: python
    [AutogradeApp | WARNING] SubmittedAssignment<ps1 for bitdiddle> is 21503.948203 seconds late
    [AutogradeApp | INFO] Using late submission penalty method: none
    [AutogradeApp | WARNING] Late submission penalty: None
    [AutogradeApp | INFO] Writing 2225 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem2.ipynb
    [AutogradeApp | INFO] Setting destination file permissions to 444
    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/jupyter.png
    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/timestamp.txt -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/timestamp.txt
    [AutogradeApp | INFO] Creating/updating student with ID 'hacker': {'first_name': 'Alyssa', 'last_name': 'Hacker'}
    [AutogradeApp | INFO] SubmittedAssignment<ps1 for hacker> submitted at 2015-02-01 17:28:58.749302
    [AutogradeApp | INFO] Overwriting files with master versions from the source directory
    [AutogradeApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/source/./ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/jupyter.png
    [AutogradeApp | INFO] Sanitizing /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/problem1.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/problem1.ipynb to notebook
    [AutogradeApp | INFO] Writing 8830 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem1.ipynb
    [AutogradeApp | INFO] Autograding /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem1.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem1.ipynb to notebook
    [AutogradeApp | INFO] Executing notebook with kernel: python
    [AutogradeApp | INFO] Writing 9460 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem1.ipynb
    [AutogradeApp | INFO] Sanitizing /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/problem2.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/submitted/hacker/ps1/problem2.ipynb to notebook
    [AutogradeApp | INFO] Writing 2358 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem2.ipynb
    [AutogradeApp | INFO] Autograding /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem2.ipynb
    [AutogradeApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem2.ipynb to notebook
    [AutogradeApp | INFO] Executing notebook with kernel: python
    [AutogradeApp | INFO] Writing 2355 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem2.ipynb
    [AutogradeApp | INFO] Setting destination file permissions to 444


When grading the submission for ``Bitdiddle``, you'll see some warnings
that look like "Checksum for grade cell correct\_squares has changed!".
What's happening here is that nbgrader has recorded what the *original*
contents of the grade cell ``correct_squares`` (when ``nbgrader assign``
was run), and is checking the submitted version against this original
version. It has found that the submitted version changed (perhaps this
student tried to cheat by commenting out the failing tests), and has
therefore overwritten the submitted version of the tests with the
original version of the tests.

You may also notice that there is a note saying "ps1 for Bitdiddle is
21503.948203 seconds late". What is happening here is that nbgrader is
detecting a file in Bitdiddle's submission called ``timestamp.txt``,
reading in that timestamp, and saving it into the database. From there,
it can compare the timestamp to the duedate of the problem set, and
compute whether the submission is at all late.

Once the autograding is complete, there will be new directories for the
autograded versions of the submissions:

Autograded submission 1:

-  `autograded/bitdiddle/ps1/problem1.ipynb <autograded/bitdiddle/ps1/problem1.html>`__
-  `autograded/bitdiddle/ps1/problem2.ipynb <autograded/bitdiddle/ps1/problem2.html>`__

Autograded submission 2:

-  `autograded/hacker/ps1/problem1.ipynb <autograded/hacker/ps1/problem1.html>`__
-  `autograded/hacker/ps1/problem2.ipynb <autograded/hacker/ps1/problem2.html>`__

Manual grading and formgrade
----------------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-formgrade`
        Command line options for ``nbgrader formgrade``

    :doc:`philosophy`
        More details on how the nbgrader hierarchy is structured.

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

After assignments have been autograded, they will saved into an ``autograded`` directory (see :doc:`philosophy` for details):

After running ``nbgrader autograde``, the autograded version of the
notebooks will be:

::

    autograded/{student_id}/{assignment_id}/{notebook_id}.ipynb

To grade the assignments with an HTML form, all we have to do is run:

.. code:: bash

    nbgrader formgrade

This will launch a server at ``http://localhost:5000`` that will provide you with an interface for hand grading assignments that it finds in the directory listed above. Note that this applies to *all* assignments as well -- as long as the autograder has been run on the assignment (see :ref:`autograde-assignments`), it will be available for manual grading via the formgrader.

The formgrader doesn't actually modify the files on disk at all; it only
modifies information about them in the database. So, there is no
"output" step for the formgrader.

Important note: if you run the formgrader on a public IP address and port (for example, by running ``nbgrader formgrade --ip=<public_ip>``), then *anyone* will be able to access the formgrader at its URL! So, you probably want to only run the formgrader on a private network that only the instructors have access to (e.g., behind a VPN). Alternately, if students are accessing their notebooks via JupyterHub, then you can configure the formgrader to authenticate users through JupyterHub so that only specified graders may access the formgrader. See :doc:`/configuration/jupyterhub_config` for more details.

Feedback on assignments
-----------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-feedback`
        Command line options for ``nbgrader feedback``
        
    :doc:`philosophy`
        Details about how the directory hierarchy is structured

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

After assignments have been autograded and/or manually graded, they will located in the `autograded` directory (see :doc:`philosophy` for details):

::

    autograded/{student_id}/{assignment_id}/{notebook_id}.ipynb

After running ``nbgrader feedback``, HTML versions of these notebooks
will be saved to:

::

    feedback/{student_id}/{assignment_id}/{notebook_id}.html

Workflow example: Instructor returning feedback to students
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the following example, we have an assignment with two notebooks.
There are two submissions of the assignment that have been graded:

Autograded submission 1:

-  `autograded/bitdiddle/ps1/problem1.ipynb <autograded/bitdiddle/ps1/problem1.html>`__
-  `autograded/bitdiddle/ps1/problem2.ipynb <autograded/bitdiddle/ps1/problem2.html>`__

Autograded submission 2:

-  `autograded/hacker/ps1/problem1.ipynb <autograded/hacker/ps1/problem1.html>`__
-  `autograded/hacker/ps1/problem2.ipynb <autograded/hacker/ps1/problem2.html>`__

Generating feedback is fairly straightforward (and as with the other
nbgrader commands for instructors, this must be run from the root of the
course directory):

.. code:: 

    %%bash
    
    nbgrader feedback "ps1"


.. parsed-literal::

    [FeedbackApp | WARNING] Config option `display_data_priority` not recognized by `GetGrades`.
    [FeedbackApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/bitdiddle/ps1/jupyter.png
    [FeedbackApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/timestamp.txt -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/bitdiddle/ps1/timestamp.txt
    [FeedbackApp | WARNING] Config option `display_data_priority` not recognized by `GetGrades`.
    [FeedbackApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem1.ipynb to html
    [FeedbackApp | INFO] Writing 274746 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/bitdiddle/ps1/problem1.html
    [FeedbackApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/bitdiddle/ps1/problem2.ipynb to html
    [FeedbackApp | INFO] Writing 253697 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/bitdiddle/ps1/problem2.html
    [FeedbackApp | INFO] Setting destination file permissions to 444
    [FeedbackApp | WARNING] Config option `display_data_priority` not recognized by `GetGrades`.
    [FeedbackApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/jupyter.png -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/hacker/ps1/jupyter.png
    [FeedbackApp | INFO] Copying /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/timestamp.txt -> /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/hacker/ps1/timestamp.txt
    [FeedbackApp | WARNING] Config option `display_data_priority` not recognized by `GetGrades`.
    [FeedbackApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem1.ipynb to html
    [FeedbackApp | INFO] Writing 271053 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/hacker/ps1/problem1.html
    [FeedbackApp | INFO] Converting notebook /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/autograded/hacker/ps1/problem2.ipynb to html
    [FeedbackApp | INFO] Writing 253827 bytes to /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/feedback/hacker/ps1/problem2.html
    [FeedbackApp | INFO] Setting destination file permissions to 444


Once the feedback has been generated, there will be new directories and
HTML files corresponding to each notebook in each submission:

Feedback for submission 1:

-  `feedback/bitdiddle/ps1/problem1.html <feedback/bitdiddle/ps1/problem1.html>`__
-  `feedback/bitdiddle/ps1/problem2.html <feedback/bitdiddle/ps1/problem2.html>`__

Feedback for submission 2:

-  `feedback/hacker/ps1/problem1.html <feedback/hacker/ps1/problem1.html>`__
-  `feedback/hacker/ps1/problem2.html <feedback/hacker/ps1/problem2.html>`__

Getting grades from the database
--------------------------------

.. versionadded:: 0.4.0

.. seealso::

    :doc:`/command_line_tools/nbgrader-export`
        Command line options for ``nbgrader export``
        
    :doc:`/plugins/export-plugin`
        Details on how to write your own custom exporter.

In addition to creating feedback for the students, you may need to
upload grades to whatever learning management system your school uses
(e.g. Canvas, Blackboard, etc.). nbgrader provides a way to export
grades to CSV out of the box, with the ``nbgrader export`` command:

.. code:: 

    %%bash
    
    nbgrader export


.. parsed-literal::

    [ExportApp | INFO] Using exporter: CsvExportPlugin
    [ExportApp | INFO] Exporting grades to grades.csv


After running ``nbgrader export``, you will see the grades in a CSV file
called ``grades.csv``:

.. code:: 

    %%bash
    
    cat grades.csv


.. parsed-literal::

    assignment,duedate,timestamp,student_id,last_name,first_name,email,raw_score,late_submission_penalty,score,max_score
    ps2,,,bitdiddle,Bitdiddle,Ben,,0.0,0.0,0.0,0.0
    ps2,,,hacker,Hacker,Alyssa,,0.0,0.0,0.0,0.0
    ps2,,,reasoner,Reasoner,Louis,,0.0,0.0,0.0,0.0
    ps1,2015-02-02 17:00:00,2015-02-02 22:58:23.948203,bitdiddle,Bitdiddle,Ben,,1.5,0.0,1.5,9.0
    ps1,2015-02-02 17:00:00,2015-02-01 17:28:58.749302,hacker,Hacker,Alyssa,,3.0,0.0,3.0,9.0
    ps1,2015-02-02 17:00:00,,reasoner,Reasoner,Louis,,0.0,0.0,0.0,9.0


If you need to customize how the grades are exported, you can :doc:`write your own exporter </plugins/export-plugin>`.
