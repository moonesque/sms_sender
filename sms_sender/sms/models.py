import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from authnz.models import User


def generate_contact_id():
    return '-'.join(['c', uuid.uuid4().hex[:16]])


def generate_group_id():
    return '-'.join(['g', uuid.uuid4().hex[:16]])


class Contact(models.Model):
    name = models.CharField(
        max_length=255,
        unique=False,
        help_text=_('Required. 150 characters or fewer. Letters and spaces only'),
    )
    phone = PhoneNumberField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_id = models.CharField(max_length=18, default=generate_contact_id, unique=True)

    def __str__(self):
        return self.contact_id


class ContactGroup(models.Model):
    name = models.CharField(
        max_length=255,
        unique=False,
        help_text=_('Required. 150 characters or fewer. Letters and spaces only'),
    )
    contacts = models.ManyToManyField(Contact)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.CharField(max_length=18, default=generate_group_id, unique=True)

    def __str__(self):
        return self.group_id
