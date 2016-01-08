from datetime import datetime
from .models import Group

def group_autoid():
	yy = datetime.now().year if datetime.now().month > 9 else datetime.now().year-1
	yy = str(yy)[2:]+str(yy+1)[2:]
	num = str(Group.objects.filter(id_string__contains=yy+'-').count()+1).zfill(3)

	return yy+'-'+num