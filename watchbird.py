#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import argparse

from datetime import datetime, timedelta

import ses_mailer
import tweepy

seconds_per_unit = {'S': 1, 'M': 60, 'H': 3600, 'd': 3600*24, 'w': 604800, 'm': 3600*24*30, 'y': 3600*24*365}

parser = argparse.ArgumentParser(description='Watchdog for Twitter. Sends an email when a Twitter handle has not tweeted in N seconds, minutes, hours, days, weeks, months (30 days) or years (365 days).')
parser.add_argument('--config', default='default.conf', dest='config', help='Configuration file', type=str)


def construct_api(access_token, access_token_secret, consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def convert_to_seconds(val):
    return int(val[:-1]) * seconds_per_unit[val[-1]]

def load_config(filename):
    config = ConfigParser.SafeConfigParser()
    config.read(filename)
    return config

def watch(api, screen_name, warning):
    statuses = api.user_timeline(screen_name, count=1, include_rts=True)
    seconds_warning = convert_to_seconds(warning)
    if statuses and (statuses[0].created_at - timedelta(seconds=seconds_warning)) < (datetime.now() - timedelta(seconds=seconds_warning)):
        send_email_notification(screen_name, warning)

def send_email_notification(screen_name, warning):
    # TODO: Move these into the config file
    mail = ses_mailer.Mail(aws_access_key_id='TODO',
               aws_secret_access_key='TODO',
               region='us-east-1',
               sender='me@email.com')
    subject = '[watchbird] %s' % (screen_name,)
    message = '%s has not tweeted in %s' % (screen_name, warning,)
    mail.send(to='you@email.com',
              subject=subject,
              body=message)

if __name__ == '__main__':
    args = parser.parse_args()
    config = load_config(args.config)

    api = construct_api(access_token=config.get('twitter', 'access_token'),
                        access_token_secret=config.get('twitter', 'access_token_secret'),
                        consumer_key=config.get('twitter', 'consumer_key'),
                        consumer_secret=config.get('twitter', 'consumer_secret'))
    watches = config.get('watch', 'screen_names').split('\n')
    for w in watches:
        sn, warning = w.split(',')
        watch(api, sn, warning)

