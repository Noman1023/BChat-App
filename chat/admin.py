from django.contrib import admin
from django.contrib.auth import get_user_model

from chat.models import *
from django.utils.translation import gettext, gettext_lazy as _

# User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    """Define admin model for custom User model with no email field."""

    class Meta:
        model = User

    fieldsets = (
        (None, {'fields': ('image', 'friends', 'friend_requests')}),

        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('id',),
    #     }),
    # )
    # list_display = ('user_id',)
    # search_fields = ('user_id',)
    # ordering = ('user_id',)
    #

admin.site.register(User, UserAdmin)
admin.site.register(Notification)
admin.site.register(Channel)
admin.site.register(Thread)
admin.site.register(Message)
