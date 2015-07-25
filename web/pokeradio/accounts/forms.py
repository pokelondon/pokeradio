from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm


class RegistrationFormWhiteListDomains(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which checks the domain is whitelisted
    """
    allowed_domains = settings.REGISTRATION_DOMAIN_WHITELIST

    def clean_email(self):
        """
        Check the supplied email address against the approved domains
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain not in self.allowed_domains:
            raise forms.ValidationError(_("Your email address isn't allowed"))
        return self.cleaned_data['email']
