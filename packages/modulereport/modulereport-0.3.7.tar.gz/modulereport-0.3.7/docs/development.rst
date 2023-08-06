===========
Development
===========


Pull Requests
-------------

- Submit Pull Requests against the `master` branch.
- Provide a good description of what you're doing and why.
- Provide tests that cover your changes and try to run the tests locally first.

**Example**.
Assuming you set up GitHub account, forked modulereport repository from
https://github.com/berrak/modulereport to your own page
via web interface, and your fork is located at https://github.com/<your-github-user-name>/modulereport

::

    $ git clone git@github.com:modulereport/modulereport.git
    $ cd modulereport
    # ...
    $ git diff
    $ git add <modified>
    $ git status
    $ git commit

You may reference relevant issues in commit messages (like #113) to
make GitHub link issues and commits together, and with phrase like
"fixes #113" you can even close relevant issues automatically. Now
push the changes to your fork::

  $ git push git@github.com:<your-github-user-name>/modulereport.git

Open Pull Requests page at https://github.com/<your-github-user-name>/modulereport/pulls and
click "New pull request". That's it.


Running tests
-------------

Ways to run the tests locally:

::

    $ make lint         # ensure code follow best practices
    $ make test         # runs all unittests
    $ make coverage     # runs coverage on code
    $ make report       # makes a nice html page of coverage result

Lint (flake8) may complain for great many details, but ``make test`` will
not run without clean code.

It can be configured to ignore certain codes in ``setup.cfg`` configuration file:

::

    [flake8]
    # it's not a bug, ignore:
    # H101: Use TODO(NAME)
    # H301: one import per line
    ignore = H101,H301


Getting involved
----------------

The Module Reporter welcomes help in the following ways:

- Making Pull Requests for code, tests, or docs.
- Commenting on open issues and pull requests.

