from django.contrib import admin

from alert_user.models import AlertUser, Rule

admin.site.register(AlertUser)
admin.site.register(Rule)
