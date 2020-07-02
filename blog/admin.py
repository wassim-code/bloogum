from django.contrib import admin

from .models import *

admin.site.site_header = 'Bloogum Administration'

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Email)