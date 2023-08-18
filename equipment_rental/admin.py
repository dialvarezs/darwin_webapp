from datetime import datetime

from django import forms
from django.contrib import admin

from . import validators
from .models import (
    Client,
    Equipment,
    IDType,
    Lease,
    LeaseEquipments,
    StockModification,
    Surcharge,
)


class EquipmentAdmin(admin.ModelAdmin):
    exclude = ["stock", "stock_leased"]
    list_display = ["name", "lease_price", "stock", "stock_leased"]


class StockModificationAdmin(admin.ModelAdmin):
    exclude = ["record"]
    list_display = ["equipment", "quantity", "description", "record"]
    list_filter = ["equipment"]

    def save_model(self, request, obj, form, change):
        obj.record = datetime.now()
        obj.equipment.stock += obj.quantity
        obj.equipment.save()
        obj.save()


class IDTypeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


class MyClientForm(forms.ModelForm):
    def clean_id_string(self):
        print(self.cleaned_data)
        if self.cleaned_data["id_type"].name == "CI":
            if not validators.ci(self.cleaned_data["id_string"].upper()):
                raise forms.ValidationError("RUT no válido")
        return self.cleaned_data["id_string"].upper().replace(".", "")


class ClientAdmin(admin.ModelAdmin):
    form = MyClientForm
    list_display = [
        "id_string",
        "id_type",
        "nationality",
        "names",
        "surnames",
        "date_of_birth",
    ]


class LeaseEquipmentsInline(admin.TabularInline):
    model = LeaseEquipments
    extra = 1


class LeaseAdmin(admin.ModelAdmin):
    list_display = [
        "__str_equipments__",
        "client",
        "lease_record",
        "return_date",
        "total_cost",
        "total_surcharge",
    ]
    inlines = [LeaseEquipmentsInline]
    exclude = ["return_record", "total_cost"]

    # readonly_fields = ['client', 'lease_record', 'return_record', 'return_date', 'total_cost', 'equipments']

    # def get_readonly_fields(self, request, obj=None):
    # 	return list(self.readonly_fields) + [field.name for field in obj._meta.fields]
    #
    # def has_add_permission(self, request, obj=None):
    # 	return False
    #
    # def has_delete_permission(self, request, obj=None):
    # 	return False


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(StockModification, StockModificationAdmin)
admin.site.register(IDType, IDTypeAdmin)
admin.site.register(Client, ClientAdmin)
# admin.site.register(Lease, LeaseAdmin)
# admin.site.register(LeaseEquipments)
# admin.site.register(Surcharge)
