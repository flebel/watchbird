Watchbird
=========

Watchdog for Twitter. Sends an email when a Twitter handle has not tweeted in N seconds, minutes, hours, days, weeks, months (30 days) or years (365 days).

Emails will be sent whether or not a notification was sent during the previous check.

Getting started
---------------

* `pip install -r requirements.txt`.
* Copy the configuration file `default.conf.sample` to `default.conf`.
* Define screen names to watch and Twitter app tokens in the configuration file.
* Run script frequently, through a cronjob or some other mean if a granularity of seconds is required.

