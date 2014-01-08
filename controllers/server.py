"""
@author: Dimitrios Kanellopoulos
@contact: jimmykane9@gmail.com
"""

import os
import re
import json
import logging
import config

from urlparse import urlparse

import webapp2
import jinja2

from google.appengine.api import urlfetch


class RootPage(webapp2.RequestHandler):

    def get(self):
        jinja_environment = self.jinja_environment
        template = jinja_environment.get_template("/index.html")
        self.response.out.write(template.render())

    def post(self):
        string = str(self.request.get('string'))
        facebook_page_name = ''
        facebook_page_id = ''
        data = False

        try:
            pieces = urlparse(string)
            logging.info(pieces)
            if pieces.scheme == 'http' or pieces.scheme == 'https':
                is_url = True
                string = pieces.path
        except Exception as e:
            # it's not a url or blah
            pass

        url = 'https://graph.facebook.com/' + string

        result = urlfetch.fetch(url)
        if result.status_code == 200:
            try:
                data = json.loads(result.content)
                facebook_page_id = data['id']
                facebook_page_name = data['username']
            except Exception as e:
                pass

        if not data:
            self.response.out.write('Could not find a Facebook page id')
            return

        self.response.out.write(
            'Found Facebook Page with name: "' + facebook_page_name + '" and id: ' + str(facebook_page_id)
        )


    @property
    def jinja_environment(self):
        jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(
                    os.path.dirname(__file__),
                    '../views'
                )
            )
        )
        return jinja_environment