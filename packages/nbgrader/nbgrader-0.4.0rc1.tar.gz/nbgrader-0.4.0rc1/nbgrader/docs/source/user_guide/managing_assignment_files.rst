
Managing assignment files
=========================

Distributing assignments to students and collecting them can be a
logistical nightmare. If you are running nbgrader on a server, some of
this pain can be relieved by relying on nbgrader's built-in
functionality for releasing and collecting assignments on the
instructor's side, and fetching and submitting assignments on the
student's side.

.. contents:: Table of Contents
   :depth: 2

Releasing assignments
---------------------

.. seealso::

    :doc:`creating_and_grading_assignments`
        Details on generating assignments

    :doc:`/command_line_tools/nbgrader-release`
        Command line options for ``nbgrader release``

    :doc:`/command_line_tools/nbgrader-list`
        Command line options for ``nbgrader list``

    :doc:`philosophy`
        More details on how the nbgrader hierarchy is structured.

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

After an assignment has been created using ``nbgrader assign``, the
instructor must actually release that assignment to students. If the
class is being taught on a single filesystem, then the instructor may
use ``nbgrader release`` to copy the assignment files to a shared
location on the filesystem for students to then download.

First, we must specify a few configuration options. We'll need to use
these a few times, so we'll create a ``nbgrader_config.py`` file that
will get automatically loaded when we run ``nbgrader``:

.. code:: 

    %%file nbgrader_config.py
    
    c = get_config()
    
    c.NbGrader.course_id = "example_course"
    c.TransferApp.exchange_directory = "/tmp/exchange"


.. parsed-literal::

    Overwriting nbgrader_config.py


In the config file, we've specified the "exchange" directory to be
``/tmp/exchange``. This directory must exist before running
``nbgrader``, and it *must* be readable and writable by all users, so
we'll first create it and configure the appropriate permissions:

.. code:: 

    %%bash
    
    # remove existing directory, so we can start fresh for demo purposes
    rm -rf /tmp/exchange
    
    # create the exchange directory, with write permissions for everyone
    mkdir /tmp/exchange
    chmod ugo+rw /tmp/exchange

Now that we have the directory created, we can actually run
``nbgrader release`` (and as with the other nbgrader commands for
instructors, this must be run from the root of the course directory):

.. code:: 

    %%bash
    
    nbgrader release "ps1"


.. parsed-literal::

    [ReleaseApp | INFO] Source: /Users/jhamrick/project/tools/nbgrader/nbgrader/docs/source/user_guide/release/./ps1
    [ReleaseApp | INFO] Destination: /tmp/exchange/example_course/outbound/ps1
    [ReleaseApp | INFO] Released as: example_course ps1


Finally, you can verify that the assignment has been appropriately
released by running the ``nbgrader list`` command:

.. code:: 

    %%bash
    
    nbgrader list


.. parsed-literal::

    [ListApp | INFO] Released assignments:
    [ListApp | INFO] example_course ps1


Note that there should only ever be *one* instructor who runs the
``nbgrader release`` and ``nbgrader collect`` commands (and there should
probably only be one instructor -- the same instructor -- who runs
``nbgrader assign``, ``nbgrader autograde`` and ``nbgrader formgrade``
as well). However this does not mean that only one instructor can do the
grading, it just means that only one instructor manages the assignment
files. Other instructors can still perform grading by accessing the
formgrader URL.

.. _fetching-assignments:

