from django.contrib import admin
from models import InstructorKey

# Register your models here.
class InstructorKeyAdmin(admin.ModelAdmin):
	list_display = ['key', 'instructor_list', 'key_used']
	exclude = ('key_used', 'instructors')

	def instructor_list(self, obj):
		return "\n".join([i.username for i in obj.instructors.all()])

admin.site.register(InstructorKey, InstructorKeyAdmin)