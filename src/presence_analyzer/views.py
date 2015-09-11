# -*- coding: utf-8 -*-
"""
Defines views.
"""

import calendar
from flask import redirect, render_template, url_for
from presence_analyzer.main import app
from presence_analyzer import utils

import logging
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@app.route('/')
def mainpage():
    """
    Redirects to front page.
    """
    return redirect(url_for('presence_weekday_template_view'))


@app.route('/presence_weekday')
def presence_weekday_template_view():
    """
    Presence by weekday page (front page)
    """
    title = 'Presence by weekday'
    return render_template('presence_weekday.html', title=title)


@app.route('/mean_time_weekday')
def mean_time_weekday_template_view():
    """
    Presence mean time by weekday page
    """
    title = 'Presence mean time by weekday'
    return render_template('mean_time_weekday.html', title=title)


@app.route('/presence_start_end')
def presence_start_end_template_view():
    """
    Presence start-end weekday
    """
    title = 'Presence start-end weekday'
    return render_template('presence_start_end.html', title=title)


@app.route('/api/v1/users', methods=['GET'])
@utils.jsonify
def users_json_view():
    """
    Users listing for dropdown.
    """
    return utils.get_users()


@app.route('/api/v1/mean_time_weekday/')
@app.route('/api/v1/mean_time_weekday/<int:user_id>', methods=['GET'])
@utils.jsonify
def mean_time_weekday_json_view(user_id=None):
    """
    Returns mean presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return {'success': False, 'data': []}

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], utils.mean(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    return {'success': True, 'data': result}


@app.route('/api/v1/presence_weekday/')
@app.route('/api/v1/presence_weekday/<int:user_id>', methods=['GET'])
@utils.jsonify
def presence_weekday_json_view(user_id=None):
    """
    Returns total presence time of given user grouped by weekday.
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return {'success': False, 'data': []}

    weekdays = utils.group_by_weekday(data[user_id])
    result = [
        (calendar.day_abbr[weekday], sum(intervals))
        for weekday, intervals in enumerate(weekdays)
    ]

    result.insert(0, ('Weekday', 'Presence (s)'))
    return {'success': True, 'data': result}


@app.route('/api/v1/presence_start_end/')
@app.route('/api/v1/presence_start_end/<int:user_id>', methods=['GET'])
@utils.jsonify
def presence_start_end_json_view(user_id=None):
    """
    Returns mean start & end time of given user grouped by weekday
    (mean time when user begins work, mean time when user finish work)
    """
    data = utils.get_data()
    if user_id not in data:
        log.debug('User %s not found!', user_id)
        return {'success': False, 'data': []}

    weekdays = utils.group_start_end_by_weekday(data[user_id])
    result = [
        (
            calendar.day_abbr[weekday],
            utils.mean(items['start']),
            utils.mean(items['end'])
        )
        for weekday, items in enumerate(weekdays)
    ]
    return {'success': True, 'data': result}
