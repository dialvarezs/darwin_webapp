from datetime import datetime
from .models import Group


def current_season():
	now = datetime.now()
	yy = now.year if now.month > 8 else now.year - 1
	yy = str(yy)[2:] + str(yy + 1)[2:]
	return yy


def group_autoid():
	num = str(Group.objects.filter(id_string__contains=current_season()+'-').count()+1).zfill(3)
	return current_season() + '-' + num
