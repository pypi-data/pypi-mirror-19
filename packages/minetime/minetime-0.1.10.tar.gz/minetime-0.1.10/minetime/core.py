# -*- coding: utf-8 -*-
import os
import sys
from collections import defaultdict, namedtuple
from datetime import datetime, timedelta
from itertools import groupby

import click
import yaml
from redmine.exceptions import ResourceNotFoundError, ValidationError
from tabulate import tabulate

from .helpers import (convert_date_string, convert_time_string,
                      get_activity_name, get_config, get_logger)
from .proxy import RedmineProxy

Timelog = namedtuple('Timelog', ['issue_id', 'hours', 'spent_on', 'activity_id', 'comments'])


def vali_date_option(ctx, param, value):
    return vali_date(value)


@click.command()
@click.option('--all', '-a', is_flag=True, default=False,
              help='import all timelogs in --batch, regardless of --date')
@click.option('--date', '-d', callback=vali_date_option,
              default=datetime.today().strftime('%Y-%m-%d'),
              help='YYYY-MM-DD date of timelogs, defaults to today')
@click.option('--batch', '-b', type=click.Choice(['gtl', 'utt']),
              help='read gtimelog|utt from input.')
@click.option('--timelog', '-t', multiple=True, type=(int, float, str, int),
              help="""
ISSUEID, HOURS, COMMENTS, ACTIVITYID
              HOURS: decimal float (0.25 : 15 minutes)
              """)
@click.option('--silent', '-s', is_flag=True, default=False,
              help='script friendly/no output.\ntimelogs must be fed.')
@click.option('--report', '-r', type=str, help='Time Report of given Project')
@click.option('--debug', is_flag=True, default=False,
              help='Enable debug logging.')
@click.version_option()
@click.argument('input', type=click.File('r', encoding='UTF-8'), required=False)
def mine_time(all, date, batch, timelog, silent, report, debug, input):
    logger = get_logger(debug)
    timelogs = []

    config = init_config()
    logger.debug('config: %s', config)
    proxy = init_proxy(logger, config)
    tracked_query_ids = config['tracked_queries']
    activity_id = config['user']['activity_id']
    try:
        activities = config['activities']
    except:
        activities = False

    if report:
        return project_report(proxy, report)
    if batch:
        timelogs = get_batch_timelogs(logger, batch, input, activity_id, date, all)
    elif timelog:
        logger.debug('importing cli-fed timelog (-t)')
        for (issue_id, hours, comments, activity_id) in timelog:
            t = Timelog(issue_id=issue_id, hours=hours, spent_on=date,
                        activity_id=activity_id, comments=comments)
            timelogs.append(t)
    else:
        logger.debug('entering cli wizard')
        focused_issues = proxy.get_issues(tracked_query_ids)
        timelogs = cli_wizard(logger, focused_issues, activity_id, date)

    click.clear()
    echo_timelogs(timelogs, activities)
    try:
        response = click.confirm('\nPost all printed entries?')
    except click.Abort:
        logger.debug('confirm before post raised a click.Abort exception')
        response = False

    if not response:
        logger.debug('did not even post a jiffy')
        return False
    try:
        proxy.post_timelogs(timelogs)
        click.echo('\n✓ Done. Goodbye.')
    except ValidationError as e:
        click.echo('Some timelogs could not be posted. Do all issues exist on redmine? Redmine returned: {}'.format(e))


def project_report(proxy, pid):
    click.clear()
    click.echo('Please wait while data is fetched from server. This should take more or less 30 seconds depending on dataset size and network connection.')
    try:
        p = proxy.get_project(pid)
    except ResourceNotFoundError:
        click.echo('Not a project. Goodbye for now.')
        return

    data = []
    username = lambda item: item['user']['name'] if hasattr(item, 'user') and hasattr(item['user'], 'name') else '-'
    if not p.versions:
        click.echo('No version found. Goodbye for now.')
        return
    for iv in p.versions:
        if not(hasattr(iv, 'created_on') and hasattr(iv, 'due_date')):
            continue
        period_time_entries = [t for t in p.time_entries
                               if day_between(datetime.date(iv.created_on),
                                              iv.due_date, t.spent_on)
                               and hasattr(t, 'spent_on')]
        total_period = total_hours(period_time_entries)

        period_time_entries.sort(key=username)
        user_grouped_entries = groupby(period_time_entries, username)
        si = [s for s in p.issues
              if (s.tracker.id == 5 and hasattr(s, 'fixed_version') and (s.fixed_version.id == iv.id))]
        if iv.status == 'open':
            issues_no_estimate = [(i.id, i.subject)
                                    for i in p.issues
                                    if (hasattr(i, 'estimated_hours')
                                    and i.estimated_hours == 0
                                    and hasattr(i, 'fixed_version')
                                    and (i.fixed_version.id == iv.id))]

            new_issues_worked = [(i.id, i.subject)
                                    for i in p.issues
                                    if (i.status == 1
                                    and i.time_entries
                                    and hasattr(i, 'fixed_version')
                                    and (i.fixed_version.id == iv.id))]
        else:
            issues_no_estimate = []
            new_issues_worked = []

        data.append((iv,
                     total_period,
                     period_time_entries,
                     user_grouped_entries,
                     si,
                     issues_no_estimate,
                     new_issues_worked))
    print_project_report(p, data)


