from django.contrib import admin
from models import InstructorKey

# Register your models here.
class InstructorKeyAdmin(admin.ModelAdmin):
	list_display = ['key',]

admin.site.register(InstructorKey, InstructorKeyAdmin)