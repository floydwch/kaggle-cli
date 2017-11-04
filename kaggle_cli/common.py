import sys
import os
import pickle
import re

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

    browser = Browser()
    login_url = 'https://www.kaggle.com/account/login'

    login_page = browser.get(login_url)

    token = re.search(
        'antiForgeryToken: \'(?P<token>.+)\'',
        str(login_page.soup)
    ).group(1)

    login_result_page = browser.post(
        login_url,
        data={
            'username': username,
            'password': password,
            '__RequestVerificationToken': token
        }
    )

    error_match = re.search(
        '"errors":\["(?P<error>.+)"\]',
        str(login_result_page.soup)
    )

    if error_match:
        print(error_match.group(1))
        return

    if not os.path.isdir(config_dir_path):
        os.mkdir(config_dir_path, 0o700)

    with open(pickle_path, 'wb') as f:
        pickle.dump(dict(
            username=username, password=password, browser=browser
        ), f)

    return browser
