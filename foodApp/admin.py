from django.contrib import admin
from .models import spec,foodUpload,adminApproval

# Register your models here.
admin.site.register(spec)
admin.site.register(foodUpload)
class approve(admin.ModelAdmin):
    list_display=('foodUploadChef','approval')
    list_editable = ('approval',)
admin.site.register(adminApproval,approve)

