from cliff.command import Command
import shutil
from . import common

class Download(Command):
    'Download data files from a specific competition.'

    def get_parser(self, prog_name):
        parser = super(Download, self).get_parser(prog_name)

        parser.add_argument('-c', '--competition', help='competition')
        parser.add_argument('-u', '--username', help='username')
        parser.add_argument('-p', '--password', help='password')

        return parser

    def take_action(self, parsed_args):
        (username, password, competition) = common.get_config(parsed_args)
        browser = common.login(username, password)

        base = 'https://www.kaggle.com'
        data_url = '/'.join([base, 'c', competition, 'data'])

        data_page = browser.get(data_url)
        links = data_page.soup.find(id='data-files').find_all('a')

        for link in links:
            url = base + link.get('href')
            self.download_file(browser, url)

    def download_file(self, browser, url):
        self.app.stdout.write('downloading %s\n' % url)
        local_filename = url.split('/')[-1]
        stream = browser.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in stream.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

