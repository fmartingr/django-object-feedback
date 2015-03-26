# coding: utf-8

# django
from django.views.generic import View
from django.utils.translation import ugettext as _
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType

# app
from .forms import ObjectFeedbackForm, ObjectFeedbackFieldsForm
from .models import ObjectFeedback
from .mixins import ObjectFeedbackMixin


class BaseFeedbackView(View):
    # Template to render to
    template = 'object_feedback/main.html'
    thanks_template = 'object_feedback/thanks.html'

    # Model to use (if needed)
    feedback_model = None

    # Dual form errors
    form_errors = {
        'fill_something': _('You need to enter a comment for this feedback or '
                            'provide some modifications in order to send it.')
    }

    def get_feedback_instance(self, request, obj=None):
        """
        """
        instance = ObjectFeedback(author=request.user)
        if obj:
            instance.content_object = obj
        return instance

    def get(self, request, *args, **kwargs):
        """
        GET
        Shows the form for the object to add a feedback to.

        Uses get_object() to get the object instance
        """
        context = {}

        # Check if we're adding feedback to an object of if it is global
        # feedback
        if self.feedback_model:
            # Get object to add a feedback to, and a base feedback instance
            obj = self.get_object(request, *args, **kwargs)
            context['object'] = obj

            # Get the fields form for the object to add a feedback
            object_form = ObjectFeedbackFieldsForm(obj,
                                                   obj.get_feedback_fields())
            context['object_form'] = object_form

        # Create a base feedback form
        context['feedback_form'] = ObjectFeedbackForm()

        ctx = RequestContext(request, context)
        return render_to_response(self.template, context_instance=ctx)

    def post(self, request, *args, **kwargs):
        """
        POST
        """
        template = self.template
        context = {'errors': []}
        error = True
        fields = ()

        if self.feedback_model:
            obj = self.get_object(request, *args, **kwargs)
            context['object'] = obj

            object_form = ObjectFeedbackFieldsForm(obj,
                                                   obj.get_feedback_fields(),
                                                   data=request.POST)

            feedback_form = ObjectFeedbackForm(
                request.POST,
                instance=self.get_feedback_instance(request, obj))

            if object_form.is_valid():
                error = False
                fields = object_form.get_fields()

        if feedback_form.is_valid():
            feedback_object = feedback_form.save(commit=False)

            if fields or feedback_object.comment:
                error = False
                obj.add_feedback(
                    author=request.user,
                    comment=feedback_object.comment,
                    fields=fields
                )

                template = self.thanks_template
            else:
                context['errors'].append(self.form_errors['fill_something'])

        if error:
            context['feedback_form'] = feedback_form
            context['object_form'] = object_form

        ctx = RequestContext(request, context)
        return render_to_response(template, context_instance=ctx)


class ObjectFeedbackView(BaseFeedbackView):
    """
    Base object feedback view to display a form
    """

    feedback_model = 'auto'  # Just to make sure it checks for get_object()

    def get_object(self, request, ct_pk, obj_pk):
        # Get the content type and object model
        try:
            content_type = ContentType.objects.get(pk=int(ct_pk))
            obj = content_type.model_class().objects.get(pk=int(obj_pk))
        except Exception as e:
            # Assuming any error we got from this is a DoesNotExist for the
            # ContentType or the model_class
            raise Http404(e)

        # Raise 404 if trying to add feedback for an object not allowed to
        if not isinstance(obj, ObjectFeedbackMixin):
            raise Http404()

        return obj


class FeedbackView(BaseFeedbackView):
    pass
