from RESCLIMA.settings import GPX_FILES_PATH
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import os

def file_directory_path(instance, filename):
	# File will be uploaded to MEDIA_ROOT/simulation/user_<id>/simulation_<id>/<filename>
	return GPX_FILES_PATH+str(filename.cleaned_data['sensor'].id)+"-"+str(filename.cleaned_data['date_init'])+"-"+str(filename.cleaned_data['date_last'])


def validate_file_extension_config(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = ['.gpx']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Debe Ingresar Archivo de puntos de tracking')
