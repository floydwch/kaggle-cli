from configparser import ConfigParser
from mechanicalsoup import Browser
import os
import sys

def get_config(parsed_args):
    prefix = ''
    while True:
        config_dir = '.kaggle-cli'
        if os.path.isdir(prefix + config_dir) or \
            os.path.abspath(prefix) == os.path.expanduser('~') or \
                os.path.abspath(prefix) == os.path.abspath('/'):
            break
        prefix = prefix + '../'

    config_dir = os.path.abspath(prefix + config_dir)

    global_config_dir = '~/.kaggle-cli'
    global_config_dir = os.path.expanduser(global_config_dir)

    if os.path.isdir(global_config_dir):
        global_config = ConfigParser(allow_no_value=True)
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
        config = ConfigParser(allow_no_value=True)
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

    return (username, password, competition)

def login(username, password):
    login_url = 'https://www.kaggle.com/account/login'
    browser = Browser()

    login_page = browser.get(login_url)
    login_form = login_page.soup.select("#login-account")[0]
    login_form.select("#UserName")[0]['value'] = username
    login_form.select("#Password")[0]['value'] = password
    login_result = browser.submit(login_form, login_page.url)
    if login_result.url == login_url:
        error = (login_result.soup
                .select('#standalone-signin .validation-summary-errors')[0].get_text())
        print('There was an error logging in: ' + error)
        sys.exit(1)

    return browser
