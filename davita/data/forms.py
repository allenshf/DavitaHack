from django import forms
from django.forms import ModelForm
from .models import Entry

class EntryForm(ModelForm):

	class Meta:
		model = Entry
		exclude = ('user', 'date_created',)
		fields = ['pre_bp_sys','pre_bp_dia','pre_weight','post_bp_sys','post_bp_dia','post_weight']
		labels = {'pre_bp_sys': 'Pre-Treatment Blood Pressure (Higher number)','pre_bp_dia':'Pre-Treatment Blood Pressure (Lower number)',
		'pre_weight': 'Pre-Treatment Weight (lbs)','post_bp_sys': 'Post-Treatment Blood Pressure (Higher number)',
		'post_bp_dia': 'Post-Treatment Blood Pressure (Lower number)','post_weight': 'Post-Treatment Weight (lbs)'}

