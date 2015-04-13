# coding: utf-8

# django
from django.contrib import admin

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

    def has_add_permission(self, request):
        """
        Not adding feedback from admin.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Feedback is not deleted, is marked as invalid.
        """
        return False

    def get_actions(self, request):
        """
        Removing default delete action from list.
        WHY U NOT DO THIS WITH self.has_delete_permission() ??!
        """
        actions = super(FeedbackAdmin, self).get_actions(request)

        # Remove delete action
        if not self.has_delete_permission(request):
            del actions['delete_selected']

        return actions

admin.site.register(ObjectFeedback, FeedbackAdmin)
