from django.contrib import admin

from django import forms
from django_admin_bootstrapped.admin.models import SortableInline

from .models import Bus, Driver, Destination, Stretch, StretchDestinations, Itinerary, Company, Group, Travel, IDType, Passenger
from . import validators
from . import utils

class MyBusAdminForm(forms.ModelForm):
	def clean_plate(self):
		if self.cleaned_data['plate']:
			if not validators.plate(self.cleaned_data['plate'].upper()):
				raise forms.ValidationError("Patente no válida")
		return self.cleaned_data['plate'].upper()
	def clean_year(self):
		if self.cleaned_data['year']:
			if not validators.year(self.cleaned_data['year']):
				raise forms.ValidationError("No es un año válido")
		return self.cleaned_data['year']

class BusAdmin(admin.ModelAdmin):
	form = MyBusAdminForm
	def formfield_for_dbfield(self, db_field, **kwargs):
		formfield = super(BusAdmin, self).formfield_for_dbfield(db_field, **kwargs)
		if db_field.name == 'notes':
			formfield.widget = forms.Textarea(attrs={'rows': 5})
		return formfield
	list_display = ('__str__', 'plate', 'model', 'capacity', 'is_available', 'company')

class MyDriverAdminForm(forms.ModelForm):
	def clean_id_string(self):
		if not validators.ci(self.cleaned_data['id_string'].upper()):
			raise forms.ValidationError("RUT no válido")
		return self.cleaned_data['id_string'].upper().replace('.','')

class DriverAdmin(admin.ModelAdmin):
	form = MyDriverAdminForm
	list_display = ('id_string', '__str_name__')

class DestinationAdmin(admin.ModelAdmin):
	def get_model_perms(self, request):
		return {}

class StretchDestinationsInline(admin.TabularInline):
	model = StretchDestinations
	ordering = ('position',)
	extra = 1

class StretchAdmin(admin.ModelAdmin):
	inlines = [StretchDestinationsInline]
	list_display = ('description', '__str_destinations__')
	list_filter = ('destinations',)
	search_fields = ('description',)

class ItineraryAdmin(admin.ModelAdmin):
	list_filter = ('stretch',)
	search_fields = ('stretch__description',)

class MyCompanyAdminForm(forms.ModelForm):
	def clean_id_string(self):
		if self.cleaned_data['id_string']:
			if not validators.ci(self.cleaned_data['id_string'].upper()):
				raise forms.ValidationError("RUT no válido")
		return self.cleaned_data['id_string'].upper().replace('.','')

class CompanyAdmin(admin.ModelAdmin):
	form = MyCompanyAdminForm
	list_display = ('short_name', 'id_string', 'name', 'email')

class GroupAdmin(admin.ModelAdmin):
	filter_vertical = ['passengers']
	list_display = ('id_string', 'external_id', 'company', 'charge', 'debt')
	list_filter = ('company',)

	def get_form(self, request, obj=None, **kwargs):
		form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
		form.base_fields['id_string'].initial = utils.group_autoid()
		return form

class TravelAdmin(admin.ModelAdmin):
	def formfield_for_dbfield(self, db_field, **kwargs):
		formfield = super(TravelAdmin, self).formfield_for_dbfield(db_field, **kwargs)
		if db_field.name == 'notes':
			formfield.widget = forms.Textarea(attrs={'rows': 5})
		return formfield
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'bus':
			kwargs['queryset'] = Bus.objects.filter(is_available=True)
		return super(TravelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	list_display = ('__str__', 'group', 'bus', 'driver', 'itinerary', 'date', 'time')
	list_filter = ('group', 'driver', 'date')

class PassengerAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'names', 'surnames')

class IDTypeAdmin(admin.ModelAdmin):
	def get_model_perms(self, request):
		return {}


admin.site.register(Bus, BusAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Stretch, StretchAdmin)
admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(IDType, IDTypeAdmin)