def print_project_report(p, data):
    project_total_hours = sum([t[1] for t in data])
    sep = '-' * 80
    p1 = u'Project {}'.format(p.name)
    p2 = 'Total Worked Hours: {}'.format(project_total_hours)
    pline = space_line(p1, p2) + '\n'


    click.clear()
    click.echo(sep)
    click.echo(pline)
    click.echo(sep)
    sort_on_due_date = lambda item: item[0]['due_date'] if len(item) and hasattr(item[0], 'due_date') else datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    data.sort(key=sort_on_due_date)
    for vperiod, period_total, period_entries, periodi, \
        scenarios, unestimated_issues, new_issues_worked in data:

        v1 = u'V: {} ({})'.format(vperiod.name, vperiod.status)
        if hasattr(vperiod, 'due_date'):
            vdue = vperiod.due_date
        else:
            vdue = datetime.strptime('1900-01-01', '%Y-%m-%d')
        v2 = 'Period From {} To {}'.format(vperiod.created_on.date(), vdue)
        vline = space_line(v1, v2) + '\n'

        click.echo(vline)
        for key, group in periodi:
            onesum = sum([item["hours"] for item in group])
            click.echo(u'{} : {}'.format(key, onesum))
        click.echo(space_line('', 'Period Total Worked Hours: {}'.format(period_total)))
        click.echo()
        vhours = 0
        scolor = {
            1: 'blue',  # New
            2: 'yellow',  # Open
            8: 'green',  # Done
            4: 'red',  # Feedback
            9: 'magenta',  # Review
        }

        for s in scenarios:
            shours = total_hours(s.time_entries)
            vhours += shours
            echostr = (u'{} ({}) : {}/{}'.format(s.subject, s.status.name, s.story_points, shours))
            click.secho(echostr, fg='white', bg=scolor[s.status.id], bold=True)
        click.echo()
        if vhours:
            click.echo(space_line('', 'Version Total Worked Hours: {}'.format(vhours)))
        click.echo(sep)
        if unestimated_issues:
            echo_boom('Issues with no estimated_hours:')
            echo_boom(tabulate(unestimated_issues))
        if new_issues_worked:
            echo_boom('New Issues with time entries:')
            echo_boom(tabulate(new_issues_worked))
    click.echo(sep)
    click.echo(pline)
    click.echo(sep)


def echo_boom(boom):
    click.secho(boom, bg='red', fg='white', bold=True)


def space_line(a, b, total=80):
    space = (total - len(a) - len(b)) * ' ' or '\n' + ' ' * (total - len(b))
    return a + space + b


def total_hours(time_entries):
    return sum([t.hours for t in time_entries])


def day_between(start, end, day):
    return start <= day <= end


def vali_date(value):
    try:
        return convert_date_string(value)
    except ValueError:
        return False


def init_config():
    config_dir = click.get_app_dir('minetime')
    config_file = os.path.join(config_dir, 'config.yml')

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(config_file):
        wizard_create_config(config_file)

    config = get_config()
    if not config:
        click.echo('wrong config!')
        sys.exit(0)

    return config


def init_proxy(logger, config):
    uri = config['general']['uri']
    key = config['user']['api_key']
    proxy = RedmineProxy(logger, uri, key)
    return proxy


