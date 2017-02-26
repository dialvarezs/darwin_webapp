from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F

from .models import Client, Equipment, Lease, LeaseEquipments, Surcharge, StockModification


@login_required
def lease_list(request):
	clients = Client.objects.all()
	equipments = Equipment.objects.annotate(available=F('stock')-F('stock_leased')).filter(available__gt=0)
	leases = Lease.objects.all().order_by('return_date')

	leases = __pagination(leases, 20, request.GET.get('page'))

	context = {'logo': 'resources/img/logo-camaleon-mini.png', 'leases': leases, 'clients': clients, 'equipments': equipments}
	return render(request, 'equipment_rental/list.html', context)


@login_required
def lease_save(request, lease_id=None):
	if lease_id:  # return
		try:
			surcharge = request.POST['surcharge']
			new_payment = request.POST['new_payment'] if request.POST['new_payment'] != '' else 0
			notes = request.POST['notes']
			if 'surcharge_equipments[]' in request.POST:
				has_surcharges = True
				surch_equipments = request.POST.getlist('surcharge_equipments[]')
				surch_discounts = request.POST.getlist('discount_numbers[]')
				surch_descriptions = request.POST.getlist('surcharge_descriptions[]')
				surch_values = request.POST.getlist('surcharge_values[]')
			else:
				has_surcharges = False
			print(request.POST)
		except KeyError:
			pass
		else:
			with transaction.atomic():
				l = Lease.objects.get(pk=lease_id)
				l.total_surcharge = surcharge
				l.payment += int(new_payment)
				l.notes = notes
				l.return_record = datetime.now()
				l.returned = True
				l.save()

				for le in l.leaseequipments_set.all():
					le.equipment.stock_leased -= le.quantity
					le.equipment.save()

				if has_surcharges:
					for epk, d, t, v in zip(surch_equipments, surch_discounts, surch_descriptions, surch_values):
						v = int(v) if v != '' else 0
						le = LeaseEquipments.objects.get(pk=epk)
						s = Surcharge(lease=l, lease_equipment=le, cost=v, note=t)
						s.save()
						if d != '' and d != '0':
							desc = "Préstamo {}: {}".format(l.pk, t)
							sm = StockModification(equipment=le.equipment, quantity=-1*int(d), description=desc, record=datetime.now())
							sm.save()

	else:  # new
		try:
			client = Client.objects.get(pk=request.POST['client'])
			return_date = request.POST['return_date']
			cost = request.POST['cost']
			payment = request.POST['payment']
			notes = request.POST['notes']
			equipments = [{'e': Equipment.objects.get(pk=e), 'n': n} for e, n in
				zip(request.POST.getlist('equipments_select[]'), request.POST.getlist('equipments_quantity[]'))]
		except KeyError:
			pass
		else:
			with transaction.atomic():
				l = Lease(client=client, return_date=return_date, total_cost=cost, total_surcharge=0, payment=payment, notes=notes, lease_record=datetime.now())
				l.save()
				for eq in equipments:
					le = LeaseEquipments(lease=l, equipment=eq['e'], quantity=eq['n'], unit_price=eq['e'].lease_price)
					le.save()
					le.equipment.stock_leased += int(le.quantity)
					le.equipment.save()

	return HttpResponseRedirect(reverse('equipment_rental:index'))


def __pagination(objects, number, page):
	paginator = Paginator(objects, number)
	try:
		return paginator.page(page)
	except PageNotAnInteger:
		return paginator.page(1)
	except EmptyPage:
		return paginator.page(paginator.num_pages)


# TODO
# Desde la lista:
# - Un botón para "imprimir" el préstamo (en pdf)
# - Un botón para devolver el préstamo del préstamo (modal)
#   - debe hacerse un recargo automático si la fecha es posterior a de retorno registrada
#
# La lista debe ofrecer un filtro por fecha, y podría mostrar coloraciones distintas de acuerdo a como está respecto a la fecha de entrega
#
# ** definir bien el resumen de ingresos diario
#
#
# Notas:
# - Después de que hora ya no se cuenta el día actual? O siempre se cuenta?
# - Cuando hay atraso se cobra un recargo adicional? fijo o %?
