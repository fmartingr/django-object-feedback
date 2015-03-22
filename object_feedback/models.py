# coding: utf-8

# django
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType


class ObjectFeedback(models.Model):
    """
    """
    # Object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    # Author
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="feedback_sent")

    # Dates
    submitted = models.DateTimeField(auto_now_add=True)

    comment = models.TextField(null=True, blank=True)

    # Staff
    reviewed = models.DateTimeField(null=True, blank=True)
    valid = models.NullBooleanField(default=None)

    def add_field(self, key, value, field_type):
        """
        NOTE: Must always be called from obj.add_feedback()
        """
        attribute = ObjectAttributeFeedback(
            feedback=self, field_type=field_type, field=key, value=value)
        attribute.save()

        return attribute

    def __unicode__(self):
        return '{}: {} - {}'.format(
            ugettext('User feedback'), self.content_type, self.content_object)

    @property
    def object(self):
        return self.content_object

    class Meta:
        verbose_name = _('Object feedback')
        verbose_name_plural = _('Object feedbacks')


class ObjectAttributeFeedback(models.Model):
    """
    """
    _base_params = {'blank': True, 'null': True}
    _field_mappings = {
        'CharField': 'text',
        'TextField': 'text',
        'URLField': 'text',
        'SlugField': 'slug',
        'DateField': 'date',
        'DateTimeField': 'datetime',
        'BooleanField': 'boolean',
        'NullBooleanField': 'nullboolean',
    }

    feedback = models.ForeignKey(ObjectFeedback, related_name='fields')
    field = models.CharField(max_length=64)
    field_type = models.CharField(max_length=20)

    value_text = models.TextField(**_base_params)
    value_date = models.DateField(**_base_params)
    value_datetime = models.DateTimeField(**_base_params)
    value_boolean = models.BooleanField(blank=True, default=False)
    value_nullboolean = models.NullBooleanField(**_base_params)
    value_slug = models.SlugField(**_base_params)

    @property
    def value_field_name(self):
        try:
            field = 'value_{}'.format(self._field_mappings[self.field_type])
            return field
        except IndexError:
            raise Exception('{} are not supported at the moment'.format(
                self.field_type))

    @property
    def value(self):
        value_field = self.value_field_name
        return getattr(self, value_field, None)

    @value.setter
    def value(self, value):
        value_field = self.value_field_name
        setattr(self, value_field, value)
