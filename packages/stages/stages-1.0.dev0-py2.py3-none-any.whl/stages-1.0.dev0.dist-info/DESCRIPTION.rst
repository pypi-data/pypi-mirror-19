
stages
~~~~~~

Simple command line tool to run scripts in a sequential manner, written in pure Python.
Basically this script is a very primitive version of what tools like `Jenkins`_ do.
If Jenkins seems like overkill for your needs or you have lots of manual steps interleaved in your automated process, chances are you might find this script useful.

Here a small example of of how to use it in an interpreter session::

    >>> from stages import Runner
    >>> runner = Runner("config_file", heading="Example run")
    >>> runner.run()

Want to read more, found a bug or you want to contribute? Visit the `GitHub repo`_

.. _Jenkins: https://jenkins.io/index.html
.. _GitHub repo: https://github.com/TobiasPleyer/pystages


