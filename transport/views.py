from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from io import BytesIO
from datetime import datetime
import json

from .models import Travel, Group, Bus, BusCompany, Driver, Itinerary, Company
from .pdf_print import DocumentBuilder


@login_required
def travel_list(request):
	travels = Travel.objects.all().select_related('group', 'bus', 'bus__company', 'itinerary', 'itinerary__stretch', 'driver')
	groups = Group.objects.filter(is_enabled=True)
	busses = Bus.objects.filter(is_available=True).select_related('company')
	companies = Company.objects.filter(is_available=True)
	buscompanies = BusCompany.objects.all()
	drivers = Driver.objects.filter(is_available=True)
	itineraries = Itinerary.objects.filter(is_enabled=True).select_related('stretch')
	current_group = None
	filters = []

	if 'group' in request.GET and request.GET['group'] != '0':
		travels = travels.filter(group=request.GET['group'])
		current_group = Group.objects.get(pk=request.GET['group'])
		filters.append("Grupo: " + current_group.__str__())

	if 'company' in request.GET and request.GET['company'] != '0':
		travels = travels.filter(group__company=request.GET['company'])
		filters.append("Empresa (Turismo): " + Company.objects.get(pk=request.GET['company']).__str__())

	if 'buscompany' in request.GET and request.GET['buscompany'] != '0':
		travels = travels.filter(bus__company=request.GET['buscompany'])
		filters.append("Empresa (Buses): " + BusCompany.objects.get(pk=request.GET['buscompany']).__str__())

	if 'driver' in request.GET and request.GET['driver'] != '0':
		travels = travels.filter(driver=request.GET['driver'])
		filters.append("Chofer: " + Driver.objects.get(pk=request.GET['driver']).__str__())

	date_from = (request.GET['date_from'] if 'date_from' in request.GET else None)
	date_to = (request.GET['date_to'] if 'date_to' in request.GET else None)
	if date_from and date_to:
		travels = travels.filter(date__range=[date_from, date_to])
		filters.append("Fechas: {} - {}".format(datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%d/%y'),
			datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%d/%y')))
	elif date_from:
		travels = travels.exclude(date__lt=date_from)
		filters.append("Fechas: {} - // ".format(datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%d/%y')))
	elif date_to:
		travels = travels.exclude(date__gt=date_to)
		filters.append("Fechas: // - {} ".format(datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%d/%y')))
	else:
		travels = travels.exclude(date__lt=datetime.today())

	travels = __pagination(travels, 20, request.GET.get('page'))

	context = {'logo': 'resources/img/logo-darwin-mini.png', 'travels': travels, 'groups': groups, 'busses': busses, 'buscompanies': buscompanies,
		'drivers': drivers, 'itineraries': itineraries, 'companies': companies, 'current_group': current_group, 'filters': filters}
	return render(request, 'transport/list.html', context)


@login_required
def travel_save(request, travel_id=None):
	try:
		group = Group.objects.get(pk=request.POST['group'])
		if request.POST['bus'] != '0':
			bus = Bus.objects.get(pk=request.POST['bus'])
		else:
			bus = None
		if request.POST['driver'] != '0':
			driver = Driver.objects.get(pk=request.POST['driver'])
		else:
			driver = None
		itinerary = Itinerary.objects.get(pk=request.POST['itinerary'])
		date_field = request.POST['date']
		time_field = request.POST['time']
		notes = request.POST['notes']
	except KeyError as e:
		return __bad_request(str(e))
	else:
		if travel_id:
			t = get_object_or_404(Travel, pk=travel_id)
		else:
			t = Travel()
		t.group = group
		t.bus = bus
		t.driver = driver
		t.itinerary = itinerary
		t.date = date_field
		t.time = time_field if time_field != '' else None
		t.notes = notes

	try:
		t.save()
	except Exception as e:
		return __bad_request(str(e))
	else:
		return HttpResponseRedirect(reverse('transport:index'))


@login_required
def group_save(request, group_id):
	g = get_object_or_404(Group, pk=group_id)

	try:
		id_string = request.POST['id_string']
		external_id = request.POST['external_id']
		company = Company.objects.get(pk=request.POST['company'])
		charge = request.POST['charge']
		debt = request.POST['debt'] if request.POST['debt'] != '' else '0'
		paid = 'paid' in request.POST
	except KeyError as e:
		return __bad_request(str(e))
	else:
		g.id_string = id_string
		g.external_id = external_id
		g.company = company
		g.charge = charge
		g.debt = debt
		g.is_paid = paid

	try:
		g.save()
	except Exception as e:
		return __bad_request(str(e))
	else:
		return HttpResponseRedirect(reverse('transport:index'))


@login_required
def travel_pdf(request):
	travels = Travel.objects.all()
	info_raw = ()

	if 'group' in request.GET and request.GET['group'] != '0':
		travels = travels.filter(group=request.GET['group'])
		info_raw += ("Grupo: " + Group.objects.get(pk=request.GET['group']).__str__(),)
	else:
		info_raw += ("Grupo: TODOS",)

	if 'company' in request.GET and request.GET['company'] != '0':
		travels = travels.filter(group__company=request.GET['company'])
		info_raw += ("Empresa (Turismo):" + Company.objects.get(pk=request.GET['company']).short_name,)
	else:
		info_raw += ("Empresa (Turismo): TODAS",)

	if 'buscompany' in request.GET and request.GET['buscompany'] != '0':
		travels = travels.filter(bus__company=request.GET['buscompany'])
		info_raw += ("Empresa (Transportes):" + BusCompany.objects.get(pk=request.GET['buscompany']).__str__(),)
	else:
		info_raw += ("Empresa (Transportes): TODAS",)

	if 'driver' in request.GET and request.GET['driver'] != '0':
		travels = travels.filter(driver=request.GET['driver'])
		info_raw += ("Conductor:" + Driver.objects.get(pk=request.GET['driver']).__str__(),)
	else:
		info_raw += ("Conductor: TODOS",)

	date_from = (request.GET['date_from'] if 'date_from' in request.GET else None)
	date_to = (request.GET['date_to'] if 'date_to' in request.GET else None)
	if date_from and date_to:
		travels = travels.filter(date__range=[date_from, date_to])
		info_raw += ("Fechas: {} - {}".format(datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%d/%y'),
			datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%d/%y')),)
	elif date_from:
		travels = travels.exclude(date__lt=date_from)
		info_raw += ("Fechas: {} - // ".format(datetime.strptime(date_from, '%Y-%m-%d').strftime('%d/%d/%y')),)
	elif date_to:
		travels = travels.exclude(date__gt=date_to)
		info_raw += ("Fechas: // - {} ".format(datetime.strptime(date_to, '%Y-%m-%d').strftime('%d/%d/%y')),)
	else:
		info_raw += ("Fechas: TODAS",)

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=' + "travel_list.pdf"

	buffer = BytesIO()
	pdf = DocumentBuilder(buffer).travel_list([info_raw], travels)

	response.write(pdf)

	return response


def __pagination(objects, number, page):
	paginator = Paginator(objects, number)
	try:
		return paginator.page(page)
	except PageNotAnInteger:
		return paginator.page(1)
	except EmptyPage:
		return paginator.page(paginator.num_pages)


def __bad_request(message):
	response = HttpResponse(json.dumps({'message': message}),
		content_type='application/json')
	response.status_code = 400
	return response
