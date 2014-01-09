# -*- coding: utf-8 -*-

import re
from logbook import Logger

from splinter import Browser

logger = Logger('InstagramWebBot')

class InstagramWebBot(object):
    '''Instagram Web Bot for automatic things using web browser.'''

    LOGIN_URL = 'https://instagram.com/accounts/login/';
    REGISTER_CLIENT_URL = 'http://instagram.com/developer/clients/register/'
    LOGOUT_URL = 'http://instagram.com/accounts/logout/'

    browser = Browser('phantomjs')
    is_logged_in = False

    def slugify(self, str):
        return re.sub(r'\W+','_',str).lower()

    def login(self, username, password):
        '''Creates a login session'''

        self.username = username
        self.password = password

        self.browser.visit(self.LOGIN_URL)
        self.browser.fill('username', username)
        self.browser.fill('password', password)
        btn = self.browser.find_by_value('Log in').first
        btn.click()
        if self.browser.title == 'Instagram':
            self.is_logged_in = True
            logger.info('Logged in as %s' % username)
        else:
            self.is_logged_in = False
            logger.error('Loggin Failed for %s' % username)

    def create_api_client(self, app_name, description, website_url, redirect_uri):
        '''Creates a new api client.

           TODO:
           1. Add more error handling cases.
        '''
        result = []

        if not self.is_logged_in:
            logger.error('Must be logged-in to create a api client.')
            return result;

        self.browser.visit(self.REGISTER_CLIENT_URL)
        if self.browser.is_text_present('Too many clients'):
            logger.error('Client limit exceeded for %s' % self.username)
            return result;

        self.browser.fill('name', app_name)
        self.browser.fill('description', description)
        self.browser.fill('website_url', website_url)
        self.browser.fill('redirect_uri', redirect_uri)
        btn = self.browser.find_by_value('Register').first
        btn.click()

        client_card = self.browser.find_by_css('.card.client tbody').first
        rows = client_card.find_by_tag('tr')
        for row in rows:
            key = self.slugify(row.find_by_tag('th').first.text)
            value = row.find_by_tag('td').first.text
            result.append({key: value})

        return result


if __name__ == '__main__':
    from getpass import getpass

    print 'Enter instragram credentials below:'
    username = raw_input('Username (email not allowed) : ')
    password = getpass('Password (will not be displayed) : ')

    bot = InstagramWebBot()
    bot.login(username, password)
    data = bot.create_api_client('test4', 'test4', 'http://helloworld.in', 'http://hello.txt')

    print data
