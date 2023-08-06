.. figure:: https://img.shields.io/pypi/dm/Slog.svg
   :alt: 

Slog is a simple logging framework named after the verb some people use
to describe the task of integrating logging into their projects.

I decided to throw this together a while back as a replacement for
Python's default logger, which is unweildy and completely overkill in
small projects, and not as noob-friendly as it could be. I then stopped
maintaining it because of an influx of other responsibilities.

A primary objective of slog is to ship with a default "theme" which is
easily readable at a glance; currently, this means including the date
and time of each log point, the level as a short text string, the file
name and line number of the invocation, and (when printing to STDOUT), a
colored splotch indicative of the log level.

Updates happen periodically, and I'm aiming to go back to regularly
maintaining slog over the next few weeks.

Syntax is simple enough; instantiate the Slog class and you're basically
ready to go.

::

    $ python
    >>> from slog.slog import Slog
    >>> log = Slog(loglvl=5, logfile="test.log")
    >>> for lvl in ['ok', 'info', 'warn', 'fail', 'crit']: getattr(log, lvl)('Testing me a slog')
    ...
    2016-08-18 05:29:09 || [  OK  ] ⬢ (<stdin>:1)   Testing me a slog
    2016-08-18 05:29:09 || [ INFO ] ⬢ (<stdin>:1)   Testing me a slog
    2016-08-18 05:29:09 || [ WARN ] ⬢ (<stdin>:1)   Testing me a slog
    2016-08-18 05:29:09 || [ FAIL ] ⬢ (<stdin>:1)   Testing me a slog
    2016-08-18 05:29:09 || [ CRIT ] ⬢ (<stdin>:1)   Testing me a slog
    >>> ^D

    $ cat test.log
    2016-08-18 05:29:09 || [  OK  ] (<stdin>:1)     Testing me a slog
    2016-08-18 05:29:09 || [ INFO ] (<stdin>:1)     Testing me a slog
    2016-08-18 05:29:09 || [ WARN ] (<stdin>:1)     Testing me a slog
    2016-08-18 05:29:09 || [ FAIL ] (<stdin>:1)     Testing me a slog
    2016-08-18 05:29:09 || [ CRIT ] (<stdin>:1)     Testing me a slog

That snippet is a comprehensive example of Slog's essential API.

The ``Slog`` class takes two optional parameters: the name of the
logfile (defaults to ``None``) and the logging level (``[0..5]``,
defaults to ``3``). If the latter gets a parameter outside of that
range, it'll default to 3.

The levels correspond to:

-  ``5`` => log everything everywhere
-  ``4`` => log only ``info`` and higher (skips ``ok``)
-  ``3`` => log only ``warn`` and higher (skips ``ok`` and ``info``)
-  ``2`` => log only ``fail`` and higher (skips ``ok``, ``info``, and
   ``warn``)
-  ``1`` => log only ``crit``
-  ``0`` => turn off logging completely on all channels

Writing a log entry is as simple as calling ``log.<level>()`` (with
``log`` an instance of ``Slog``) with ``<level>`` being one of ``ok``,
``info``, ``warn``, ``fail``, or ``crit``. Each of these functions takes
exactly one argument.

Because I want to retain the ability to create arbirary custom messages,
I've kept a modified ``write`` method - use it as
``log.write(message, level, color)``. This adds even more flexibility
taking int account that ``color`` can be ``any`` colour supported by the
``termcolor`` package.

Installing slog
^^^^^^^^^^^^^^^

For Python 3:

::

    $ pip3 install slog
    $ # or, depending on your aliases
    $ pip install slog

For Python 2 (only 2.7 tested):

::

    $ pip install slog

New stuff in this re-release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  File names and line numbers! Each slog call will include the file
   name and line number of the call.

Extending and modifying slog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It's a single-file, 75ish-line module, so I didn't build in a plugin
architecture, and I'm not planning on it. Slog's under an MIT license,
though, so go wild modifying it.

For example, you could swap out the ``ct()`` function, which returns the
current time, with a different time format. You could just rebind the
``slog.slog.ct`` function object to one you defined for a drop-in
replacement.

In an upcoming release (probably before September, 2016), I plan to add
better support for message formatting. Until then, I tried to go for
something good-looking, and which clearly conveys the severity, time,
and message.

I haven't done any testing to help adapt this default theme to
devleopers with colourblindness for lack of resources and expertise; I'd
be greatly appreciative of any input from this part of the community to
try and optimize it for at least the more common types of
colourblindness.

Please report any issues to the GitHub issue tracker at
github.com/verandaguy/slog/issues.

Acknowledgements (from way back, before the re-release)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Reddit user /u/pujuma for helping fix issue #1

-  Reddit user /u/grundee for providing feedback about the API
