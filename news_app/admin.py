from django.contrib import admin

from .models import News,Category,Contacts
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id','category','title' ,'publish_time','status']
    list_filter = ['publish_time','create_time']
    prepopulated_fields = {"slug":('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title','create_time']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_filter = ['id']
    search_fields = ['publsih_time']

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['id','email']