from django.contrib import admin

from .models import Subscribers
@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_date', )
    search_fields = ('email', 'subscription_date',)
    list_filter = ('email', 'subscription_date',)
