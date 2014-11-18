from cliff.command import Command
from mechanize import Browser
from lxml import html
from time import sleep


class Entry(Command):
    'Submit an entry to a specific competition.'

    def get_parser(self, prog_name):
        parser = super(Entry, self).get_parser(prog_name)

        parser.add_argument('competition', help='competition name')
        parser.add_argument('entry', help='entry file')

        parser.add_argument('-m', '--message', help='message')
        parser.add_argument('-u', '--username', help='username',
                            required=True)
        parser.add_argument('-p', '--password', help='password',
                            required=True)

        return parser

    def take_action(self, parsed_args):

        base = 'https://www.kaggle.com'

        login_url = base
        username = parsed_args.username
        password = parsed_args.password

        competition = parsed_args.competition
        submit_url = '/'.join([base, 'c', competition, 'submissions', 'attach'])

        entry = parsed_args.entry
        message = parsed_args.message

        browser = Browser()

        browser.open(login_url)
        browser.select_form(nr=0)

        browser['UserName'] = username
        browser['Password'] = password

        browser.submit()

        browser.open(submit_url)
        browser.select_form(nr=0)

        browser.form.add_file(open(entry), filename=entry)

        if message:
            browser['SubmissionDescription'] = message

        browser.submit()

        while True:
            leaderboard = html.fromstring(browser.response().read())
            score = leaderboard.cssselect(
                '.submission-results strong')

            if len(score) and score[0].text_content():
                score = score[0].text_content()
                break

            sleep(30)
            browser.reload()

        self.app.stdout.write(score + '\n')
