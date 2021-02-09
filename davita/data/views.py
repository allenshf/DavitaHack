from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EntryForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):

	return render(request, 'data/home.html')

@login_required
def enter_data(request):
	form = EntryForm()
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