Fetching assignments
--------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-fetch`
        Command line options for ``nbgrader fetch``

    :doc:`/command_line_tools/nbgrader-list`
        Command line options for ``nbgrader list``

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

From the student's perspective, they can list what assignments have been
released, and then fetch a copy of the assignment to work on. First,
we'll create a temporary directory to represent the student's home
directory:

.. code:: 

    %%bash
    
    # remove the fake student home directory if it exists, for demo purposes
    rm -rf /tmp/student_home
    
    # create the fake student home directory and switch to it
    mkdir /tmp/student_home

If you are not using the default exchange directory (as is the case
here), you will additionally need to provide your students with a
configuration file that sets the appropriate directory for them:

.. code:: 

    %%file /tmp/student_home/nbgrader_config.py
    
    c = get_config()
    c.TransferApp.exchange_directory = '/tmp/exchange'
    c.NbGrader.course_id = "example_course"


.. parsed-literal::

    Writing /tmp/student_home/nbgrader_config.py


From the command line
~~~~~~~~~~~~~~~~~~~~~

From the student's perspective, they can see what assignments have been
released using ``nbgrader list``, and passing the name of the class:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader list


.. parsed-literal::

    [ListApp | INFO] Released assignments:
    [ListApp | INFO] example_course ps1


They can then fetch an assignment for that class using
``nbgrader fetch`` and passing the name of the class and the name of the
assignment:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader fetch "ps1"


.. parsed-literal::

    [FetchApp | INFO] Source: /tmp/exchange/example_course/outbound/ps1
    [FetchApp | INFO] Destination: /private/tmp/student_home/ps1
    [FetchApp | INFO] Fetched as: example_course ps1


Note that running ``nbgrader fetch`` copies the assignment files from
the exchange directory to the local directory, and therefore can be used
from any directory:

.. code:: 

    %%bash
    
    ls -l "/tmp/student_home/ps1"


.. parsed-literal::

    total 40
    -rw-r--r--  1 jhamrick  wheel  5733 Jan 14 16:37 jupyter.png
    -rw-r--r--  1 jhamrick  wheel  8034 Jan 14 16:37 problem1.ipynb
    -rw-r--r--  1 jhamrick  wheel  2187 Jan 14 16:37 problem2.ipynb


Additionally, the ``nbgrader fetch`` (as well as ``nbgrader submit``)
command also does not rely on having access to the nbgrader database --
the database is only used by instructors.

From the notebook dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

  The "Assignment List" extension is not fully compatible with multiple
  courses on the same server. Please see :ref:`multiple-classes` for details.

Alternatively, students can fetch assignments using the assignment list notebook server extension. You must have installed the extension by following the instructions :doc:`here </user_guide/installation>`, after which you should see an "Assignments" tab in dashboard:

.. figure:: images/assignment_list_released.png
   :alt: 

The image above shows that there has been one assignment released
("ps1") for the class "example\_course". To get this assignment,
students can click the "Fetch" button (analogous to running
``nbgrader fetch ps1 --course example_course``. **Note: this assumes
nbgrader is always run from the root of the notebook server, which on
JupyterHub is most likely the root of the user's home directory.**

After the assignment is fetched, it will appear in the list of
"Downloaded assignments":

.. figure:: images/assignment_list_downloaded.png
   :alt: 

Students can click on the name of the assignment to expand it and see
all the notebooks in the assignment:

.. figure:: images/assignment_list_downloaded_expanded.png
   :alt: 

Clicking on a particular notebook will open it in a new tab in the
browser.

Submitting assignments
----------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-submit`
        Command line options for ``nbgrader fetch``

    :doc:`/command_line_tools/nbgrader-list`
        Command line options for ``nbgrader list``

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

From the command line
~~~~~~~~~~~~~~~~~~~~~

First, as a reminder, here is what the student's ``nbgrader_config.py``
file looks like:

.. code:: 

    %%bash
    
    cat /tmp/student_home/nbgrader_config.py


.. parsed-literal::

    
    c = get_config()
    c.TransferApp.exchange_directory = '/tmp/exchange'
    c.NbGrader.course_id = "example_course"

After working on an assignment, the student can submit their version for
grading using ``nbgrader submit`` and passing the name of the assignment
and the name of the class:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader submit "ps1"


.. parsed-literal::

    [SubmitApp | INFO] Source: /private/tmp/student_home/ps1
    [SubmitApp | INFO] Destination: /tmp/exchange/example_course/inbound/jhamrick+ps1+2017-01-15 00:37:46 UTC
    [SubmitApp | INFO] Submitted as: example_course ps1 2017-01-15 00:37:46 UTC


