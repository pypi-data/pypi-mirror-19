minetime
========

Minetime is a command line application helping you input timelogs and post them to configured redmine. minetime can collect timelogs in 4 main ways:

- With no special import option you enter interactive wizard mode, where all information will be prompted by the user. In wizard mode, user gets to select issues from assigned issues and tracked queries.
- With one or more --timelog option to import timelogs solely from the command line.
- With the --batch utt option to import timelogs from specified utt flat file.
- With the --batch gtl option to import timelogs from specified Gtimelog flat file.

Multiple timelogs on same issue and date can be auto-magically merged together into a single time entry.

Timelogs times are rounded to the nearest quarter-hour (after merge).

Collected timelogs are always presented for confirmation before transparently beeing pushed to configured redmine server via its REST API, using the python-redmine library.

`Learn more <https://gitlab.com/yakoi/minetime>`_.


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
    activities:
       - 9: Developpement

Configuration directory and file are not created upon installation. You may create them manually or launch minetime for the first time and the configuration wizard will kick in.

You can find your API key on your redmine account page ( /my/account ) when logged in, on the right-hand pane of the default layout. Rest API has to be activated on the redmine instance. See `Redmine Rest API Documentation <https://www.redmine.org/projects/redmine/wiki/Rest_API#Authentication>`_ for more in depth details.


Using minetime
--------------

::


  minetime --help

  Usage: minetime [OPTIONS] [INPUT]

  Options:
    -a, --all                       import all timelogs in --batch, regardless
                                    of --date
    -d, --date TEXT                 YYYY-MM-DD date of timelogs, defaults to
                                    today
    -b, --batch [gtl|utt]           read gtimelog|utt from input.
    -t, --timelog <INTEGER FLOAT TEXT INTEGER>...
                                    ISSUEID, HOURS, COMMENTS, ACTIVITYID
                                    HOURS: decimal float (0.25 : 15 minutes)
    -s, --silent                    script friendly/no output.
                                    timelogs must be
                                    fed.
    -r, --report TEXT               Time Report of given Project
    --debug                         Enable debug logging.
    --version                       Show the version and exit.
    --help                          Show this message and exit.


Interactive CLI Wizard::

   minetime


Example feeding 2 timelogs from command line::

   minetime -t 123 0.75 "first time log", 9 -t 321 1.5 "second time log", 9


Example importing gtimelog flat file::

   minetime -b gtl ~/.local/share/gtimelog/timelog.txt

Note that this will import *today's* timelogs. Use ``--date`` to specify another day to import or ``--all`` to import everything found in input file.


Project Report::

   minetime -r git-helloworld
