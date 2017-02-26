from django.db import models


class Equipment(models.Model):
	name = models.CharField(max_length=16, verbose_name='nombre')
	description = models.CharField(max_length=64, verbose_name='descripción')
	branch = models.CharField(max_length=32, verbose_name='marca')
	model = models.CharField(max_length=32, verbose_name='modelo')
	lease_price = models.PositiveIntegerField(verbose_name='precio de arriendo')
	stock = models.PositiveIntegerField(default=0, verbose_name='cantidad total')
	stock_leased = models.PositiveIntegerField(default=0, verbose_name='cantidad arrendada')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'equipamiento'
		verbose_name_plural = 'equipamientos'


class StockModification(models.Model):
	equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='equipamiento')
	quantity = models.IntegerField(verbose_name='cantidad')
	description = models.CharField(max_length=255, verbose_name='descripción')
	record = models.DateTimeField(verbose_name='registro')

	def __str__(self):
		return "{} {}{}: {}".format(self.equipment, '+' if self.quantity < 0 else '', self.quantity, self.description)

	class Meta:
		verbose_name = 'modificación de inventario'
		verbose_name_plural = 'modificaciones de inventario'


class IDType(models.Model):
	name = models.CharField(max_length=16, verbose_name='nombre')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'tipo de identificación'
		verbose_name_plural = 'tipos de identificación'


class Client(models.Model):
	SEX_CHOICE = (('m', 'masculino'), ('f', 'femenino'))
	id_type = models.ForeignKey(IDType, on_delete=models.PROTECT, verbose_name='tipo de identificación')
	id_string = models.CharField(max_length=16, verbose_name='identificación')
	names = models.CharField(max_length=32, verbose_name='nombres')
	surnames = models.CharField(max_length=32, verbose_name='apellidos')
	sex = models.CharField(max_length=1, choices=SEX_CHOICE, verbose_name='sexo')
	date_of_birth = models.DateField(verbose_name='fecha de nacimiento')
	nationality = models.CharField(max_length=16, verbose_name='nacionalidad')

	def __str__(self):
		return "{} {}: {}, {}".format(self.id_type, self.id_string, self.surnames, self.names)

	class Meta:
		verbose_name = 'cliente'
		verbose_name_plural = 'clientes'


class Lease(models.Model):
	client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='cliente')
	lease_record = models.DateTimeField(verbose_name='registro de arriendo')
	return_record = models.DateTimeField(blank=True, null=True, verbose_name='registro de entrega')
	return_date = models.DateField(verbose_name='fecha de devolución')
	total_cost = models.PositiveIntegerField(verbose_name='costo')
	total_surcharge = models.PositiveIntegerField(verbose_name='recargo')
	payment = models.PositiveIntegerField(verbose_name='pago')
	returned = models.BooleanField(default=False, verbose_name='devuelto')
	notes = models.CharField(max_length=256, blank=True, null=True, verbose_name='notas')
	equipments = models.ManyToManyField(Equipment, through='LeaseEquipments', verbose_name='equipamientos')

	def __str__(self):
		return self.__str_equipments__()

	def __str_equipments__(self):
		return str(", ".join("{} ({})".format(e.equipment, e.quantity) for e in self.leaseequipments_set.all()))
	__str_equipments__.short_description = 'equipamientos'

	def equipments_str(self):
		return self.__str_equipments__()

	class Meta:
		verbose_name = 'arriendo'
		verbose_name_plural = 'arriendos'


class LeaseEquipments(models.Model):
	lease = models.ForeignKey(Lease, on_delete=models.CASCADE, verbose_name='arriendo')
	equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='equipamiento')
	quantity = models.PositiveIntegerField(verbose_name='cantidad')
	unit_price = models.PositiveIntegerField(verbose_name='precio unitario')

	def __str__(self):
		return "{}: {} ({})".format(self.lease.pk, self.equipment, self.quantity)

	class Meta:
		verbose_name = 'equipamiento arrendado'
		verbose_name_plural = 'equipamientos arrendados'


class Surcharge(models.Model):
	lease = models.ForeignKey(Lease, on_delete=models.CASCADE, verbose_name='arriendo')
	lease_equipment = models.ForeignKey(LeaseEquipments, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='equipo arrendado')
	cost = models.PositiveIntegerField(verbose_name='costo')
	note = models.CharField(max_length=128, blank=True, verbose_name='nota')

	def __str__(self):
		return str(self.pk)

	class Meta:
		verbose_name = 'recargo'
		verbose_name_plural = 'recargos'
