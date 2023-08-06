from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from cms.common import mixins

from .models import Message, MassMessage


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(MessageAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['recipients'].widget.attrs['class'] = 'no-tinymce'
        return form

    def html_content(self, obj):
        return obj.content
    html_content.short_description = _('Content')
    html_content.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('subject', 'recipients', 'html_content', 'reply_to',
                    'created', 'sent', 'postdate')
        else:
            return ()

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'html_content',
                               'reply_to', ('created', 'sent', 'postdate'))
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'content', 'reply_to')
                }),
            )

    list_display = ('subject', 'recipients', 'reply_to', 'created', 'sent',
                    'postdate')
    list_filter = ('sent',)
    search_fields = ('subject', 'recipients', 'reply_to', 'content')

    class Media:
        js = mixins.TinyMCE.js


@admin.register(MassMessage)
class MassMessageAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            url(
                r'^(\d+)/send/$',
                self.admin_site.admin_view(self.send_view),
                name='emails_massmessage_send',
            ),
        ] + super(MassMessageAdmin, self).get_urls()

    def send_view(self, request, id):
        try:
            obj = MassMessage.objects.get(pk=id, sent=False)
            for r in obj.recipients.values_list('email', flat=True):
                if not r:
                    continue
                Message.objects.create(
                    subject=obj.subject,
                    recipients=r,
                    content=obj.content,
                    reply_to=obj.reply_to,
                    send_immediately=False
                )
            obj.sent = True
            obj.sent_date = timezone.now()
            obj.save()
            self.message_user(
                request,
                _('Mass message has been queued for sending.'),
                level=messages.SUCCESS
            )
        except MassMessage.DoesNotExist:
            self.message_user(
                request,
                _('Mass message object does not exist or has been already '
                  'sent.'),
                level=messages.ERROR
            )
        return redirect(reverse('admin:emails_massmessage_changelist'))

    def send_link(self, obj):
        if obj.pk and not obj.sent:
            return '<a href="{}">{}</a>'.format(
                reverse('admin:emails_massmessage_send', args=(obj.pk,)),
                _('Send')
            )
        else:
            return ''
    send_link.short_description = _('Send')
    send_link.allow_tags = True

    def html_content(self, obj):
        return obj.content
    html_content.short_description = _('Content')
    html_content.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.sent:
            return ('subject', 'recipients', 'html_content', 'reply_to',
                    'created', 'sent', 'postdate')
        else:
            return ()

    def get_fieldsets(self, request, obj=None):
        if obj and obj.sent:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'html_content',
                               'reply_to', ('created', 'sent', 'postdate'))
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'content', 'reply_to')
                }),
            )

    list_display = (
        'subject', 'reply_to', 'created', 'sent', 'postdate', 'send_link'
    )
    list_filter = ('sent',)
    search_fields = ('subject', 'reply_to', 'content')

    filter_horizontal = ('recipients',)

    class Media:
        js = mixins.TinyMCE.js
