from django.contrib import admin

from .models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class AreaCodeInline(admin.TabularInline):
    model = AreaCode
    extra = 0


class CountryAdmin(admin.ModelAdmin):
    inlines = [AreaCodeInline]

    list_display = ('name', )
    search_fields = ['name', ]

class NumGeoMxResource(resources.ModelResource):
    class Meta:
        model = NumGeoMx

class  NumGeoMxAdmin(ImportExportModelAdmin):
    resource_class = NumGeoMxResource

admin.site.register(Country, CountryAdmin)
admin.site.register(NumGeoMx, NumGeoMxAdmin)

