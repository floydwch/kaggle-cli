'''
List of recent submissions.
Author: Konstantin Tretyakov (@konstantint)
'''
from __future__ import print_function
from cliff.command import Command
import json

from . import common
from .config import get_final_config


class Submissions(Command):
    'List recent submissions.'

    def get_parser(self, prog_name):
        parser = super(Submissions, self).get_parser(prog_name)
        parser.add_argument('-c', '--competition', help='competition')
        parser.add_argument('-u', '--username', help='username')
        parser.add_argument('-p', '--password', help='password')
        parser.add_argument('-s', '--sort', default='date', help='Field to sort by (date|publicScore|name). Default: date.')
        parser.add_argument('--page', type=int, default=1, help='Page of results (default: 1)')
        parser.add_argument('-g', '--group', default='successful', help='Submission group (all|successful|selected). Default: successful.')
        parser.add_argument('-f', '--format', type=lambda s: s.replace('\\t', '\t').replace('\\n','\n'),
                            default='{date}\\t{name}\\t{details}\\t{publicScore}', 
                            help='Format string for printing results. Special value "json" denotes raw json output. Default: {date}\\t{name}\\t{details}\\t{publicScore}')
        return parser

    @staticmethod
    def list(config=None, sort='date', group='successful', page=1, **other_args):
        if config is None: config = get_final_config()
        browser = common.login(config['username'], config['password'])
        base = 'https://www.kaggle.com'
        url = '/'.join([base, 'c', config['competition'], 'submissions.json'])
        return browser.get(url, params=dict(sortBy=sort, group=group, page=page)).json()
   
    @staticmethod
    def output(subs, format):
        if format == 'json':
            print(json.dumps(subs, indent=2))
        else:
            try:
                for ln in subs:
                    print(format.format(**ln))
            except KeyError, e:
                print("Invalid format string. Unknown key: {0}".format(e))
       
    def take_action(self, args):
        self.output(self.list(get_final_config(args), **vars(args)), args.format)

