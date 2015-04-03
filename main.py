#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from webapp2_extras import sessions
import os
import jinja2

from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
        
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        self.render('index.html')

webapp2_config = {}
webapp2_config['webapp2_extras.sessions'] = {
        'secret_key': 'aldfnv;ladnfv:_+%^&!()HUTD<><><ndflsfnvl;dsfnvskdfnvfd',
    }

app = webapp2.WSGIApplication([
    ('/', MainPage),
], config=webapp2_config, debug=True)
