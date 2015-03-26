# coding: utf-8

# python
import copy

# django
from django import forms

# app
from .models import ObjectFeedback


class ObjectFeedbackModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ObjectFeedbackModelForm, self).__init__(*args, **kwargs)
        self._original = self.instance
        self._fields_changed = []
        self._object_feedback = ObjectFeedback()
        self._object_feedback.content_object = copy.copy(self._original)

    def is_valid(self, *args, **kwargs):
        result = super(ObjectFeedbackModelForm, self).is_valid(*args, **kwargs)

        if result:
            for key, value in self.cleaned_data.iteritems():
                field_type = self._original._meta.get_field(
                    key).get_internal_type()
                self._object_feedback.add_field(key, value, field_type)
                if key in self._object_feedback.changed_fields:
                    self._fields_changed.append((key, value))

            return len(self._fields_changed) > 0

        return result

    def get_fields(self):
        return self._fields_changed

    def save(self):
        # Not needed
        raise Exception("save() method is not needed on this")


class ObjectFeedbackFieldsForm(object):
    def __new__(self, obj, fields, data=None):
        meta = type('Meta', (), {"model": obj, "fields": fields})
        form_class = type('modelform',
                          (ObjectFeedbackModelForm,),
                          {"Meta": meta})
        return form_class(data, instance=obj)


class ObjectFeedbackForm(forms.ModelForm):
    class Meta:
        model = ObjectFeedback
        fields = ('comment', )
