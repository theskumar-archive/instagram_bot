# -*- coding: utf-8 -*-

import re
from logbook import Logger

from splinter import Browser

logger = Logger('InstagramWebBot')

class InstagramWebBot(object):
    '''Instagram Web Bot for automatic things using web browser.'''

    LOGIN_URL = 'https://instagram.com/accounts/login/';
    REGISTER_CLIENT_URL = 'http://instagram.com/developer/clients/register/'
    REGISTER_DEVELOPER_URL = 'http://instagram.com/developer/register/'
    LOGOUT_URL = 'http://instagram.com/accounts/logout/'

    is_logged_in = False
    is_developer = False

    def __init__(self, username, password):
        self.browser = Browser('phantomjs')
        self.username = username
        self.password = password

    def slugify(self, str):
        return re.sub(r'\W+','_',str).lower()

    def login(self):
        '''Creates a login session'''

        self.browser.visit(self.LOGIN_URL)
        self.browser.fill('username', self.username)
        self.browser.fill('password', self.password)
        btn = self.browser.find_by_value('Log in').first
        btn.click()
        if self.browser.title == 'Instagram':
            self.is_logged_in = True
            logger.info('Logged in as %s' % self.username)
        else:
            self.is_logged_in = False
            logger.error('Login Failed for %s' % self.username)

    def register_developer(self, website="", phone_number="", description=""):
        '''
        Registers the user for developer access in instagram
        '''
        result = {}

        if not self.is_logged_in:
            logger.error('Must be logged-in to create register as a developer.')
            return result;

        self.browser.visit(self.REGISTER_DEVELOPER_URL)
        if self.browser.is_text_present('Hello Developers.'):
          logger.info('Developer registration done')
          self.is_developer = True
        elif self.browser.is_text_present('Developer Signup'):
            logger.info('Registering as developer')
            self.browser.fill('website', website)
            self.browser.fill('phone_number', phone_number)
            self.browser.fill('description', description)
            self.browser.check('accept_terms')
            btn = self.browser.find_by_value('Sign up').first
            btn.click()
            self.register_developer(website, phone_number, description)
        else:
            logger.info('Developer registration failed')
            self.is_developer = False

        return result

    def create_api_client(self, app_name, description, website_url, redirect_uri):
        '''Creates a new api client.

           TODO:
           1. Add more error handling cases.
        '''
        result = {}

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
            result.update({key: value})

        return result

    def __del__(self):
        self.browser.quit()
