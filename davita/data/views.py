from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EntryForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .models import Image as ImageModel
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from django.shortcuts import get_object_or_404
from django.utils import timezone
import io
import matplotlib.pyplot as plt
import urllib, base64
import pandas as pd
import numpy as np

# Create your views here.
def home(request):
	return render(request, 'data/home.html')

@login_required
def upload_image(request):
	if request.method == 'POST':
		upload = request.FILES['picture']
		fs = FileSystemStorage()
		fs.save(upload.name,upload)
		newEntry = parseData(upload)
		newImage = ImageModel(image=upload,entry=newEntry,url=upload.name)
		newEntry.save()
		newImage.save()
		return redirect('/confirm/' + str(newEntry.id))
	return render(request, 'data/upload.html')

#TODO:Run image through OCR to get data for new Entry
def parseData(image):

	return Entry(user=request.user, pre_bp_dia=1,pre_bp_sys=1,pre_weight=1,post_bp_dia=1,post_bp_sys=1,post_weight=1, date_created=timezone.now())


@login_required
def enter_data(request):
	form = EntryForm()
	#form = EntryForm(initial={'pre_bp_sys':pre_bp_sys,...})
	return render(request,'data/enter_data.html',{'form':form,'confirm':False})


@login_required
def submit_data(request,id=0):
	flag = request.session.get('flag')
	if flag is None:
		flag = True
	form = EntryForm(request.POST)
	if form.is_valid():
		entry = form.save(commit=False)
		if id > 0:
			entry.id = id
			entry.date_created = Entry.objects.get(id=id).date_created
		else:
			entry.date_created = timezone.now()
		entry.user = request.user
		entry.save()
		if flag and (entry.pre_bp_dia < entry.post_bp_dia or entry.pre_bp_sys < entry.post_bp_sys or entry.pre_weight < entry.post_weight):
			messages.warning(request,'One or more post-treatment metrics is higher than pre-treament. Are you sure everything is correct?')
			request.session['flag'] = False
			return redirect('/confirm/' + str(entry.id))
		request.session['flag'] = True
		messages.success(request, 'Your Entry has Been Logged')
		return redirect('/')
	else:
		messages.error(request,'Form is Incorrect/Incomplete')
		HttpResponseRedirect(request.META.get('HTTP_REFERER','/')) 

@login_required
def confirm(request, id):
	entry = get_object_or_404(Entry,id=id, user=request.user)
	form = EntryForm(instance=entry)
	return render(request,'data/enter_data.html',{'form':form,'confirm':True,'id':id})

@login_required
def data(request,field=''):

	if field == 'bps':
		cat = 'Systolic Blood Pressure'
		data = [ {'date': entry.date_created, 'pre_bps': entry.pre_bp_sys,
			'post_bps': entry.post_bp_sys, 'avg': (entry.pre_bp_sys+entry.post_bp_sys)/2} for entry in request.user.entry_set.all().order_by('date_created')]
		df = pd.DataFrame(data)	
		y_LL = int(df['post_bps'].min()*0.9)
		y_UL = int(df['pre_bps'].max()*1.1)
	elif field == 'bpd':
		cat = 'Diastolic Blood Pressure'
		data = [ {'date': entry.date_created, 'pre_bpd': entry.pre_bp_dia,
			'post_bpd': entry.post_bp_dia, 'avg': (entry.pre_bp_dia+entry.post_bp_dia)/2} for entry in request.user.entry_set.all().order_by('date_created')]
		df = pd.DataFrame(data)
		y_LL = int(df['post_bpd'].min()*0.9)
		y_UL = int(df['pre_bpd'].max()*1.1)
	else:
		cat = 'Weight'
		data = [ {'date': entry.date_created,'pre_wei': entry.pre_weight,
			'post_wei': entry.post_weight,'avg': (entry.pre_weight+entry.post_weight)/2} for entry in request.user.entry_set.all().order_by('date_created')]
		df = pd.DataFrame(data)
		y_LL = int(df['post_wei'].min()*0.9)
		y_UL = int(df['pre_wei'].max()*1.1)

	if int(df['avg'].max()) > int(df['avg'][0]*1.1):
<<<<<<< HEAD
		messages.warning(request, 'Note: Your ' + str(cat) + " has increased by over 10% recently.")
=======
		messages.warning(request,'Alert: Your ' + str(cat) + " has increased by over 10% recently.")
>>>>>>> 9ab4c46f95fab14759c38120b55c9246f0c168f2

	y_interval = 10

	x_LL = data[0]['date']
	x_UL = data[-1]['date']
	mycolors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange'] 

	# Draw Plot and Annotate
	fig, ax = plt.subplots(1,1,figsize=(16, 9), dpi= 80)    
	columns = df.columns[1:3]  
	for i, column in enumerate(columns):    
		if i == 0:
			plt.plot(df.date.values, df[column].values, lw=1.5, color=mycolors[i], label='Pre-Treatment')   
		else:
			plt.plot(df.date.values, df[column].values, lw=1.5, color=mycolors[i], label='Post-Treatment')   
		plt.text(df.shape[0]+1, df[column].values[-1], column, fontsize=14, color=mycolors[i])

	# Draw Tick lines  
	for y in range(y_LL, y_UL, y_interval):    
		plt.hlines(y, xmin=x_LL, xmax=x_UL, colors='black', alpha=0.3, linestyles="--", lw=0.5)

	# Decorations    
	plt.tick_params(axis="both", which="both", bottom=False, top=False,    
					labelbottom=True, left=False, right=False, labelleft=True)        

	# Lighten borders
	plt.gca().spines["top"].set_alpha(.3)
	plt.gca().spines["bottom"].set_alpha(.3)
	plt.gca().spines["right"].set_alpha(.3)
	plt.gca().spines["left"].set_alpha(.3)

	if field == 'bps':
		plt.title('Systolic Blood Pressure vs Time')
		plt.ylabel('Blood Pressure (Systolic)')
	elif field == 'bpd':
		plt.title('Diastolic Blood Pressure vs Time')
		plt.ylabel('Blood Pressure (Diastolic)')
	else:
		plt.title('Weight vs Time')
		plt.ylabel('Weight(Pounds)')
	plt.xlabel('Date')
	plt.yticks(range(y_LL, y_UL, y_interval), [str(y) for y in range(y_LL, y_UL, y_interval)], fontsize=12)    
	plt.ylim(y_LL, y_UL)   
	plt.xlim(x_LL, x_UL) 
	plt.legend()
	
	fig = plt.gcf()
	buf = io.BytesIO()
	fig.savefig(buf,format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	url = urllib.parse.quote(string)
	
	return render(request,'data/data.html',{'data':url})
