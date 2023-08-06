#
# Flask-Intercom
#
# Copyright (C) 2017 Boris Raicheff
# All rights reserved
#


from flask.signals import Namespace


# https://developers.intercom.io/docs/topics
namespace = Namespace()


# Conversation
conversation_user_created = namespace.signal('conversation.user.created')
conversation_user_replied = namespace.signal('conversation.user.replied')
conversation_admin_replied = namespace.signal('conversation.admin.replied')
conversation_admin_assigned = namespace.signal('conversation.admin.assigned')
conversation_admin_noted = namespace.signal('conversation.admin.noted')
conversation_admin_closed = namespace.signal('conversation.admin.closed')
conversation_admin_opened = namespace.signal('conversation.admin.opened')

# User
user_created = namespace.signal('user.created')
user_deleted = namespace.signal('user.deleted')
user_unsubscribed = namespace.signal('user.unsubscribed')
user_email_updated = namespace.signal('user.email.updated')

# UserTag
user_tag_created = namespace.signal('user.tag.created')
user_tag_deleted = namespace.signal('user.tag.deleted')

# Lead
contact_created = namespace.signal('contact.created')
contact_signed_up = namespace.signal('contact.signed_up')
contact_added_email = namespace.signal('contact.added_email')

# Company
company_created = namespace.signal('company.created')

# Event
event_created = namespace.signal('event.created')

# Ping
ping = namespace.signal('ping')


# EOF
