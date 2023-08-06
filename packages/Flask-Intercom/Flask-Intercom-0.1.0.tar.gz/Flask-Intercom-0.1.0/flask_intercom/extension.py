#
# Flask-Intercom
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


import hashlib
import hmac
import logging

import itsdangerous
import requests

from flask import Response, abort, request
from six.moves.http_client import BAD_REQUEST, OK

from .signals import namespace


logger = logging.getLogger('Flask-Intercom')

BASE_URL = 'https://api.intercom.io'


class Intercom(object):
    """
    Flask-Intercom

    Documentation:
    https://flask-intercom.readthedocs.io

    API:
    https://developers.intercom.com/reference

    Inspiration:
    https://github.com/nikentic/flask-intercom
    https://django-intercom.readthedocs.io
    https://django-intercom-io.readthedocs.io

    :param app: Flask app to initialize with. Defaults to `None`
    """

    secret_key = None

    hub_secret = None

    def __init__(self, app=None, blueprint=None):

        session = requests.Session()
        session.headers = {'Accept': 'application/json'}
        self.session = session

        if app is not None:
            self.init_app(app, blueprint)

    def init_app(self, app, blueprint=None):

        self.secret_key = app.config.get('INTERCOM_SECRET_KEY')
        self.hub_secret = app.config.get('INTERCOM_HUB_SECRET')

        app.add_template_filter(self._user_hash, 'intercom_user_hash')

        if blueprint is not None:
            blueprint.add_url_rule('/intercom', 'intercom', self.handle_webhook, methods=['POST'])

    def create_user(self, **user):
        """
        https://doc.intercom.io/api/#create-or-update-user
        """
        response = self.session.post(BASE_URL + '/users', json=user)
        response.raise_for_status()
        return response.json()

    def create_event(self, **event):
        """
        https://doc.intercom.io/api/#submitting-events
        """
        response = self.session.post(BASE_URL + '/events', json=event)
        response.raise_for_status()
        return response.json()

    def send_message(self, message_type, admin_id, user_id, subject, body, user_email=None):
        """
        https://doc.intercom.io/api/#admin-initiated-conversation
        """
        if message_type == 'email' and subject is None:
            raise ValueError('Need to specify subject for email')

        if user_id is not None:
            to = {'type': 'user', 'id': str(user_id)}
        elif user_email is not None:
            to = {'type': 'user', 'email': user_email}
        else:
            raise ValueError('Need to specify either user_id or user_email')

        data = {
            'message_type': message_type,
            'subject': subject,
            'body': body,
            'from': {'type': 'admin', 'id': str(admin_id)},
            'to': to
        }
        response = self.session.post(BASE_URL + '/messages', json=data)
        response.raise_for_status()
        return response.json()

    def handle_webhook(self):
        """
        https://developers.intercom.com/reference#webhooks-and-notifications
        """

        hub_signature = request.headers.get('x-hub-signature')
        if hub_signature is None:
            abort(BAD_REQUEST)

        algorithm, signature = hub_signature.split('=')
        if not all((algorithm == 'sha1', signature)):
            abort(BAD_REQUEST)

        digest = hmac.new(self.hub_secret.encode(), request.data, hashlib.sha1).hexdigest()
        if not itsdangerous.constant_time_compare(digest, signature):
            abort(BAD_REQUEST)

        event = request.get_json()
        namespace.signal(event.get('topic')).send(self, item=event['data']['item'])

        return Response(status=OK)

    def _user_hash(self, user_id):
        """
        https://docs.intercom.com/configure-intercom-for-your-product-or-site/staying-secure/enable-secure-mode-on-your-web-product
        """
        return hmac.new(self.secret_key.encode(), str(user_id).encode(), hashlib.sha256).hexdigest()


# EOF
