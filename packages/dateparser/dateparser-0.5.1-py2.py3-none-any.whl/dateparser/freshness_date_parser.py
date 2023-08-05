# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import regex as re
from datetime import datetime
from datetime import time

from dateutil.relativedelta import relativedelta

from dateparser.utils import apply_timezone, localize_timezone
from .parser import time_parser


_UNITS = r'year|month|week|day|hour|minute|second'
PATTERN = re.compile(r'(\d+)\s*(%s)\b' % _UNITS, re.I | re.S | re.U)


class FreshnessDateDataParser(object):
    """ Parses date string like "1 year, 2 months ago" and "3 hours, 50 minutes ago" """
    def __init__(self):
        self.now = None

    def _are_all_words_units(self, date_string):
        skip = [_UNITS,
                r'ago|in|\d+',
                r':|[ap]m']

        date_string = re.sub(r'\s+', ' ', date_string.strip())

        words = filter(lambda x: x if x else False, re.split(r'\W', date_string))
        words = filter(lambda x: not re.match(r'%s' % '|'.join(skip), x), words)
        return not list(words)

    def _parse_time(self, date_string, settings):
        """Attemps to parse time part of date strings like '1 day ago, 2 PM' """
        date_string = PATTERN.sub('', date_string)
        date_string = re.sub(r'\b(?:ago|in)\b', '', date_string)
        try:
            return time_parser(date_string)
        except:
            pass

    def parse(self, date_string, settings):

        _time = self._parse_time(date_string, settings)

        def apply_time(dateobj, timeobj):
            if not isinstance(_time, time):
                return dateobj

            return dateobj.replace(
                hour=timeobj.hour, minute=timeobj.minute,
                second=timeobj.second, microsecond=timeobj.microsecond
            )

        if settings.RELATIVE_BASE:
            if 'local' not in settings.TIMEZONE.lower():
                self.now = localize_timezone(
                    settings.RELATIVE_BASE, settings.TIMEZONE)
            else:
                self.now = settings.RELATIVE_BASE

        elif 'local' in settings.TIMEZONE.lower():
            self.now = datetime.now()

        else:
            utc_dt = datetime.utcnow()
            self.now = apply_timezone(utc_dt, settings.TIMEZONE)

        date, period = self._parse_date(date_string)

        if date:
            date = apply_time(date, _time)
            if settings.TO_TIMEZONE:
                date = apply_timezone(date, settings.TO_TIMEZONE)

            if not settings.RETURN_AS_TIMEZONE_AWARE:
                date = date.replace(tzinfo=None)

        self.now = None
        return date, period

    def _parse_date(self, date_string):
        if not self._are_all_words_units(date_string):
            return None, None

        kwargs = self.get_kwargs(date_string)
        if not kwargs:
            return None, None

        period = 'day'
        if 'days' not in kwargs:
            for k in ['weeks', 'months', 'years']:
                if k in kwargs:
                    period = k[:-1]
                    break

        td = relativedelta(**kwargs)
        if re.search(r'\bin\b', date_string):
            date = self.now + td
        else:
            date = self.now - td
        return date, period

    def get_kwargs(self, date_string):
        m = PATTERN.findall(date_string)
        if not m:
            return {}

        kwargs = {}
        for num, unit in m:
            kwargs[unit + 's'] = int(num)

        return kwargs

    def get_date_data(self, date_string, settings=None):
        date, period = self.parse(date_string, settings)
        return dict(date_obj=date, period=period)

freshness_date_parser = FreshnessDateDataParser()