Note that "the name of the assignment" really corresponds to "the name
of a folder". It just happens that, in our current directory, there is a
folder called "ps1":

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    ls -l "/tmp/student_home"


.. parsed-literal::

    total 8
    drwxr-xr-x  3 jhamrick  wheel  102 Jan 14 16:37 Library
    -rw-r--r--  1 jhamrick  wheel  108 Jan 14 16:37 nbgrader_config.py
    drwxr-xr-x  5 jhamrick  wheel  170 Jan 14 16:37 ps1


Students can see what assignments they have submitted using
``nbgrader list --inbound``:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader list --inbound


.. parsed-literal::

    [ListApp | INFO] Submitted assignments:
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:46 UTC


Importantly, students can run ``nbgrader submit`` as many times as they
want, and all submitted copies of the assignment will be preserved:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader submit "ps1"


.. parsed-literal::

    [SubmitApp | INFO] Source: /private/tmp/student_home/ps1
    [SubmitApp | INFO] Destination: /tmp/exchange/example_course/inbound/jhamrick+ps1+2017-01-15 00:37:49 UTC
    [SubmitApp | INFO] Submitted as: example_course ps1 2017-01-15 00:37:49 UTC


We can see all versions that have been submitted by again running
``nbgrader list --inbound``:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader list --inbound


.. parsed-literal::

    [ListApp | INFO] Submitted assignments:
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:46 UTC
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:49 UTC


Note that the ``nbgrader submit`` (as well as ``nbgrader fetch``)
command also does not rely on having access to the nbgrader database --
the database is only used by instructors.

``nbgrader`` requires that the submitted notebook names match the
released notebook names for each assignment. For example if a student
were to rename one of the given assignment notebooks:

.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    # assume the student renamed the assignment file
    mv ps1/problem1.ipynb ps1/myproblem1.ipynb
    
    nbgrader submit "ps1"


.. parsed-literal::

    [SubmitApp | INFO] Source: /private/tmp/student_home/ps1
    [SubmitApp | INFO] Destination: /tmp/exchange/example_course/inbound/jhamrick+ps1+2017-01-15 00:37:51 UTC
    [SubmitApp | WARNING] Possible missing notebooks and/or extra notebooks submitted for assignment ps1:
        Expected:
        	problem1.ipynb: MISSING
        	problem2.ipynb: FOUND
        Submitted:
        	myproblem1.ipynb: EXTRA
        	problem2.ipynb: OK
    [SubmitApp | INFO] Submitted as: example_course ps1 2017-01-15 00:37:51 UTC


By default this assignment will still be submitted however only the
"FOUND" notebooks (for the given assignment) can be ``autograded`` and
will appear on the ``formgrade`` extension. "EXTRA" notebooks will not
be ``autograded`` and will not appear on the ``formgrade`` extension.

To ensure that students cannot submit an assignment with missing
notebooks (for a given assignment) the ``strict`` option, in the
student's ``nbgrader_config.py`` file, can be set to ``True``:

.. code:: 

    %%file /tmp/student_home/nbgrader_config.py
    
    c = get_config()
    c.TransferApp.exchange_directory = '/tmp/exchange'
    c.NbGrader.course_id = "example_course"
    c.SubmitApp.strict = True


.. parsed-literal::

    Overwriting /tmp/student_home/nbgrader_config.py


.. code:: 

    %%bash
    export HOME=/tmp/student_home && cd $HOME
    
    nbgrader submit "ps1"


.. parsed-literal::

    [SubmitApp | INFO] Source: /private/tmp/student_home/ps1
    [SubmitApp | INFO] Destination: /tmp/exchange/example_course/inbound/jhamrick+ps1+2017-01-15 00:37:53 UTC
    [SubmitApp | ERROR] Assignment ps1 not submitted. There are missing notebooks for the submission:
        Expected:
        	problem1.ipynb: MISSING
        	problem2.ipynb: FOUND
        Submitted:
        	myproblem1.ipynb: EXTRA
        	problem2.ipynb: OK


