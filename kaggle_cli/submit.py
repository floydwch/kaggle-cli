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

        username = config['username']
        password = config['password']
        competition = config['competition']

        browser = common.login(username, password)
        base = 'https://www.kaggle.com'
        submit_url = '/'.join([base, 'c', competition, 'submissions', 'attach'])

        entry = parsed_args.entry
        message = parsed_args.message

        submit_page = browser.get(submit_url)
        submit_form = submit_page.soup.find(id='submission-form')
        submit_form.find('input', {'name': 'SubmissionUpload'})['value'] = entry

        if message:
            submit_form.find('textarea', {'name': 'SubmissionDescription'}).insert(0, message)
        submit_result = browser.submit(submit_form, submit_page.url)
        leaderboard_url = '/'.join([base, 'c', competition, 'leaderboard'])
        assert submit_result.url == leaderboard_url

        # while True:
        #     leaderboard = html.fromstring(browser.response().read())
        #     score = leaderboard.cssselect('.submission-result strong')

        #     if len(score) and score[0].text_content():
        #         score = score[0].text_content()
        #         break

        #     sleep(30)
        #     browser.reload()

        # self.app.stdout.write(score + '\n')
