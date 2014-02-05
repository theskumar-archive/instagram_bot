# -*- coding: utf-8 -*-

import re
from logbook import Logger
import random
import string

from splinter import Browser

logger = Logger('InstagramWebBot')

def random_string_generator(size=0, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    if size == 0:
        size = random.randint(1, 8)
    return ''.join(random.choice(chars) for x in range(size))

class InstagramWebBot(object):
    '''Instagram Web Bot for automatic things using web browser.'''

    LOGIN_URL = 'http://instagram.com/accounts/login/';
    MANAGE_CLIENTS_URL =  'http://instagram.com/developer/clients/manage/'
    REGISTER_CLIENT_URL = 'http://instagram.com/developer/clients/register/'
    REGISTER_DEVELOPER_URL = 'http://instagram.com/developer/register/'
    LOGOUT_URL = 'http://instagram.com/accounts/logout/'
    CHANGE_PASSWORD_URL = 'http://instagram.com/accounts/password/change/'

    is_logged_in = False
    is_developer = False

    def __init__(self, username, password):
        self.browser = Browser('firefox')
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

    def change_password(self):
        self.browser.visit(self.CHANGE_PASSWORD_URL)
        new_password = random_string_generator(8)
        self.browser.fill('old_password', self.password)
        self.browser.fill('new_password1', new_password)
        self.browser.fill('new_password2', new_password)
        btn = self.browser.find_by_value('Change Password').first
        btn.click()
        if self.browser.is_text_present('Thanks! You have successfully changed your password.'):
          logger.info('Password Changed')
          logger.info(new_password)
          return new_password
        else:
          return None


    def register_developer(self, website="", phone_number="", description=""):
        '''
        Registers the user for developer access in instagram
        '''
        result = {}

        if not self.is_logged_in:
            logger.error('Must be logged-in to create register as a developer.')
            return result;

        self.browser.visit(self.MANAGE_CLIENTS_URL)
        if self.browser.is_text_present('Developer Signup'):
            logger.info('Registering as developer')
            self.browser.fill('website', website)
            self.browser.fill('phone_number', phone_number)
            self.browser.fill('description', description)
            self.browser.check('accept_terms')
            btn = self.browser.find_by_value('Sign up').first
            btn.click()
            self.register_developer(website, phone_number, description)
        elif self.browser.is_text_present('Register a New Client'):
          logger.info('Developer registration done')
          self.is_developer = True
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

    def fill_api_client_form(self):
        if not self.is_logged_in:
            logger.error('Must be logged-in to create a api client.')
            return result;

        app_name = random_string_generator()
        description = random_string_generator()
        website_url = random_string_generator()
        redirect_uri = 'http://dev.lovematically.fueled.com/complete/instagram'

        self.browser.visit(self.REGISTER_CLIENT_URL)
        self.browser.fill('name', app_name)
        self.browser.fill('description', description)
        self.browser.fill('website_url', website_url)
        self.browser.fill('redirect_uri', redirect_uri)

    def get_api_clients(self):
        self.browser.visit(self.MANAGE_CLIENTS_URL)
        client_cards = self.browser.find_by_css('.card.client')
        clients = []
        for client_card in client_cards:
          rows = client_card.find_by_tag('tbody').find_by_tag('tr')
          name = client_card.find_by_tag('h2').first.text
          result = {}
          for row in rows:
              key = self.slugify(row.find_by_tag('th').first.text)
              value = row.find_by_tag('td').first.text
              result.update({key: value})
          result.update({'name': name})
          clients.append(result)

        return clients



    def __del__(self):
        self.browser.quit()
