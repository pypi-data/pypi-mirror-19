from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminOverride(UserAdmin):
    # removes first_name and last_name from admin site
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets
    fieldsets[1][1]['fields'] = ('email',)


admin.site.unregister(User)
admin.site.register(User, UserAdminOverride)
