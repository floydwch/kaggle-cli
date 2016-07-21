from cliff.command import Command
from mechanize import Browser
from lxml import html
from time import sleep
import os
import ConfigParser


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
        prefix = ''
        while True:
            config_dir = './.kaggle-cli'
            if os.path.isdir(prefix + '.kaggle-cli'):
                config_dir = os.path.expanduser(config_dir)
                break
            else:
                if os.path.expanduser(config_dir) !=\
                        os.path.expanduser('~'):
                    prefix = prefix + '../'
                else:
                    config_dir = os.path.expanduser(config_dir)
                    os.mkdir(config_dir, 0o700)
                    break

        global_config_dir = '~/.kaggle-cli'
        global_config_dir = os.path.expanduser(global_config_dir)

        if os.path.isdir(global_config_dir):
            global_config = ConfigParser.ConfigParser(allow_no_value=True)
            global_config.readfp(open(global_config_dir + '/config'))

            if parsed_args.username:
                username = parsed_args.username
            else:
                username = global_config.get('user', 'username')

            if parsed_args.password:
                password = parsed_args.password
            else:
                password = global_config.get('user', 'password')

            if parsed_args.competition:
                competition = parsed_args.competition
            else:
                competition = global_config.get('user', 'competition')

        if os.path.isdir(config_dir):
            config = ConfigParser.ConfigParser(allow_no_value=True)
            config.readfp(open(config_dir + '/config'))

            if parsed_args.username:
                username = parsed_args.username
            else:
                if config.has_option('user', 'username'):
                    username = config.get('user', 'username')

            if parsed_args.password:
                password = parsed_args.password
            else:
                if config.has_option('user', 'password'):
                    password = config.get('user', 'password')

            if parsed_args.competition:
                competition = parsed_args.competition
            else:
                if config.has_option('user', 'competition'):
                    competition = config.get('user', 'competition')
        else:
            username = parsed_args.username
            password = parsed_args.password
            competition = parsed_args.competition

        base = 'https://www.kaggle.com'
        login_url = 'https://www.kaggle.com/account/login'
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

        # while True:
        #     leaderboard = html.fromstring(browser.response().read())
        #     score = leaderboard.cssselect('.submission-result strong')

        #     if len(score) and score[0].text_content():
        #         score = score[0].text_content()
        #         break

        #     sleep(30)
        #     browser.reload()

        # self.app.stdout.write(score + '\n')