def merge_sieblings(timelogs, logger):
    merged_timelogs = []

    # Pop timelogs and group them by (issue, date) pair
    D = defaultdict(list)

    for x in range(len(timelogs) - 1, -1, -1):
        timelog = timelogs.pop()
        D[(timelog.issue_id, timelog.spent_on)].append(timelog)

    # Merge back
    for k, v in list(D.items()):
        if len(v) == 1:
            rhours = round_hours(v[0].hours)
            t = Timelog(v[0][0], rhours, v[0][2], v[0][3], v[0][4])
            merged_timelogs.append(t)
        elif len(v) > 1:
            mhours = 0
            mcomments = ''
            for timelog in v:
                c = timelog.comments.strip()
                mhours += timelog.hours
                if mcomments.find(c) == -1:
                    mcomments += (c + '|')
                mactivity = timelog.activity_id
            mcomments = mcomments.rstrip('|')
            mhours = round_hours(mhours)
            merged_timelogs.append(Timelog(k[0], mhours, k[1], mactivity, mcomments))

    return merged_timelogs


def round_hours(hours):
    return round(hours * 4) / 4


def get_batch_timelogs(logger, batch, input, activity_id, date, all):
    '''
    gtimelog format:
        2016-12-04 05:00: arrived
        2016-12-04 05:45: 12345 bake breakfast
        2016-12-04 06:30: 12346 shower
        2016-12-04 07:15: 12347 walk the spiders
        2016-12-04 08:00: 12348 fix the hamsters
        2016-12-04 09:00: 12349 stick the stickers
        2016-12-04 09:15: 12346 shower
        2016-12-04 12:00: 12347 clean the dumpsters
        2016-12-04 12:45: 12346 shower**
        2016-12-04 13:15: lunch ***
        2016-12-04 13:45: 12346 shower
    '''

    logger.debug('importing input-file-fed timelogs, {} format'.format(batch))

    timelogs = []
    t0 = [0, 0]
    for line in input:
        line_strip = line.strip()
        if not line_strip:
            continue
        logger.debug(u'playing on line: {}'.format(line_strip))
        try:
            raw_date, raw_time, raw_issue = line_strip.split(' ', 2)
        except(ValueError):
            raise ValueError('Stumbled on line {}'.format(line_strip))

        raw_time = raw_time.rstrip(':')
        record_date = vali_date(raw_date)
        record_time = convert_time_string(raw_time)
        record_issue = raw_issue
        logger.debug('working on batch line record_date: {} record_time: {}'.format(record_date, record_time))

        # off focus
        if not all and (record_date != date):
            logger.debug('record_date: {} | date: {}'.format(record_date, date))
            continue
        # reset day
        elif record_issue.startswith('arrived') or record_issue.startswith('hello'):
            logger.debug('new day: {}'.format(record_date))
            t0 = [record_date, record_time]
            continue
        else:
            assert(t0[0] == record_date)
            current_time = datetime.combine(datetime(1, 1, 1, 0, 0, 0), record_time)
            previous_time = datetime.combine(datetime(1, 1, 1, 0, 0, 0), t0[1])
            time_diff = current_time - previous_time
            t0[1] = record_time  # reset timer

            # off-records
            if batch == 'gtl' and record_issue.startswith('**'):
                continue  # only gtimelog accepts starting ** as escape sequence
            if record_issue.endswith('**'):
                continue

            logger.debug('New timelog! {} record_date: {} record_time: {}'
                         .format(t0, record_date, record_time))
            # add timelog
            hours = time_diff.total_seconds() / timedelta(hours=1).total_seconds()
            issue_id = 0
            raw_description = ''
            try:
                if record_issue.find(':'):
                    raw_issue_id, raw_description = record_issue.split(':', 1)
                    raw_issue_id = raw_issue_id.strip()
                    if(raw_issue_id.isdigit()):
                        issue_id = int(raw_issue_id)
                if(not issue_id):
                    raw_issue_id, raw_description = record_issue.split(' ', 1)
                    issue_id = int(raw_issue_id.strip())

                description = raw_description.strip()
                t = Timelog(issue_id=issue_id, hours=hours,
                            spent_on=record_date,
                            activity_id=activity_id,
                            comments=description)
                timelogs.append(t)


            except ValueError:
                # add to drop list
                logger.debug('stdin dropped timelog: %s', record_issue)
                pass

    timelogs = merge_sieblings(timelogs, logger)
    logger.debug('Batched-parsed-timelogs: %s', timelogs)
    return timelogs


