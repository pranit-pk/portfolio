from django.contrib import admin
from .models import Project, ContactMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Customized admin interface for Project model with focus on usability."""
    
    list_display = ('title', 'tech_stack_preview', 'is_featured', 'order', 'created_at')
    list_editable = ('order', 'is_featured')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'slug', 'short_description')
    
    fieldsets = (
        ('Project Identity', {
            'fields': ('title', 'slug', 'short_description'),
            'description': 'Core project information'
        }),
        ('Content', {
            'fields': ('description', 'tech_stack'),
        }),
        ('Media & Links', {
            'fields': ('thumbnail', 'github_url', 'live_url'),
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order'),
            'description': 'Control visibility and positioning'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make slug readonly only for existing objects to allow customization on creation."""
        if obj:
            return ('slug', 'created_at', 'updated_at')
        return ('created_at', 'updated_at')
    
    def tech_stack_preview(self, obj):
        """Display a truncated version of tech stack in list view."""
        tech = obj.tech_stack.replace(', ', ' • ')
        if len(tech) > 50:
            return tech[:47] + '...'
        return tech
    tech_stack_preview.short_description = 'Tech Stack'
    
    class Media:
        css = {
            'all': ('admin/css/project_admin.css',)
        }


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for contact messages with focus on readability and moderation."""
    
    list_display = ('contact_info', 'subject_preview', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    list_per_page = 25
    
    fieldsets = (
        ('From', {
            'fields': ('name', 'email', 'phone'),
            'description': 'Sender information'
        }),
        ('Message', {
            'fields': ('subject', 'message'),
        }),
        ('Status', {
            'fields': ('is_read', 'created_at'),
            'description': 'Message status and timestamp'
        }),
    )
    
    def contact_info(self, obj):
        """Display sender name and email."""
        return f"{obj.name} <{obj.email}>"
    contact_info.short_description = 'Contact'
    
    def subject_preview(self, obj):
        """Display truncated subject line."""
        if len(obj.subject) > 50:
            return obj.subject[:47] + '...'
        return obj.subject
    subject_preview.short_description = 'Subject'
    
    def get_queryset(self, request):
        """Order by unread first, then newest."""
        qs = super().get_queryset(request)
        return qs.order_by('-is_read', '-created_at')
    
    def has_add_permission(self, request):
        """Prevent manual message creation via admin."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent accidental message deletion."""
        return request.user.is_superuser
