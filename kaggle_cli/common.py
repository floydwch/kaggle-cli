import sys

from mechanicalsoup import Browser


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
