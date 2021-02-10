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


# Create your views here.
def home(request):
	return render(request, 'data/home.html')

def upload_image(request):
	if request.method == 'POST':
		upload = request.FILES['picture']
		fs = FileSystemStorage()
		fs.save(upload.name,upload)
		#TODO:Run image (upload) through OCR to get data for new Entry
		
		newEntry = Entry(user=request.user, pre_bp_dia=1,pre_bp_sys=1,pre_weight=1,post_bp_dia=1,post_bp_sys=1,post_weight=1)
		newImage = ImageModel(image=upload,entry=newEntry)
		newEntry.save()
		newImage.save()
		return redirect('/confirm/' + str(newEntry.id))
	return render(request, 'data/upload.html')

@login_required
def enter_data(request):
	form = EntryForm()
	#form = EntryForm(initial={'pre_bp_sys':pre_bp_sys,...})
	return render(request,'data/enter_data.html',{'form':form})

def submit_data(request):
	form = EntryForm(request.POST)
	if form.is_valid():
		entry = form.save(commit=False)
		entry.user = request.user
		entry.save()
		messages.success(request, 'Your Entry has Been Logged')
		return redirect('/')
	else:
		messages.warning(request,'Form is Incorrect/Incomplete')
		HttpResponseRedirect(request.META.get('HTTP_REFERER','/')) 

def confirm(request, id):
	form = EntryForm(instance=Entry.objects.get(id=id))
	return render(request,'data/enter_data.html',{'form':form})
