from django.db import models
from django.contrib.auth.models import User

from cryptofield import CryptoField

MAX_ADDRESS_LENGTH = 253
MIN_ACCOUNT_LENGTH = 1
MIN_DOMAIN_LENGTH = 4
MAX_ACCOUNT_LENGTH = MAX_ADDRESS_LENGTH - MIN_DOMAIN_LENGTH
MAX_DOMAIN_LENGTH = MAX_ADDRESS_LENGTH - MIN_ACCOUNT_LENGTH


class Domain(models.Model):
    name = models.CharField(unique=True, max_length=MAX_DOMAIN_LENGTH)
    owner = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Target(models.Model):
    address = models.CharField(unique=True, max_length=MAX_ADDRESS_LENGTH + 1)

    def __str__(self):
        return self.address


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    allowed_domains = models.ManyToManyField(Domain,
                                             db_table="maccman_users_domains",
                                             blank=True)

    def __str__(self):
        return "{0} {1} ({2})".format(self.user.first_name,
                                      self.user.last_name,
                                      self.user.username)


class Identity(models.Model):
    account = models.CharField(max_length=MAX_ACCOUNT_LENGTH)
    enabled = models.BooleanField(default=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain)

    class Meta:
        unique_together = ('account', 'domain',)
        abstract = True

    def __str__(self):
        return "{0}@{1}".format(self.account, self.domain)


class Mailbox(Identity):
    password = CryptoField()

    class Meta(Identity.Meta):
        verbose_name_plural = "mailboxes"

    def __str__(self):
        return "Mailbox " + super(Mailbox, self).__str__()


class Alias(Identity):
    targets = models.ManyToManyField(Target,
                                     db_table="maccman_aliases_targets")

    class Meta(Identity.Meta):
        verbose_name_plural = "aliases"

    def __str__(self):
        return "Alias " + super(Alias, self).__str__()
