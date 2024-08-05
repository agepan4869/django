from django.contrib import admin
from .models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'subdirectory', 'uploaded_at')

admin.site.register(UploadedFile, UploadedFileAdmin)
