from django.contrib import admin
from .models import company, profile, project

#admin.site.register(Imageupload)
#admin.site.register(Keyword)

class profileInline(admin.TabularInline):
    model = profile

@admin.register(company)
class companyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'address', 'type', 'description')
    #ordering = ['-date_of_upload']
    inlines = [profileInline]

@admin.register(profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company', 'department', 'title', 'email', 'phone', 'description')

@admin.register(project)
class profileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company', 'product', 'member', 'status', 'date_start', 'date_update', 'detail', 'technical', 'sales')
