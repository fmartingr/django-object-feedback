# coding: utf-8

# python
import copy

# django
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType

# 3rd party
import jsonfield


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
                               related_name="feedback_sent")

    # Dates
    submitted = models.DateTimeField(auto_now_add=True)

    comment = models.TextField(null=True, blank=True)

    # Staff
    reviewed = models.DateTimeField(null=True, blank=True)
    valid = models.NullBooleanField(default=None)

    def get_actual_value_from_key(self, key):
        return getattr(self.object, key, None)

    def set_changed_field(self, key, value):
        self.changed_fields[key] = value
        print('set')
        print(self.changed_fields)

    def add_field(self, key, value, field_type):
        """
        Adds the desired field to the current feedback instance
        The method will check if the field has changed, if not, it wont
        save the field within the feedback.
        If the field is a special field (like a relation) a custom method
        is called to interact with those.
        Currently supported fields: TODO
        """

        if getattr(self, 'add_field_{}'.format(field_type.lower()), None):
            method = getattr(self, 'add_field_{}'.format(field_type.lower()))
            method(key, value)
        elif self.get_actual_value_from_key(key) != value:
            self.set_changed_field(key, value)

    def add_field_manytomanyfield(self, key, qs):
        val = self.get_actual_value_from_key(key)
        if (
            set(val.values_list('id',
                                flat=True)) != set(qs.values_list('id',
                                                                  flat=True))
        ):
            value = list(qs.values_list('id', flat=True))
            self.set_changed_field(key, value)

    def add_field_foreignkey(self, key, obj):
        val = self.get_actual_value_from_key(key)
        if val.pk != obj.pk:
            value = obj.pk
            self.set_changed_field(key, value)

    def __unicode__(self):
        return '{}: {} - {}'.format(
            ugettext('User feedback'), self.content_type, self.content_object)

    @property
    def object(self):
        return self.content_object

    class Meta:
        verbose_name = _('Object feedback')
        verbose_name_plural = _('Object feedbacks')
