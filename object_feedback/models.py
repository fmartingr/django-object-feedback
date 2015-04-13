# coding: utf-8

# python
import copy

# django
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType

# 3rd party
import jsonfield

# app
from .fields import fields_map


class ObjectFeedback(models.Model):
    """
    """
    # Object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    changed_fields = jsonfield.JSONField()

    # Author
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="feedback_sent",
                               blank=True, null=True)

    # Dates
    submitted = models.DateTimeField(auto_now_add=True)

    comment = models.TextField(null=True, blank=True)

    # Staff
    reviewed = models.DateTimeField(null=True, blank=True)
    valid = models.NullBooleanField(default=None)

    def set_changed_field(self, key, value):
        self.changed_fields[key] = value

    def add_field(self, key, value, field_type):
        """
        Adds the desired field to the current feedback instance
        The method will check if the field has changed, if not, it wont
        save the field within the feedback.
        If the field is a special field (like a relation) a custom method
        is called to interact with those.
        Currently supported fields: TODO
        """

        if field_type in fields_map:
            field = fields_map[field_type](self.object, key, value)
        else:
            raise Exception('{}: Not implemented'.format(field_type))

        if field.has_changed():
            self.set_changed_field(key, value)

    def mark_as_valid(self, fields=()):
        """
        Mark this feedback as valid and change the fields in the content_object
        with the provided in this feedback
        """
        # TODO selective fields
        # TODO change fields
        if not self.reviewed:
            self.valid = True
            self.reviewed = now()
            self.save()

    def mark_as_invalid(self):
        """
        Mark this feedback as not valid and reviewed.
        """
        if not self.reviewed:
            self.valid = False
            self.reviewed = now()
            self.save()

    def __unicode__(self):
        return u'{}: {} - {}'.format(
            _('User feedback'), self.content_type, self.content_object)

    @property
    def object(self):
        return self.content_object

    class Meta:
        verbose_name = _('Object feedback')
        verbose_name_plural = _('Object feedbacks')
