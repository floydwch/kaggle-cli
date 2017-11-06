import os
import time
import re
import json

from cliff.command import Command

from . import common
from .config import get_final_config


class Submit(Command):
    'Submit an entry to a specific competition.'

    def get_parser(self, prog_name):
        parser = super(Submit, self).get_parser(prog_name)

        parser.add_argument('entry', help='entry file')

        parser.add_argument('-m', '--message', help='message')
        parser.add_argument('-c', '--competition', help='competition')
        parser.add_argument('-u', '--username', help='username')
        parser.add_argument('-p', '--password', help='password')

        return parser

    def take_action(self, parsed_args):
        config = get_final_config(parsed_args)

        username = config.get('username', '')
        password = config.get('password', '')
        competition = config.get('competition', '')

        browser = common.login(username, password)
        base = 'https://www.kaggle.com'
        competition_url = '/'.join([base, 'c', competition])
        file_form_url = '/'.join([base, 'blobs/inbox/submissions'])
        entry_form_url = '/'.join([competition_url, 'submission.json'])

        entry = parsed_args.entry
        message = parsed_args.message

        competition_page = browser.get(competition_url)

        if competition_page.status_code == 404:
            print('competition not found')
            return

        team_id = re.search(
            '"team":{"id":(?P<id>\d+)',
            str(competition_page.soup)
        ).group(1)

        form_submission = browser.post(
            file_form_url,
            data={
                'fileName': entry,
                'contentLength': os.path.getsize(entry),
                'lastModifiedDateUtc': int(os.path.getmtime(entry) * 1000)
            }
        ).json()

        file_submit_url = base + form_submission['createUrl']

        with open(entry, 'rb') as submission_file:
            token = browser.post(
                file_submit_url,
                files={
                    'file': submission_file
                }
            ).json()['token']

        entry_form_resp_message = browser.post(
            entry_form_url,
            data=json.dumps({
                'blobFileTokens': [token],
                'submissionDescription': message if message else ''
            }),
            headers={
                'Content-Type': 'application/json'
            }
        ).json()

        if entry_form_resp_message['pageMessages'] and \
            entry_form_resp_message['pageMessages']['type'] == 'error':
            print(entry_form_resp_message['dangerousHtmlMessage'])
            return

        status_url = (
            'https://www.kaggle.com/'
            'c/{}/submissions/status.json'
            '?apiVersion=1&teamId={}'.format(competition, team_id)
        )

        while True:
            time.sleep(1)
            status = browser.get(status_url).json()
            if status['submissionStatus'] == 'pending':
                continue
            elif status['submissionStatus'] == 'complete':
                print(status['publicScoreFormatted'])
                break
            else:
                print('something went wrong')
                break
