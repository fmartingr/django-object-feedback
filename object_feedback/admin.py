from django.contrib import admin
from .models import ObjectFeedback


class FeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(ObjectFeedback, FeedbackAdmin)
