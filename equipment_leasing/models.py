from django.db import models

SEX_CHOICE = (
	('m', 'masculino'),
	('f', 'femenino'),
)

class Equipment(models.Model):
	name = models.CharField(max_length=16, verbose_name='nombre')
	description = models.CharField(max_length=64, verbose_name='descipción')
	price = models.PositiveIntegerField(verbose_name='precio')
	quantity = models.PositiveIntegerField(verbose_name='cantidad')
	stock = models.PositiveIntegerField(verbose_name='disponibles')

class IDType(models.Model):
	name = models.CharField(max_length=16, verbose_name='nombre')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'tipo de identificación'
		verbose_name_plural = 'tipos de identificación'

class Client(models.Model):
	id_string = models.CharField(max_length=16, verbose_name='identificación')
	id_type = models.ForeignKey(IDType, verbose_name='tipo de identificación')
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
	client = models.ForeignKey(Client, verbose_name='cliente')