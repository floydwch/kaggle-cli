from cliff.command import Command
from mechanize import Browser
from lxml import html
import ConfigParser
import os


class Download(Command):
    'Download data files from a specific competition.'

    def get_parser(self, prog_name):
        parser = super(Download, self).get_parser(prog_name)

        parser.add_argument('-c', '--competition', help='competition')
        parser.add_argument('-u', '--username', help='username')
        parser.add_argument('-p', '--password', help='password')

        return parser

    def take_action(self, parsed_args):
        config_dir = '~/.kaggle-cli'
        config_dir = os.path.expanduser(config_dir)

        if os.path.isdir(config_dir):
            config = ConfigParser.ConfigParser(allow_no_value=True)
            config.readfp(open(config_dir + '/config'))

            if parsed_args.username:
                username = parsed_args.username
            else:
                username = config.get('user', 'username')

            if parsed_args.password:
                password = parsed_args.password
            else:
                password = config.get('user', 'password')

            if parsed_args.competition:
                competition = parsed_args.competition
            else:
                competition = config.get('user', 'competition')

        base = 'https://www.kaggle.com'
        login_url = 'https://www.kaggle.com/account/login'
        data_url = '/'.join([base, 'c', competition, 'data'])

        browser = Browser()

        browser.open(login_url)
        browser.select_form(nr=0)

        browser['UserName'] = username
        browser['Password'] = password

        browser.submit()

        browser.open(data_url)
        data_page = html.fromstring(browser.response().read())

        src_urls = map(
            lambda x: base + x.attrib['href'],
            data_page.cssselect('#data-files a'))

        for url in src_urls:
            self.app.stdout.write('downloading %s\n' % url)
            browser.retrieve(url, url.split('/')[-1])
