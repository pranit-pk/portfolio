from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    """Portfolio project model with slug-based URLs, tech stack, and featured status."""
    
    title = models.CharField(
        max_length=200,
        help_text="Project title displayed in portfolio"
    )
    slug = models.SlugField(
        unique=True,
        help_text="URL-friendly identifier (auto-generated from title)"
    )
    short_description = models.CharField(
        max_length=300,
        help_text="Brief one-liner or summary of the project"
    )
    description = models.TextField(
        help_text="Detailed project description with context, challenges, and outcomes"
    )
    tech_stack = models.TextField(
        help_text="Comma-separated list of technologies (e.g., Django, React, PostgreSQL)"
    )
    thumbnail = models.ImageField(
        upload_to='projects/',
        null=True,
        blank=True,
        help_text="Project thumbnail or preview image"
    )
    github_url = models.URLField(
        null=True,
        blank=True,
        help_text="Link to GitHub repository"
    )
    live_url = models.URLField(
        null=True,
        blank=True,
        help_text="Link to live project or demo"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Display this project prominently on homepage"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manual ordering position (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured', 'order']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Store contact form submissions from website visitors."""
    
    name = models.CharField(
        max_length=200,
        help_text="Sender's name"
    )
    email = models.EmailField(
        help_text="Sender's email address"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Sender's phone number (optional)"
    )
    subject = models.CharField(
        max_length=300,
        help_text="Message subject or topic"
    )
    message = models.TextField(
        help_text="Message content"
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Mark whether this message has been read"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        status = "[NEW]" if not self.is_read else "[READ]"
        return f"{status} {self.name} ({self.email}) - {self.subject}"
