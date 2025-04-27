from django.contrib import admin

# Now you can use the decorator to register models with the Django Admin
from .models import Project, Category, Donation, ProjectImage
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_goal', 'donations_amount', 'progress', 'user', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ar')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'amount', 'payment_status', 'created_at')
    
@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
