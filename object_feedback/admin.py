# coding: utf-8

# django
from django.contrib import admin
from django.conf.urls import url
from django.template.response import TemplateResponse

# app
from .models import ObjectFeedback


# Admin actions
def mark_as_invalid(modeladmin, request, queryset):
    for item in queryset:
        item.mark_as_invalid()


def mark_as_valid(modeladmin, request, queryset):
    for item in queryset:
        item.mark_as_valid()


class FeedbackAdmin(admin.ModelAdmin):
    # Override templates
    change_list_template = 'admin/object_feedback/list.html'
    change_form_template = 'admin/object_feedback/review.html'
    review_template = 'admin/object_feedback/review.html'
    actions = (mark_as_invalid, mark_as_valid, )

    list_display = ('submitted', 'content_object', 'valid', 'reviewed', )

    def get_urls(self):
        urls = super(FeedbackAdmin, self).get_urls()
        my_urls = [
            url(r'^2(?P<pk>\d+)/$',
                self.admin_site.admin_view(self.review_view))
        ]
        return my_urls + urls

    def review_view(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        context = dict(
            self.admin_site.each_context(),
            object=obj,
        )
        return TemplateResponse(
            request,
            self.review_template,
            context)

    def has_add_permission(self, request):
        """
        Not adding feedback from admin.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(FeedbackAdmin, self).get_actions(request)

        # Remove delete action
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

admin.site.register(ObjectFeedback, FeedbackAdmin)
