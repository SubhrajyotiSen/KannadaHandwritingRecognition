from django import forms
from .models import DocumentImage

"""
	The following method of form description is used to take advantage of django
	form.as_p functionality.
	It reads the meta data and prepares form with label and name by itself

	Call in html file looks like {{form.as_p}}
	
"""


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentImage
        fields = ('image_url', )
