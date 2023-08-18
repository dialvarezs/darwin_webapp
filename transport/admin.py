from django import forms
from django.contrib import admin

from . import utils, validators
from .models import (
    Bus,
    BusCompany,
    Company,
    Destination,
    Driver,
    Group,
    IDType,
    Passenger,
    Stretch,
    StretchDestinations,
    Travel,
)


class BusCompanyAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class MyBusAdminForm(forms.ModelForm):
    def clean_plate(self):
        if self.cleaned_data["plate"]:
            if not validators.plate(self.cleaned_data["plate"].upper()):
                raise forms.ValidationError("Patente no válida")
        return self.cleaned_data["plate"].upper()

    def clean_year(self):
        if self.cleaned_data["year"]:
            if not validators.year(self.cleaned_data["year"]):
                raise forms.ValidationError("No es un año válido")
        return self.cleaned_data["year"]


class BusAdmin(admin.ModelAdmin):
    form = MyBusAdminForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(BusAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "notes":
            formfield.widget = forms.Textarea(attrs={"rows": 5})
        return formfield

    list_display = ["__str__", "company", "plate", "model", "capacity", "is_available"]


class MyDriverAdminForm(forms.ModelForm):
    def clean_id_string(self):
        if not validators.ci(self.cleaned_data["id_string"].upper()):
            raise forms.ValidationError("RUT no válido")
        return self.cleaned_data["id_string"].upper().replace(".", "")


class DriverAdmin(admin.ModelAdmin):
    form = MyDriverAdminForm
    list_display = ["id_string", "__str_name__", "is_available"]
    list_filter = ["is_available"]
    actions = ["make_unavailable"]

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    make_unavailable.short_description = (
        "Marcar choferes seleccionados como no disponibles"
    )


class DestinationAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class StretchDestinationsInline(admin.TabularInline):
    model = StretchDestinations
    ordering = ["position"]
    extra = 1


class StretchAdmin(admin.ModelAdmin):
    inlines = [StretchDestinationsInline]
    list_display = ["description", "__str_destinations__", "is_enabled"]
    list_filter = ["destinations", "is_enabled"]
    search_fields = ["description"]
    actions = ["make_disabled"]

    def make_disabled(self, request, queryset):
        queryset.update(is_enabled=False)

    make_disabled.short_description = "Deshabilitar tramos seleccionados"


class MyCompanyAdminForm(forms.ModelForm):
    def clean_id_string(self):
        if self.cleaned_data["id_string"]:
            if not validators.ci(self.cleaned_data["id_string"].upper()):
                raise forms.ValidationError("RUT no válido")
        return self.cleaned_data["id_string"].upper().replace(".", "")


class CompanyAdmin(admin.ModelAdmin):
    form = MyCompanyAdminForm
    list_display = ["short_name", "id_string", "name", "email", "is_available"]
    list_filter = ["is_available"]
    actions = ["make_unavailable"]

    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)

    make_unavailable.short_description = (
        "Marcar empresas seleccionadas como no disponibles"
    )


class GroupAdmin(admin.ModelAdmin):
    filter_vertical = ["passengers"]
    list_display = [
        "id_string",
        "external_id",
        "company",
        "charge",
        "debt",
        "is_enabled",
    ]
    list_filter = ["company", "is_enabled"]
    actions = ["make_disabled"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["id_string"].initial = utils.group_autoid()
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] = Company.objects.filter(is_available=True)
        return super(GroupAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def make_disabled(self, request, queryset):
        queryset.update(is_enabled=False)

    make_disabled.short_description = "Deshabilitar grupos seleccionados"


class TravelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "group", "bus", "driver", "stretch", "date", "time"]
    list_filter = ["group", "driver", "stretch", "date"]

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(TravelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "notes":
            formfield.widget = forms.Textarea(attrs={"rows": 5})
        return formfield

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "bus":
            kwargs["queryset"] = Bus.objects.filter(is_available=True)
        if db_field.name == "driver":
            kwargs["queryset"] = Driver.objects.filter(is_available=True)
        if db_field.name == "stretch":
            kwargs["queryset"] = Stretch.objects.filter(is_enabled=True)
        if db_field.name == "group":
            kwargs["queryset"] = Group.objects.filter(is_enabled=True)
        return super(TravelAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class PassengerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "names", "surnames"]


class IDTypeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


admin.site.register(BusCompany, BusCompanyAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Stretch, StretchAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(IDType, IDTypeAdmin)
