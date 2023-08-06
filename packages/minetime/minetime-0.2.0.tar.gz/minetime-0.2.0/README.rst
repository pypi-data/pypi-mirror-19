.. image:: https://badge.fury.io/py/minetime.svg
    :target: https://badge.fury.io/py/minetime

.. image:: https://gitlab.com/yakoi/minetime/badges/master/build.svg
    :target: https://gitlab.com/yakoi/minetime/commits/master

.. image:: https://gitlab.com/yakoi/minetime/badges/master/coverage.svg
    :target: https://gitlab.com/yakoi/minetime/commits/master

minetime
++++++++

Minetime is a command line application to help you collect timelogs and post them to a configured `Redmine <http://www.redmine.org>`_ project management application. minetime can collect timelogs in 4 main ways:

- With one or more --timelog option to import timelogs from the command line.
- With the --batch utt option to import timelogs from specified utt flat file.
- With the --batch gtl option to import timelogs from specified Gtimelog flat file.
- With no special import option, you enter interactive wizard mode, where all information will be prompted by the user. In wizard mode, user gets to select issues from assigned issues and tracked queries.

Multiple timelogs on same issue and date can be auto-magically merged together into a single time entry.

Timelogs times are rounded to the nearest quarter-hour (after merge).

Collected timelogs are kept in memory and always presented for confirmation before transparently beeing posted to configured redmine server via its `REST API <http://www.redmine.org/projects/redmine/wiki/Rest_api>`_, using the `python-redmine <https://github.com/maxtepkeev/python-redmine>`_ library.

`Learn more <https://gitlab.com/yakoi/minetime/blob/master/docs/index.rst>`_.


Quickstart
==========

Installation
------------

::

  # install minetime
  pip install minetime

  # upgrade minetime
  pip install --upgrade minetime

or, without pip, from source:

::

  python setup.py install


Main Configuration File
-----------------------

Default location: ``$HOME/.config/minetime/config.yml``. Format: YAML

The default location may be overwritten by the MINETIME_CONF environment variable.

Here's an example of the main configuration file::

    general:
      uri: https://redmine.mydomain.com/
    user:
      api_key: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
      activity_id: 9
    tracked_queries:
    - 10001
    - 10002
    - 10003
    tracked_reports:
    - my_report_string_id
    activities:
      9: Developpement

Configuration directory and file are not created upon installation. You may create them manually or launch minetime for the first time and the configuration wizard will kick in.

You can find your API key on your redmine account page ( /my/account ) when logged in, on the right-hand pane of the default layout. Rest API has to be activated on the redmine instance. See `Redmine Rest API Documentation <https://www.redmine.org/projects/redmine/wiki/Rest_API#Authentication>`_ for more in depth details.


Using minetime
--------------

::


  minetime --help

  Usage: minetime [OPTIONS] [INPUT]

  Options:
    -a, --all                       Import all timelogs in --batch, regardless
                                    of --date.
    -d, --date TEXT                 YYYY-MM-DD date of timelogs, default: today.
    -b, --batch [gtl|utt]           Read GTimelog|utt from input. See GTimelog
                                    integration documentation.
    -t, --timelog <INTEGER FLOAT TEXT INTEGER>...
                                    ISSUEID, HOURS, COMMENTS, ACTIVITYID
                                    HOURS: decimal float (0.25 : 15 minutes).
    -i, --issues                    Show issues and exit. See GTimelog
                                    integration documentation.
    -r, --report TEXT               Time Report of given Project.
    --debug                         Enable debug logging.
    --version                       Show the version and exit.
    --help                          Show this message and exit.


Interactive CLI Wizard::

   minetime


Example feeding 2 timelogs from command line::

   minetime -t 123 0.75 "first time log", 9 -t 321 1.5 "second time log", 9


Example importing gtimelog flat file::

   minetime -b gtl $HOME/.local/share/gtimelog/timelog.txt

Note that this will import *today's* timelogs. Use ``--date`` to specify another day to import or ``--all`` to import everything found in input file.


Project Report::

   minetime -r git-helloworld
