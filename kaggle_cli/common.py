import sys
import os
import pickle

from mechanicalsoup import Browser

from .config import CONFIG_DIR_NAME


def login(username, password):
    config_dir_path = os.path.join(
        os.path.expanduser('~'),
        CONFIG_DIR_NAME
    )
    pickle_path = os.path.join(
        config_dir_path,
        'browser.pickle'
    )
    if os.path.isfile(pickle_path):
        try:
            with open(pickle_path, 'rb') as file:
                data = pickle.load(file)
                if data['username'] == username and \
                        data['password'] == password:
                    return data['browser']
        except:
            pass

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

    if not os.path.isdir(config_dir_path):
        os.mkdir(config_dir_path, 0o700)

    with open(pickle_path, 'wb') as f:
        pickle.dump(dict(
            username=username, password=password, browser=browser
        ), f)

    return browser
