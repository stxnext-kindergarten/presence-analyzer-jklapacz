# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from flask import redirect, abort

from presence_analyzer.main import app
from presence_analyzer import utils

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect('/static/presence_weekday.html')


@app.route('/api/v1/users', methods=['GET'])
@utils.jsonify
def users_view():
    """
    Users listing for dropdown.
    """
    data = utils.get_data()
    return [
        {'user_id': i, 'name': 'User {0}'.format(str(i))}
        for i in data.keys()
    ]


@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@utils.jsonify
def mean_time_weekday_view(user_id):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], utils.mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    return result


@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@utils.jsonify
def presence_weekday_view(user_id):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return result


@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@utils.jsonify
def presence_start_end_view(user_id):
    """
    Returns mean start & end time of given user grouped by weekday
    (mean time when user begins work, mean time when user finish work)
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        abort(404)

    weekdays = utils.group_start_end_by_weekday(data[user_id])
    return [
        (calendar.day_abbr[weekday], utils.mean(items['start']), utils.mean(items['end']))
        for weekday, items in enumerate(weekdays)
    ]
