from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import signing

from cms.emails.models import Message


def send_activation_message(user, request):
    key = signing.dumps({'action': 'ACTIVATE', 'user': user.pk})
    link = '<a href="{0}">{0}</a>'.format(
        request.build_absolute_uri(
            '{}/accounts/activate/{}'.format(
                settings.FRONTEND_ADDRESS, key
            )
        )
    )
    content = (
        '<div style="margin-bottom: 20px;">{}</div>\r\n\r\n'
        '<div>{}</div>'
    ).format(
        _('Your accounts has been created. To activate it click on link '
          'below, or copy it to your browser.'), link
    )
    Message.objects.create(
        subject=_('Activate your account'),
        recipients=user.email,
        content=content,
        reply_to='no-reply'
    )


def send_reset_password_message(user, request):
    key = signing.dumps({'action': 'RESET_PASSWORD', 'user': user.pk})
    link = '<a href="{0}">{0}</a>'.format(
        request.build_absolute_uri(
            '{}/accounts/reset-password/{}'.format(
                settings.FRONTEND_ADDRESS, key
            )
        )
    )
    content = (
        '<div style="margin-bottom: 20px;">{}</div>\r\n\r\n'
        '<div>{}</div>'
    ).format(
        _('To change you password click on link below, or copy it to your '
          'browser.'), link
    )
    Message.objects.create(
        subject=_('Change your password'),
        recipients=user.email,
        content=content,
        reply_to='no-reply'
    )


def send_change_email_confirmation_message(new_email, request):
    key = signing.dumps({
        'action': 'CHANGE_EMAIL',
        'user': request.user.pk,
        'new_email': new_email
    })
    link = '<a href="{0}">{0}</a>'.format(
        request.build_absolute_uri(
            '{}/accounts/change-email-confirmation/{}'.format(
                settings.FRONTEND_ADDRESS, key
            )
        )
    )
    content = (
        '<div style="margin-bottom: 20px;">{}</div>\r\n\r\n'
        '<div>{}</div>'
    ).format(
        _('To change you email click on link below, or copy it to your '
          'browser.'), link
    )
    Message.objects.create(
        subject=_('Change your password'),
        recipients=new_email,
        content=content,
        reply_to='no-reply'
    )
