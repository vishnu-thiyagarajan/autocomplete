from django.contrib import admin
# Register your models here.
from .models import AutoComplete
from import_export.admin import ImportExportModelAdmin
from .forms import AutoCompleteForm


class AutoSearchForm(ImportExportModelAdmin):
    list_display = ["__str__"]
    form = AutoCompleteForm


admin.site.register(AutoComplete, AutoSearchForm)