From the notebook dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

  The "Assignment List" extension is not fully compatible with multiple
  courses on the same server. Please see :ref:`multiple-classes` for details.

Alternatively, students can submit assignments using the assignment list notebook server extension. You must have installed the extension by following the instructions `here <https://github.com/jupyter/nbgrader>`__. Students must have also downloaded the assignments (see :ref:`fetching-assignments`).

After students have worked on the assignment for a while, but before
submitting, they can validate that their notebooks pass the tests by
clicking the "Validate" button (analogous to running
``nbgrader validate``). If any tests fail, they will see a warning:

.. figure:: images/assignment_list_validate_failed.png
   :alt: 

If there are no errors, they will see that the validation passes:

.. figure:: images/assignment_list_validate_succeeded.png
   :alt: 

Once students have validated all the notebooks, they can click the
"Submit" button to submit the assignment (analogous to running
``nbgrader submit ps1 --course example_course``). Afterwards, it will
show up in the list of submitted assignments (and also still in the list
of downloaded assignments):

.. figure:: images/assignment_list_submitted.png
   :alt: 

Students may submit an assignment as many times as they'd like. All
copies of a submission will show up in the submitted assignments list,
and when the instructor collects the assignments, they will get the most
recent version of the assignment:

.. figure:: images/assignment_list_submitted_again.png
   :alt: 

Similarly, if the ``strict`` option (in the student's
``nbgrader_config.py`` file) is set to ``True``, the students will not
be able to submit an assignment with missing notebooks (for a given
assignment):

.. figure:: images/assignment_list_submit_error.jpg
   :alt: 

Collecting assignments
----------------------

.. seealso::

    :doc:`/command_line_tools/nbgrader-collect`
        Command line options for ``nbgrader fetch``

    :doc:`/command_line_tools/nbgrader-list`
        Command line options for ``nbgrader list``

    :doc:`philosophy`
        More details on how the nbgrader hierarchy is structured.

    :doc:`/configuration/config_options`
        Details on ``nbgrader_config.py``

First, as a reminder, here is what the instructor's
``nbgrader_config.py`` file looks like:

.. code:: 

    %%bash
    
    cat nbgrader_config.py


.. parsed-literal::

    
    c = get_config()
    
    c.NbGrader.course_id = "example_course"
    c.TransferApp.exchange_directory = "/tmp/exchange"

After students have submitted their assignments, the instructor can view
what has been submitted with ``nbgrader list --inbound``:

.. code:: 

    %%bash
    
    nbgrader list --inbound


.. parsed-literal::

    [ListApp | INFO] Submitted assignments:
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:46 UTC
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:49 UTC
    [ListApp | INFO] example_course jhamrick ps1 2017-01-15 00:37:51 UTC


The instructor can then collect all submitted assignments with
``nbgrader collect`` and passing the name of the assignment (and as with
the other nbgrader commands for instructors, this must be run from the
root of the course directory):

.. code:: 

    %%bash
    
    nbgrader collect "ps1"


.. parsed-literal::

    [CollectApp | INFO] Collecting submission: jhamrick ps1


This will copy the student submissions to the ``submitted`` folder in a
way that is automatically compatible with ``nbgrader autograde``:

.. code:: 

    %%bash
    
    ls -l submitted


.. parsed-literal::

    total 0
    drwxr-xr-x  3 jhamrick  staff  102 Sep 25 17:38 bitdiddle
    drwxr-xr-x  3 jhamrick  staff  102 Sep 25 17:38 hacker
    drwxr-xr-x  3 jhamrick  staff  102 Jan 14 16:37 jhamrick


Note that there should only ever be *one* instructor who runs the
``nbgrader release`` and ``nbgrader collect`` commands (and there should
probably only be one instructor -- the same instructor -- who runs
``nbgrader assign``, ``nbgrader autograde`` and ``nbgrader formgrade``
as well). However this does not mean that only one instructor can do the
grading, it just means that only one instructor manages the assignment
files. Other instructors can still perform grading by accessing the
formgrader URL.