def cli_choose_issue(focused_issues):
    assigned_issues, tracked_issues_list = focused_issues
    if(len(tracked_issues_list)):
        tracked_issues = tracked_issues_list[0]  # TODO: handle tracked_issues_list
    else:
        tracked_issues = []
    len_assigned_issues = len(assigned_issues)
    len_tracked_issues = len(tracked_issues)
    assigned_index = list(range(1, len_assigned_issues + 1))
    tracked_index = list(range(len_assigned_issues + 1,
                          len_assigned_issues + len_tracked_issues + 1))
    click.echo("Assigned Issues\n")
    click.echo(tabulate(assigned_issues, headers="keys", showindex=assigned_index))
    if len_tracked_issues:
        click.echo("\nTracked Issues\n")
        click.echo(tabulate(tracked_issues, headers="keys", showindex=tracked_index))
    click.echo("\n")

    selected = 0
    while not selected:
        raw_selected = click.prompt("Select Issue", type=int)
        try:
            selected = int(raw_selected)
            s = selected - 1

            if selected in assigned_index:
                issue_id = assigned_issues[s]['id']
                issue_subject = assigned_issues[s]['subject']
            elif selected in tracked_index:
                s = s - len_assigned_issues
                issue_id = tracked_issues[s]['id']
                issue_subject = tracked_issues[s]['subject']
            else:
                raise ValueError
        except ValueError:
            click.echo('selected invalid value. Please select one of the listed issues')
            selected = 0

    return (issue_id, issue_subject)


def cli_wizard(logger, focused_issues, activity_id, date):
    """ wizard, creates Timelogs interactively"""

    timelogs = []
    while True:
        click.clear()
        issue_id, issue_subject = cli_choose_issue(focused_issues)

        # TODO validate activity_id

        hours = click.prompt("Enter decimal hours worked (0.25 per 15 minutes)", type=float)
        import_date = click.prompt("Input new date for timelog or keep current default",
                                   default=date, value_proc=vali_date)

        comments = get_comments_message(issue_id, issue_subject, hours, import_date)

        # All is good. Add timelog.
        date = import_date
        t = Timelog(issue_id=issue_id, hours=hours, spent_on=date,
                    activity_id=activity_id, comments=comments)
        timelogs.append(t)

        if not click.confirm('New time entry?'):
            if click.confirm('Merge sieblings?'):
                timelogs = merge_sieblings(timelogs, logger)
            return timelogs


def get_comments_message(issue_id, issue_subject, hours, date):
    MARKER = '# Everything below is ignored\n'
    INSTRUCTION = '# Describe your time entry (to complete issue name)\n'
    CONTEXT = u'# Task ({}) : {}\n'.format(issue_id, issue_subject)
    HOURS = '# Hours worked: {}\n'.format(hours)
    DATE = '# Date worked on: {}\n'.format(date)
    message = ''
    while not message:
        if click.confirm('Enter Comments?'):
            message = click.edit('\n\n' + MARKER + INSTRUCTION + CONTEXT + HOURS + DATE)
        else:
            return ''
    return message.split(MARKER, 1)[0].rstrip('\n')


def echo_timelogs(timelogs, activities):
    human_timelogs = [[t[0],
                       t[1],
                       humanize_date(t[2]),
                       get_activity_name(t[3], activities),
                       t[4]]
                      for t in timelogs]

    click.echo(tabulate(human_timelogs, headers=('id', 'hr', 'date', 'activity', 'com')))


def humanize_date(d):
    today = datetime.now().date()
    delta = d - today
    if delta.days == 0:
        return 'today'
    elif delta.days == 1:
        return 'tomorrow'
    elif delta.days == -1:
        return 'yesterday'
    else:
        return d.strftime('%Y-%m-%d')


def wizard_create_config(config_file):
    wizard_confirm_file = '''
    It seems like you have no configuration file.
    Wizard can create one for you.
    What you will need:
      - The redmine instance URL
      - Your API Key
    Go?'''

    if not click.confirm(wizard_confirm_file):
        return

    api_key = click.prompt("What is your Redmine API Key?", type=str)
    redmine_url = click.prompt("What is your Redmine URL?", type=str)

    config = get_new_config(api_key, redmine_url)

    write_new_config(config, config_file)


def get_new_config(api_key, redmine_url):
    config = {}
    config['user'] = {}
    config['general'] = {}
    config['tracked_queries'] = {}
    config['user']['api_key'] = api_key
    config['general']['uri'] = redmine_url
    config['user']['activity_id'] = 9
    return config


def write_new_config(config, config_file):
    with click.open_file(config_file, 'w') as f:
        return yaml.safe_dump(config, f, default_flow_style=False)
