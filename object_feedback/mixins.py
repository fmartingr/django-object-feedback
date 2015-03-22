# coding: utf-8

# django
from django.db import models
from django.db import transaction
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

# app
from .models import ObjectFeedback


class ObjectFeedbackMixin(models.Model):
    feedbacks = generic.GenericRelation(ObjectFeedback)

    @transaction.atomic
    def add_feedback(self, author, comment=None, fields=()):
        """
        Adds a feedback to the current object.

        Parameters:
            author: A AUTH_USER_MODEL instance
            fields: A tuple of fields as ('<key>', '<value>')
        """
        # Create feedback object
        obj_feedback = ObjectFeedback(author=author, content_object=self)
        obj_feedback.save()

        # Add fields for feedback check
        for key, value in fields:
            # Check if the field is allowed to receive feedback
            if key in self.feedback_fields:
                field_type = self._meta.get_field(key).get_internal_type()
                obj_feedback.add_field(key, value, field_type)

        return obj_feedback

    @property
    def pending_review(self):
        return (self.feedbacks.filter(reviewed__isnot=None).count())

    def get_feedback_url(self):
        ct_obj = ContentType.objects.get_for_model(self)
        return reverse('object_feedback:object', kwargs={'ct_pk': ct_obj.pk,
                                                         'obj_pk': self.pk})

    class Meta:
        abstract = True
