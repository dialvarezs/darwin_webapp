from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from io import BytesIO
from datetime import datetime

from .models import Travel, Group, Bus, BusCompany, Driver, Itinerary, Company
from .pdf_print import DocumentBuilder

@login_required
def index(request):
	travels_all = Travel.objects.exclude(date__lt=datetime.today())
	groups = Group.objects.all()
	busses = Bus.objects.filter(is_available=True)
	companies = Company.objects.all()
	buscompanies = BusCompany.objects.all()
	drivers = Driver.objects.all()
	itineraries = Itinerary.objects.all()

	paginator = Paginator(travels_all, 25)
	page = request.GET.get('page')

	try:
		travels = paginator.page(page)
	except PageNotAnInteger:
		travels = paginator.page(1)
	except EmptyPage:
		travels = paginator.page(paginator.num_pages)    

	context = {'nbar':'transport', 'logo':'img/logo-darwin-mini.png', 'travels':travels, 'groups':groups, 'busses':busses, 'companies':companies, 'buscompanies':buscompanies, 'drivers':drivers, 'itineraries':itineraries}
	return render(request, 'transport/index.html', context)

@login_required
def filter(request):
	travels_all = Travel.objects.all()
	groups = Group.objects.all()
	busses = Bus.objects.filter(is_available=True)
	buscompanies = BusCompany.objects.all()
	drivers = Driver.objects.all()
	itineraries = Itinerary.objects.all()
	companies = Company.objects.all()
	current_group = None

	if 'group' in request.GET and request.GET['group'] != '0':
		travels_all = travels_all.filter(group=request.GET['group'])
		current_group = Group.objects.get(pk=request.GET['group'])

	if 'company' in request.GET and request.GET['company'] != '0':
		travels_all = travels_all.filter(group__company=request.GET['company'])

	if 'buscompany' in request.GET and request.GET['buscompany'] != '0':
		travels_all = travels_all.filter(bus__company=request.GET['buscompany'])

	if 'driver' in request.GET and request.GET['driver'] != '0':
		travels_all = travels_all.filter(driver=request.GET['driver'])

	date_from = (request.GET['date_from'] if 'date_from' in request.GET else None)
	date_to = (request.GET['date_to'] if 'date_to' in request.GET else None)
	if date_from and date_to:
		travels_all = travels_all.filter(date__range=[date_from, date_to])
	elif date_from:
		travels_all = travels_all.exclude(date__lt=date_from)
	elif date_to:
		travels_all = travels_all.exclude(date__gt=date_to)


	paginator = Paginator(travels_all, 25)
	page = request.GET.get('page')

	try:
		travels = paginator.page(page)
	except PageNotAnInteger:
		travels = paginator.page(1)
	except EmptyPage:
		travels = paginator.page(paginator.num_pages)    

	context = {'nbar':'transport', 'logo':'img/logo-darwin-mini.png', 'travels':travels, 'groups':groups, 'busses':busses, 'buscompanies':buscompanies, 'drivers':drivers, 'itineraries':itineraries, 'companies':companies, 'current_group':current_group}
	return render(request, 'transport/filter.html', context)

@login_required
def travel_save(request, travel_id=None):
	if travel_id:
		t = get_object_or_404(Travel, pk=travel_id)
	else:
		t = Travel()
	try:
		group = Group.objects.get(pk=request.POST['group'])
		if request.POST['bus'] != '0':
			bus = Bus.objects.get(pk=request.POST['bus'])
		else:
			bus = None
		if request.POST['driver'] != '0':
			driver = Driver.objects.get(pk=request.POST['driver'])
		else:
			bus = None
		itinerary = Itinerary.objects.get(pk=request.POST['itinerary'])
		datetime_field = request.POST['datetime']
		notes = request.POST['notes']
	except:
		pass
	else:
		t.group = group
		t.bus = bus
		t.driver = driver
		t.itinerary = itinerary
		t.date = datetime.strptime(datetime_field.split(' ')[0], '%d/%m/%Y').strftime('%Y-%m-%d')
		t.time = datetime_field.split(' ')[1]
		t.notes = notes
		t.save()

	return HttpResponseRedirect(reverse('transport:index'))

@login_required
def group_save(request, group_id):
	g = get_object_or_404(Group, pk=group_id)

	try:
		id_string = request.POST['id_string']
		external_id = request.POST['external_id']
		company = Company.objects.get(pk=request.POST['company'])
		charge = request.POST['charge']
		debt = request.POST['debt']
		if debt == '':
			debt = '0'
	except:
		pass
	else:
		g.id_string = id_string
		g.external_id = external_id
		g.company = company
		g.charge = charge
		g.debt = debt
		g.save()

	return HttpResponseRedirect(reverse('transport:index'))

@login_required
def travel_pdf(request):
	travels = Travel.objects.all()
	info_raw = ()

	if 'group' in request.GET and request.GET['group'] != '0':
		travels = travels.filter(group=request.GET['group'])
		info_raw += ("Grupo: " + Group.objects.all().get(pk=request.GET['group']).__str__(),)
	else:
		info_raw += ("Grupo: TODOS",)

	if 'company' in request.GET and request.GET['company'] != '0':
		travels = travels.filter(group__company=request.GET['company'])
		info_raw += ("Empresa (Turismo):" + Company.objects.all().get(pk=request.GET['company']).short_name,)
	else:
		info_raw += ("Empresa (Turismo): TODAS",)

	if 'buscompany' in request.GET and request.GET['buscompany'] != '0':
		travels = travels.filter(bus__company=request.GET['buscompany'])
		info_raw += ("Empresa (Transportes):" + BusCompany.objects.all().get(pk=request.GET['buscompany']).__str__(),)
	else:
		info_raw += ("Empresa (Transportes): TODAS",)

	if 'driver' in request.GET and request.GET['driver'] != '0':
		travels = travels.filter(driver=request.GET['driver'])
		info_raw += ("Conductor:" + Driver.objects.all().get(pk=request.GET['driver']).__str__(),)
	else:
		info_raw += ("Conductor: TODOS",)


	date_from = (request.GET['date_from'] if 'date_from' in request.GET else None)
	date_to = (request.GET['date_to'] if 'date_to' in request.GET else None)
	if date_from and date_to:
		travels = travels.filter(date__range=[date_from, date_to])
		info_raw += ("Fechas: {} - {}".format(datetime.strptime(date_from , '%Y-%m-%d').strftime('%d/%d/%y'), datetime.strptime(date_to , '%Y-%m-%d').strftime('%d/%d/%y')),)
	elif date_from:
		travels = travels.exclude(date__lt=date_from)
		info_raw += ("Fechas: {} - // ".format(datetime.strptime(date_from , '%Y-%m-%d').strftime('%d/%d/%y')),)
	elif date_to:
		travels = travels.exclude(date__gt=date_to)
		info_raw += ("Fechas: // - {} ".format(datetime.strptime(date_to , '%Y-%m-%d').strftime('%d/%d/%y')),)
	else:
		info_raw += ("Fechas: TODAS",)


	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename='+"travel_list.pdf"
	
	buffer = BytesIO()
	pdf = DocumentBuilder(buffer).travel_list([info_raw], travels)
	
	response.write(pdf)

	return response