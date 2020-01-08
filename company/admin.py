from django.contrib import admin
from .models import company, profile, project, staff, report

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
class projectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'company', 'product', 'member', 'status', 'date_start', 'date_update', 'detail', 'technical', 'sales')

@admin.register(staff)
class staffAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'department', 'boss0', 'boss1', 'boss2')

@admin.register(report)
class reportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'staff_id', 'date_app', 'work', 'date_start', 'date_end', 'b0', 'date_b0', 'b1', 'date_b1', 'b2', 'date_b2', 'status', 'comment')
