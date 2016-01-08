from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	context = {'nbar':'equipment_leasing',}
	return render(request, 'equipment_leasing/index.html', context)