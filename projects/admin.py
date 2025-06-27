from django.contrib import admin

from .models import Project, Category, Donation, ProjectImage
class ProjectImageInline(admin.TabularInline):  # Or use admin.StackedInline
    model = ProjectImage
    extra = 1 # to add each time
    fields = ['image']  # only show image field in inline form
    show_change_link = False
    can_delete = True
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_goal', 'donations_amount', 'progress', 'user', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('categories', 'created_at')
    inlines = [ProjectImageInline]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ar')

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'amount', 'payment_status', 'created_at')
    
@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
    
