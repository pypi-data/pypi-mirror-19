twiggy-goodies
==============

[![ChangeLog](http://allmychanges.com/p/python/twiggy-goodies/badge/?rnd=1)](http://allmychanges.com/p/python/twiggy-goodies/)

Here you'll find some useful addons to [Twiggy], pythonic logger.
These addons help to use Twiggy with third-party libraries, which
use standart library's [logging][].

Main target was to create convenient way to write log items
which are grouped by some request identifier. Twiggy already
supports it by it's `fields` method, but sometimes it is too
inconvenient to pass logger object around. That is why I take
idea of a threadlocal loggers stack from the [logbook][] and
implemented it for twiggy.

Here is example how to use it:

    from twiggy_goodies.setup import setup_logging
    from twiggy_goodies.threading import log

    def some_function():
        log.info('inner function does not accept logger')
        log.info('but uses same field as caller')


    setup_logging(None)

    log.info('before request')

    with log.fields(request_id='foo'):
        log.info('bar has happened')
        some_function()

    log.info('after request, id gone')

Output will be, as expected:

    2014-04-14T18:29:02Z:INFO:before request
    2014-04-14T18:29:02Z:INFO:request_id=foo:bar has happened
    2014-04-14T18:29:02Z:INFO:request_id=foo:inner function does not accept logger
    2014-04-14T18:29:02Z:INFO:request_id=foo:but uses same field as caller
    2014-04-14T18:29:02Z:INFO:after request, id gone

Same way, logger name could be changed, just replace `fields` context
manager to `name`.

There is no dark magick behind the scene: 

1) setup_logging does simple setup and redirects all output
   from standart `logging` to twiggy.
2) `log` object is proxies all logging methods to a topmost
   logger on the thread-local stack.
3) `fields` and `name` context managers just create a new
   logger as original twiggy's methods and put it on thread-local
   stack.

That is it.

Some other goodies
------------------

  * `twiggy_goodies.syslog` contains `SysLogOutput`.
  * `twiggy_goodies.json` contains `JsonOutput`, useful
    to pass data to logstash.
  * `twiggy_goodies.logstash` contains `LogstashOutput`,
    which sends messages directly to Logstash's UDP port.
  * `twiggy_goodies.django_rq` contains `job` decorator, which
    groups all messages logged from one task, using UUID.
  * `twiggy_goodies.django` contains `LogMixin` class which
    could be mixed to any management command, to group all
    logged messages by single UUID.
  * `twiggy_goodies.django` also contains `LogMiddleware`, to
    do the same as `LogMixin`, but for each http request.

[Twiggy]: https://github.com/wearpants/twiggy
[logging]: https://docs.python.org/2/library/logging.html
[logbook]: http://pythonhosted.org//Logbook/
