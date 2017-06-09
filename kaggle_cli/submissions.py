'''
List of recent submissions.
Author: Konstantin Tretyakov (@konstantint)
'''
from __future__ import print_function
import json
from itertools import starmap

from cliff.command import Command

from . import common
from .config import get_final_config


class Submissions(Command):
    'List recent submissions.'

    def get_parser(self, prog_name):
        parser = super(Submissions, self).get_parser(prog_name)
        parser.add_argument('-c', '--competition', help='competition')
        parser.add_argument('-u', '--username', help='username')
        parser.add_argument('-p', '--password', help='password')
        parser.add_argument(
            '-s', '--sort',
            default='date',
            help='Field to sort by (date|publicScore|name). Default: date.'
        )
        parser.add_argument(
            '--page',
            type=int,
            default=1,
            help='Page of results (default: 1)'
        )
        parser.add_argument(
            '-g', '--group',
            default='successful',
            help=(
                'Submission group (all|successful|selected).'
                'Default: successful.'
            )
        )
        parser.add_argument(
            '-f', '--format',
            type=lambda s: s.replace('\\t', '\t').replace('\\n', '\n'),
            default='{date}\\t{name}\\t{details}\\t{publicScore}',
            help=(
                'Format string for printing results.'
                'Special value "json" denotes raw json output.'
                'Default: {date}\\t{name}\\t{details}\\t{publicScore}'
            )
        )
        return parser

    def fetch_submissions(self, config):
        browser = common.login(config['username'], config['password'])
        base = 'https://www.kaggle.com'
        url = '/'.join([base, 'c', config['competition'], 'submissions.json'])
        return browser.get(
            url,
            params=dict(
                sortBy=config['sort'],
                group=config['group'],
                page=config['page']
            )
        ).json()

    def take_action(self, parsed_args):
        config = get_final_config(parsed_args)
        submissions = self.fetch_submissions(config)

        if config['format'] == 'json':
            print(json.dumps(submissions, indent=2))
        else:
            for submission in submissions:
                try:
                    print(config['format'].format(
                        **dict(starmap(
                            lambda key, value: (
                                key,
                                '' if not value else value
                            ),
                            submission.items()
                        ))
                    ))
                except KeyError as e:
                    print(
                        'Invalid format string.'
                        'Field not found: {}'.format(e)
                    )
