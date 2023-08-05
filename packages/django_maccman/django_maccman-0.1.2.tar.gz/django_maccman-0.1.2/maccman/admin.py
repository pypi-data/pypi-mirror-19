from django.contrib import admin

from .models import Alias, Domain, Mailbox, Target, UserProfile

admin.site.register([Alias, Domain, Mailbox, Target, UserProfile])
