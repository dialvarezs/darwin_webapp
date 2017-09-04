from django.db import models


class BusCompany(models.Model):
	name = models.CharField(max_length=32, verbose_name='nombre')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'empresa de buses'
		verbose_name_plural = 'empresas de buses'
		ordering = ['name']


class Bus(models.Model):
	company = models.ForeignKey(BusCompany, on_delete=models.PROTECT, verbose_name='empresa')
	plate = models.CharField(max_length=6, blank=True, verbose_name='patente')
	brand = models.CharField(max_length=32, verbose_name='marca')
	model = models.CharField(max_length=32, verbose_name='modelo')
	year = models.IntegerField(blank=True, null=True, verbose_name='año')
	capacity = models.IntegerField(verbose_name='capacidad')
	is_available = models.BooleanField(default=True, verbose_name='disponible')
	notes = models.CharField(max_length=128, blank=True, verbose_name='notas')

	def __str__(self):
		return "{} ({} [{}])".format(self.plate, self.model, self.capacity)

	class Meta:
		verbose_name = 'bus'
		verbose_name_plural = 'buses'
		ordering = ['company', 'plate']


class Driver(models.Model):
	id_string = models.CharField(max_length=16, verbose_name='RUT')
	names = models.CharField(max_length=32, verbose_name='nombres')
	surnames = models.CharField(max_length=32, verbose_name='apellidos')
	is_available = models.BooleanField(default=True, verbose_name='disponible')

	def __str__(self):
		return self.names.split(' ')[0] + ' ' + self.surnames.split(' ')[0]

	def __str_name__(self):
		return self.names + ' ' + self.surnames
	__str_name__.short_description = 'nombre'

	class Meta:
		verbose_name = 'chofer'
		verbose_name_plural = 'choferes'
		ordering = ['surnames', 'names']


class Destination(models.Model):
	name = models.CharField(max_length=32, verbose_name='nombre')
	short_name = models.CharField(max_length=16, verbose_name='nombre corto')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'destino'
		verbose_name_plural = 'destinos'
		ordering = ['name']


class Stretch(models.Model):
	description = models.CharField(max_length=64, verbose_name='descripción')
	destinations = models.ManyToManyField(Destination, through='StretchDestinations')
	is_enabled = models.BooleanField(default=True, verbose_name='habilitado')

	def __str__(self):
		return self.description

	def __str_destinations__(self):
		return ' - '.join([x.short_name for x in self.destinations.all().order_by('stretchdestinations__position')])
	__str_destinations__.short_description = 'destinos'

	class Meta:
		verbose_name = 'tramo'
		verbose_name_plural = 'tramos'
		ordering = ['description']


class StretchDestinations(models.Model):
	stretch = models.ForeignKey(Stretch, on_delete=models.CASCADE, verbose_name='tramo')
	destination = models.ForeignKey(Destination, on_delete=models.CASCADE, verbose_name='destino')
	position = models.PositiveSmallIntegerField(verbose_name='posición')

	def __str__(self):
		return self.destination.name

	class Meta:
		verbose_name = 'destino'
		verbose_name_plural = 'destinos'
		ordering = ['position']


class Company(models.Model):
	name = models.CharField(max_length=64, verbose_name='nombre')
	short_name = models.CharField(max_length=8, verbose_name='nombre corto')
	id_string = models.CharField(blank=True, max_length=16, verbose_name='RUT')
	line_of_business = models.CharField(max_length=64, verbose_name='giro')
	address = models.CharField(max_length=64, verbose_name='dirección')
	email = models.EmailField(verbose_name='e-mail')
	is_available = models.BooleanField(default=True, verbose_name='disponible')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'empresa'
		verbose_name_plural = 'empresas'
		ordering = ['name']


class IDType(models.Model):
	name = models.CharField(max_length=16, verbose_name='nombre')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'tipo de identificación'
		verbose_name_plural = 'tipos de identificación'
		ordering = ['name']


class Passenger(models.Model):
	SEX_CHOICE = (('m', 'masculino'), ('f', 'femenino'),)
	id_string = models.CharField(max_length=16, verbose_name='identificación')
	id_type = models.ForeignKey(IDType, on_delete=models.PROTECT, verbose_name='tipo de identificación')
	names = models.CharField(max_length=32, verbose_name='nombres')
	surnames = models.CharField(max_length=32, verbose_name='apellidos')
	date_of_birth = models.DateField(verbose_name='fecha de nacimiento')
	sex = models.CharField(max_length=1, choices=SEX_CHOICE, verbose_name='sexo')

	def __str__(self):
		return "{} {}: {}, {}".format(self.id_type, self.id_string, self.surnames, self.names)

	class Meta:
		verbose_name = 'pasajero'
		verbose_name_plural = 'pasajeros'
		ordering = ['id_type', 'id_string']


class Group(models.Model):
	id_string = models.CharField(max_length=16, verbose_name='ID')
	external_id = models.CharField(max_length=16, verbose_name='ID Externo')
	company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='empresa')
	debt = models.PositiveIntegerField(verbose_name='deuda')
	charge = models.PositiveIntegerField(verbose_name='costo')
	is_enabled = models.BooleanField(default=True, verbose_name='habilitado')
	is_paid = models.BooleanField(default=False, verbose_name='pagado')
	passengers = models.ManyToManyField(Passenger, verbose_name='pasajeros', blank=True)

	def __str__(self):
		return "{} ({})".format(self.id_string, self.external_id)

	class Meta:
		verbose_name = 'grupo'
		verbose_name_plural = 'grupos'
		ordering = ['external_id']


class Travel(models.Model):
	group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='grupo')
	bus = models.ForeignKey(Bus, on_delete=models.PROTECT, blank=True, null=True, verbose_name='bus')
	driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='chofer')
	additional_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, related_name='%(app_label)s_aditional_%(class)s_related',
		blank=True, null=True, verbose_name='chofer adicional')
	stretch = models.ForeignKey(Stretch, on_delete=models.PROTECT, blank=True, null=True, verbose_name='tramo')
	app_people = models.IntegerField(default=0, verbose_name='PAX')
	guides = models.IntegerField(default=0, verbose_name='guías')
	date = models.DateField(verbose_name='fecha')
	time = models.TimeField(blank=True, null=True, verbose_name='hora')
	notes = models.CharField(max_length=128, blank=True, verbose_name='notas')

	def __str__(self):
		return str(self.pk).zfill(4)

	class Meta:
		verbose_name = 'viaje'
		verbose_name_plural = 'viajes'
		ordering = ['date', 'time']
