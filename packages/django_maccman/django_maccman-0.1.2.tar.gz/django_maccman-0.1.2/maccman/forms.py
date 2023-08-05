from django.contrib.auth.forms import AuthenticationForm
from django.forms import forms
from django.utils.translation import gettext as _

from .models import UserProfile


class UserProfileAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise forms.ValidationError(_('No profile found for this user'),
                                        code='no_profile')
