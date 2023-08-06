from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from social_core.exceptions import AuthException


class EmailIsTaken(AuthException):
    def __str__(self):
        return _('Email address associated with this account is already '
                 'taken.')


def is_email_taken(backend, uid, user=None, social=None, *args, **kwargs):
    email = kwargs['details'].get('email')
    try:
        existing_user = get_user_model().objects.get(email=email)
        if existing_user == user:
            return
        else:
            raise EmailIsTaken(backend)
    except get_user_model().DoesNotExist:
        return
