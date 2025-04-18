from django.contrib import admin
from .models import Project, Category, ProjectImage

# Inline for showing images inside Project admin
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Number of empty forms to show
    readonly_fields = ['image']  # Optional: if you just want to view image in admin

@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price_goal', 'donations_amount', 'progress', 'created_at')
    list_filter = ('created_at', 'categories')
    search_fields = ('title', 'title_ar', 'user__username')
    inlines = [ProjectImageInline]
    filter_horizontal = ('categories',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_ar')
    search_fields = ('title', 'title_ar')

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
